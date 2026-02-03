from fastapi import FastAPI, Request, Form, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Body
import sqlite3
from backend.feature.recommender import get_recommendations


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

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
    
