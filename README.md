# Spy Cat Agency

A full-stack application to manage a secret organization of spy cats. This project demonstrates a modern **FastAPI** (Python) backend integrated with a **Next.js** (TypeScript) frontend.

## Features

* **Agent Management**: Recruit (create) new cats with details like experience and salary.
* **Breed Validation**: Automatically validates cat breeds using [TheCatAPI](https://thecatapi.com/) to ensure only real breeds are recruited.
* **Mission Control**: (Backend) Logic to assign missions to cats, ensuring agents are only on one active mission at a time.
* **Responsive Dashboard**: A clean UI built with Tailwind CSS to view, edit, and retire agents.

## Tech Stack

* **Backend:** Python, FastAPI, SQLAlchemy, SQLite
* **Frontend:** TypeScript, Next.js 16 (App Router), Tailwind CSS, Lucide React

## Project Structure

```text
├── client/      # Next.js Frontend
└── server/      # FastAPI Backend
```

## Getting Started

Follow these steps to run the project locally. You will need two terminal windows.

### 1. Start the Backend (Server)

Navigate to the server directory and set up the Python environment.

```bash
cd server

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload
```

*The backend API will run at `http://127.0.0.1:8000`.*

*API Documentation (Swagger UI) available at `http://127.0.0.1:8000/docs`.*

### 2. Start the Frontend (Client)

Open a new terminal, navigate to the client directory, and start the React app.

```bash
cd client

# Install dependencies
npm install

# Run the development server
npm run dev
```

*The frontend dashboard will run at `http://localhost:3000`.*

## Usage

1. Open `http://localhost:3000` in your browser.
2. Use the form to **Recruit** a new agent.
* *Note: The "Breed" field is validated against TheCatAPI. Try "Siberian" or "Persian".*
3. Click the **Edit** (pencil) icon to update an agent's salary.
4. Click the **Trash** icon to retire (delete) an agent.

## License

This project is available under the MIT License.