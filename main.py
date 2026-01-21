from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, validator
from typing import List, Optional
import requests
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session

# --- DATABASE SETUP ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./spy_cat.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- MODELS ---
class CatDB(Base):
    __tablename__ = "cats"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    years_of_experience = Column(Integer)
    breed = Column(String)
    salary = Column(Float)

class MissionDB(Base):
    __tablename__ = "missions"
    id = Column(Integer, primary_key=True, index=True)
    cat_id = Column(Integer, ForeignKey("cats.id"), nullable=True) # Assigned later
    is_complete = Column(Boolean, default=False)
    targets = relationship("TargetDB", back_populates="mission")

class TargetDB(Base):
    __tablename__ = "targets"
    id = Column(Integer, primary_key=True, index=True)
    mission_id = Column(Integer, ForeignKey("missions.id"))
    name = Column(String)
    country = Column(String)
    notes = Column(String, default="")
    is_complete = Column(Boolean, default=False)
    mission = relationship("MissionDB", back_populates="targets")

Base.metadata.create_all(bind=engine)

# --- SCHEMAS  ---
class CatCreate(BaseModel):
    name: str
    years_of_experience: int
    breed: str
    salary: float

    @validator('breed')
    def validate_breed(cls, v):
        # TheCatAPI Validation Logic
        response = requests.get("https://api.thecatapi.com/v1/breeds")
        breeds = [b['name'] for b in response.json()]
        if v not in breeds:
           raise ValueError(f"Breed {v} not recognized by TheCatAPI")
        return v

class CatResponse(CatCreate):
    id: int
    class Config:
        orm_mode = True

# --- MISSION & TARGET SCHEMAS ---
class TargetBase(BaseModel):
    name: str
    country: str
    notes: Optional[str] = ""
    is_complete: Optional[bool] = False

class MissionCreate(BaseModel):
    cat_id: Optional[int] = None
    targets: List[TargetBase]

    @validator('targets')
    def validate_targets(cls, v):
        if not (1 <= len(v) <= 3):
            raise ValueError('A mission must have between 1 and 3 targets')
        return v

class TargetResponse(TargetBase):
    id: int
    mission_id: int
    class Config:
        orm_mode = True

class MissionResponse(BaseModel):
    id: int
    cat_id: Optional[int]
    is_complete: bool
    targets: List[TargetResponse]
    class Config:
        orm_mode = True

class TargetUpdate(BaseModel):
    notes: Optional[str] = None
    is_complete: Optional[bool] = None

# --- APP ---
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ENDPOINTS: SPY CATS ---
@app.post("/cats/", response_model=CatResponse)
def create_cat(cat: CatCreate, db: Session = Depends(get_db)):
    # 1. Validate Breed with external API
    res = requests.get(f"https://api.thecatapi.com/v1/breeds/search?q={cat.breed}")
    if not res.json():
         raise HTTPException(status_code=400, detail="Invalid Breed (checked against TheCatAPI)")

    db_cat = CatDB(**cat.dict())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

@app.get("/cats/", response_model=List[CatResponse])
def list_cats(db: Session = Depends(get_db)):
    return db.query(CatDB).all()

@app.get("/cats/{cat_id}", response_model=CatResponse)
def get_cat(cat_id: int, db: Session = Depends(get_db)):
    cat = db.query(CatDB).filter(CatDB.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    return cat

@app.delete("/cats/{cat_id}")
def delete_cat(cat_id: int, db: Session = Depends(get_db)):
    cat = db.query(CatDB).filter(CatDB.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    db.delete(cat)
    db.commit()
    return {"ok": True}

@app.put("/cats/{cat_id}/salary")
def update_salary(cat_id: int, salary: float, db: Session = Depends(get_db)):
    cat = db.query(CatDB).filter(CatDB.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    cat.salary = salary
    db.commit()
    return {"ok": True, "new_salary": salary}

# --- ENDPOINTS: MISSIONS ---
@app.post("/missions/", response_model=MissionResponse)
def create_mission(mission: MissionCreate, db: Session = Depends(get_db)):
    # Validate Cat Availability (One cat = One active mission)
    if mission.cat_id:
        active_mission = db.query(MissionDB).filter(
            MissionDB.cat_id == mission.cat_id, 
            MissionDB.is_complete == False
        ).first()
        if active_mission:
            raise HTTPException(status_code=400, detail="Cat already has an active mission")

    # Create Mission
    db_mission = MissionDB(cat_id=mission.cat_id, is_complete=False)
    db.add(db_mission)
    db.commit()
    db.refresh(db_mission)

    # Create Targets
    for target in mission.targets:
        db_target = TargetDB(
            mission_id=db_mission.id,
            name=target.name,
            country=target.country,
            notes=target.notes,
            is_complete=target.is_complete
        )
        db.add(db_target)
    
    db.commit()
    db.refresh(db_mission)
    return db_mission

@app.get("/missions/", response_model=List[MissionResponse])
def list_missions(db: Session = Depends(get_db)):
    return db.query(MissionDB).all()

@app.get("/missions/{mission_id}", response_model=MissionResponse)
def get_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.query(MissionDB).filter(MissionDB.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission

@app.delete("/missions/{mission_id}")
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.query(MissionDB).filter(MissionDB.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    # Cannot delete if assigned to a cat
    if mission.cat_id is not None:
         raise HTTPException(status_code=400, detail="Cannot delete mission assigned to a cat")

    # Delete targets first
    db.query(TargetDB).filter(TargetDB.mission_id == mission_id).delete()
    db.delete(mission)
    db.commit()
    return {"ok": True}

@app.post("/missions/{mission_id}/assign/{cat_id}")
def assign_cat(mission_id: int, cat_id: int, db: Session = Depends(get_db)):
    mission = db.query(MissionDB).filter(MissionDB.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    # Check if cat is free
    active_mission = db.query(MissionDB).filter(
        MissionDB.cat_id == cat_id, 
        MissionDB.is_complete == False
    ).first()
    if active_mission:
        raise HTTPException(status_code=400, detail="Cat already has an active mission")

    mission.cat_id = cat_id
    db.commit()
    return {"ok": True}

# --- ENDPOINTS: TARGETS ---
@app.patch("/targets/{target_id}")
def update_target(target_id: int, update_data: TargetUpdate, db: Session = Depends(get_db)):
    target = db.query(TargetDB).filter(TargetDB.id == target_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    
    mission = target.mission

    # Notes are frozen if target OR mission is complete
    if update_data.notes is not None:
        if target.is_complete or mission.is_complete:
             raise HTTPException(status_code=400, detail="Cannot update notes: Target or Mission is closed")
        target.notes = update_data.notes

    if update_data.is_complete is not None:
        target.is_complete = update_data.is_complete
        
        # Check if ALL targets are complete
        all_targets = db.query(TargetDB).filter(TargetDB.mission_id == mission.id).all()
        if all(t.is_complete for t in all_targets):
            mission.is_complete = True
        else:
            mission.is_complete = False # Re-open if someone unchecks a target

    db.commit()
    db.refresh(target)
    return target

# CORS for Frontend
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)