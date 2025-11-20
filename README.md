![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-teal)
![SQLite](https://img.shields.io/badge/SQLite-Database-gray)
![Render](https://img.shields.io/badge/Deployed%20on-Render-purple)

# Content-Based-Recommendation-System
This project is a content-based movie recommender built from The Movies Dataset on Kaggle (rounakbanik).

The system loads the raw CSVs, cleans and normalizes the metadata, stores everything in a structured SQLite database, and builds sparse feature vectors for each movie using TF-IDF (keywords), multilabel encodings (genres, companies), and one-hot encoding (collections). 

Cosine similarity is used to score intra movie relationships or generate a user profile from multiple inputs and deliver recommendations based on the profile. 

A FastAPI backend serves the recommender, handling all interaction through a frontend UI and API endpoints. 

The goal of this project was to build a clean, modular recommendation engine that mirrors how real systems are designed. The data pipeline (data ingestion, preprocessing, database modeling, feature generation, and serving layer) was modeled to resemble what you’d see in an actual production setup. To show how these kinds of systems may be used in real business environments, the recommender is wrapped in a full-stack application and deployed via Render.

## 🚀 Features
- Content-based recommendations built from movie metadata including keywords, genres, collections, and production companies.

- TF-IDF keyword vectors combined with multilabel and one hot encoded features to represent each movie in a sparse vector space.

- User profile generation that averages feature vectors from multiple selected movies to create a personalized recommendation baseline.

- Cosine similarity scoring to measure how closely movies match the user profile or each other.

- Normalized relational (SQLite) database with purposeful many to many relationships for genres, companies, collections, and keywords.

- FastAPI backend that serves recommendations, handles movie search, and drives the frontend UI.

- Similarity matrix caching in the validation pipeline to speed up repeated evaluation.

- Precision at 5 validation tools to evaluate the quality of recommendations.

- Deployed via Render as a full stack application.

## 📌 View Deployed Demo
```
https://content-based-recommendation-system-ofm5.onrender.com/
```
<img width="1920" height="642" alt="Screenshot 2025-11-11 at 11 55 52 PM" src="https://github.com/user-attachments/assets/d0f8ae73-5847-4f7b-b9a2-f86e9ddf68ca" />


## 🧠 System Architecture Overview
The system follows a standard pipeline used in metadata-driven similarity models. The workflow moves from raw metadata, through preprocessing and structured storage, into feature generation and vector similarity computation, and finally into the serving layer that presents similarity rankings to users in an easily digestible format.

```
Raw CSV Data
      ↓
Preprocessing and Normalization
      ↓
SQLite Database (movies, genres, collections, companies, keywords)
      ↓
Feature Engineering (TF-IDF, multilabel, one hot encoding)
      ↓
Combined Sparse Feature Matrix
      ↓
Recommender Engine (cosine similarity and user profiling)
      ↓
FastAPI Backend (search and recommend endpoints)
      ↓
Frontend UI (movie selection and results)
      ↓
Render Deployment
```
## 🛠️ Tech Stack
- Python 3.12 – Core language used for data preprocessing, feature engineering, similarity computation, and application logic.

- FastAPI – Backend framework that exposes search and recommendation endpoints and serves the frontend interface.

- SQLite – Structured relational database used to store cleaned movie metadata and many-to-many relationships.

- Pandas / NumPy – Used for data loading, cleaning, numerical operations, and DataFrame manipulation.

- Scikit-learn – Provides TF-IDF vectorization, multilabel encoders, one-hot encoding, and cosine similarity utilities.

- SciPy – Powers sparse matrix operations and efficient vector space handling.

- Jinja2 Templates – Renders UI pages for interacting with the recommender.

- Render – Deployment platform hosting the full-stack application.

## ▶️ Running Instructions (Local Host)
### Clone the Repository
```
git clone https://github.com/swish0621/Content-Based-Recommendation-System.git
cd Content-Based-Recommendation-System
```
### Create and Activate Virtual Environment 
```
python3 -m venv venv
source venv/bin/activate   # macOS / Linux
# or
venv\Scripts\activate      # Windows
```
### Install Dependencies
```
pip install -r requirements.txt
```
### Build SQLite Database
```
python -m db
```
### Optional: Run Validation 
```
python -m validation.validation
```
### Start FastAPI Application
```
uvicorn main:app --reload
```
### Open Application
```
http://127.0.0.1:8000
```
## Key Learnings
- Designed a modular data pipeline from ingestion to serving layer.

- Implemented sparse vector similarity search with TF-IDF and cosine similarity.

- Modeled normalized relational data with many-to-many relationships.

- Built a full-stack deployed application using FastAPI and Render.

- Developed validation tools (Precision@5) to evaluate model quality.

## Project Structure 
```
Content-Based-Recommendation-System/
│── data_processing/       # Ingestion, cleaning, feature generation
│── db/                    # Database schema, load scripts, and CRUD
│── feature/               # Recommender engine logic
│── validation/            # Precision@5 evaluation tools
│── templates/             # Jinja2 frontend pages
│── static/                # CSS
│── main.py                # FastAPI app entry point
│── movies.db              # SQLite database
│── requirements.txt
```
