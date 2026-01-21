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

# CORS for Frontend
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)