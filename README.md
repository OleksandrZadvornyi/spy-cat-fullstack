# Spy Cat Agency

**[Live Demo](https://spy-cat-fullstack.vercel.app/)** | **[API Documentation](https://spy-cat-backend.onrender.com/docs)**

A full-stack application to manage a secret organization of spy cats. This project demonstrates a modern **FastAPI** (Python) backend integrated with a **Next.js** (TypeScript) frontend.

## Live Deployment

* **Frontend (Vercel):** [https://spy-cat-fullstack.vercel.app/](https://spy-cat-fullstack.vercel.app/)
* **Backend (Render):** [https://spy-cat-backend.onrender.com/](https://spy-cat-backend.onrender.com/)
* **Swagger UI:** [https://spy-cat-backend.onrender.com/docs](https://spy-cat-backend.onrender.com/docs)

## Features

* **Agent Management**: Recruit (create) new cats with details like experience and salary.
* **Breed Validation**: Automatically validates cat breeds using [TheCatAPI](https://thecatapi.com/) to ensure only real breeds are recruited.
* **Mission Control**: (Backend) Logic to assign missions to cats, ensuring agents are only on one active mission at a time.
* **Responsive Dashboard**: A clean UI built with Tailwind CSS to view, edit, and retire agents.
* **Persistent Data**: Hosted on PostgreSQL (Neon/Supabase) to ensure data survives server restarts.

## Tech Stack

* **Backend:** Python, FastAPI, SQLAlchemy, PostgreSQL
* **Frontend:** TypeScript, Next.js 16 (App Router), Tailwind CSS, Lucide React
* **Deployment:** Vercel (Frontend), Render (Backend)

## Project Structure

```text
├── client/      # Next.js Frontend
└── server/      # FastAPI Backend
```

## Local Development

Follow these steps to run the project locally on your machine.

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

## License

This project is available under the MIT License.