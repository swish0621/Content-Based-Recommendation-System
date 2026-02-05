import os
import sqlite3
from fastapi import FastAPI, Query, Body
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.feature.recommender import get_recommendations



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://content-based-recommendation-system-v2.onrender.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Calls the get_recommendations function using selected movies and outputs the results onto the recommendations template 
@app.post("/recommend")
async def recommend(movie_ids: list[int] = Body(...)):
    recommendations = get_recommendations(movie_ids)
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    
    # Variable number of placeholders to be insert into sql statement 
    placeholders = ','.join('?' * len(recommendations))
    cursor.execute(f"SELECT movie_id, original_title FROM movie WHERE movie_id In ({placeholders})", recommendations["movie_id"].tolist())
    title_map = dict(cursor.fetchall())
    conn.close()
    
    # Transform results into jinja compliant format 
    recommendations["original_title"] = recommendations["movie_id"].map(title_map)
    
    return recommendations[["original_title", "similarity"]].to_dict(orient="records")

# Returns movie titles that are similar to the searched for title 
@app.get("/search")
def search_movies(q: str = Query(..., min_length = 1, description="Movie search Query")):
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute('''
                    SELECT movie_id, original_title
                    FROM movie 
                    WHERE LOWER(original_title) LIKE ?
                    ORDER BY popularity DESC
                    LIMIT 5
                   ''', (f"%{q.lower()}%",) )
    results = cursor.fetchall()
    conn.close()

    return JSONResponse([{"id": movie_id, "original_title": original_title} for movie_id, original_title in results])
    
# --- RENDER DEPLOYMENT LOGIC ---

# 1. Define paths to the React build folder
# main.py is in /backend, so go up one level to find /frontend/dist
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(BASE_DIR, "frontend", "dist")

# 2. Serve static assets (JS/CSS)
# React looks for these in /assets/
if os.path.exists(os.path.join(DIST_DIR, "assets")):
    app.mount("/assets", StaticFiles(directory=os.path.join(DIST_DIR, "assets")), name="static")

# 3. Catch-all: Serve index.html for all other routes
# This lets React handle its own routing
@app.get("/{catchall:path}")
async def serve_react(catchall: str):
    index_path = os.path.join(DIST_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse(status_code=404, content={"message": "Frontend files not found. Ensure 'npm run build' was successful."})
