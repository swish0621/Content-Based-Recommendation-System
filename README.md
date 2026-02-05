![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-teal)
![SQLite](https://img.shields.io/badge/SQLite-Database-gray)
![React](https://img.shields.io/badge/React-Frontend-61dafb)
![TypeScript](https://img.shields.io/badge/TypeScript-Frontend-3178c6)
![Vite](https://img.shields.io/badge/Vite-Build%20Tool-646cff)

# Content-Based Recommendation System (Full Stack)

A content-based movie recommender built from **The Movies Dataset (Kaggle / rounakbanik)**.

This project:
- ingests + cleans raw CSV movie metadata
- stores normalized data in a **SQLite** database
- builds sparse feature vectors per movie using **TF-IDF** (keywords) + encoded metadata (genres/companies/collections)
- generates recommendations using **cosine similarity**, including a multi-movie “user profile” approach
- serves results through a **FastAPI backend** and a **React + TypeScript frontend** (Vite)

---

## 🚀 Features

### Recommender Engine
- Content-based similarity using keywords, genres, collections, and production companies  
- TF-IDF keyword vectors + encoded metadata combined into a single sparse matrix
- Multi-movie **user profile** generation (averaged vector representation)  
- Cosine similarity scoring and recommendation filtering

### Backend (FastAPI)
- `/search` endpoint for movie lookup
- `/recommend` endpoint (POST) accepts an array of `movie_id`s and returns ranked recommendations
- SQLite-backed title lookup for display
- Optional cached artifacts (e.g., similarity matrix) to speed repeat runs

### Frontend (React + TypeScript)
- Search UI → select movies → request recommendations
- Componentized UI:
  - `SearchResults`
  - `SelectedMovies`
  - `Recommendations`
- Loading + error handling for API calls
- Basic CSS styling for a clean, usable UI

---

## 📌 View Deployed Demo
**Live Link:** [https://content-based-recommendation-system-ofm5.onrender.com/](https://content-based-recommendation-system-v2.onrender.com/)

<img width="1920" height="642" alt="Screenshot" src="https://github.com/user-attachments/assets/d0f8ae73-5847-4f7b-b9a2-f86e9ddf68ca" />

---

## 🧠 High-Level Architecture

```text
Raw CSV Data
↓
Preprocessing / Normalization
↓
SQLite Database (movies + supporting tables)
↓
Feature Engineering (TF-IDF + encoded metadata)
↓
Combined Sparse Feature Matrix
↓
Recommender (cosine similarity + user profiling)
↓
FastAPI Backend (/search, /recommend)
↓
React + TypeScript Frontend (Vite)
```

---

## 🛠️ Tech Stack

**Backend**
- Python 3.12
- FastAPI
- SQLite
- pandas / numpy
- scikit-learn (TF-IDF, cosine similarity)
- scipy (sparse matrices)

**Frontend**
- React
- TypeScript
- Vite
- CSS

---

## ▶️ Run Locally

### 1) Clone repo
```bash
git clone https://github.com/swish0621/Content-Based-Recommendation-System.git
cd Content-Based-Recommendation-System
```
### Backend Setup (Python)
```
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows

pip install -r requirements.txt
python -m backend.db       # Build SQLite Database
uvicorn backend.main:app --reload
```
App will run on:
```
 http://127.0.0.1:8000
```

### Frontend setup (React + TypeScript)
```
cd frontend
npm install
npm run dev
```

### Vite dev server will run on:
```
http://127.0.0.1:5173
```

## 📡 API Endpoints

#### GET /search?q=\<query>  
Returns a list of matching movies.  
Example:
```
[
  { "id": 123, "original_title": "Toy Story" },
  { "id": 456, "original_title": "Toy Story 2" }
]
```

#### POST /recommend  
Body: JSON array of selected movie IDs  
Request:
```
[123, 456]
```

Example response:
```
[
  { "original_title": "A Bug's Life", "similarity": 0.63 },
  { "original_title": "Monsters, Inc.", "similarity": 0.61 }
]
```

## 📁 Project Structure 
```
.
├── backend/                 # FastAPI app + recommender pipeline
│   ├── data_processing/     # ingestion / preprocessing / transforms
│   ├── db/                  # db setup / load / crud
│   ├── feature/             # recommender logic
│   └── main.py              # FastAPI entry point
├── frontend/                # Vite React + TS app
│   └── src/
│       ├── components/      # UI components
│       ├── App.tsx          # state + orchestration
│       └── types.ts         # shared frontend types
├── movies.db                # SQLite database (generated locally)
├── requirements.txt
└── build.sh                 # Render build script

```
## Key Learnings
- Built a full pipeline from raw dataset ingestion → normalized storage → feature engineering → similarity search

- Implemented sparse vector similarity and multi-item profile recommendations

- Integrated a FastAPI backend with a React + TypeScript frontend (async calls, loading/error states, component props)

- Practiced real full-stack debugging around API contracts, payloads, and response handling
