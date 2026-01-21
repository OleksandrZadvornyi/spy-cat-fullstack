# Spy Cat Agency - Backend

The REST API for the Spy Cat Agency, built with **FastAPI**.
It manages agents (cats), missions, and targets, utilizing **SQLAlchemy** for persistence and **TheCatAPI** for breed validation.

## Setup

1.  **Create Virtual Env:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: .\venv\Scripts\activate
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run Server:**
    ```bash
    uvicorn main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.
    Docs: `http://127.0.0.1:8000/docs`.

## 📡 API Documentation
[Link to Postman Collection](https://www.postman.com/oleksandrzadvornyi-7638218/spy-cat-agency/collection/51549141-10da6a80-a13d-4200-8a61-c4a872a3379c?action=share&creator=51549141)