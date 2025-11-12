from fastapi import FastAPI, Request, Form, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import sqlite3
from recommender import get_recommendations


app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

# calls the get_recommendations function using selected movies and outputs the results onto the recommendations template 
@app.post("/recommend", response_class=HTMLResponse)
async def recommend(request: Request, movie_ids: list[int] = Form(...)):
    recommendations = get_recommendations(movie_ids)
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    
    # variable number of placeholders to be insert into sql statement 
    placeholders = ','.join('?' * len(recommendations))
    cursor.execute(f"SELECT movie_id, original_title FROM movie WHERE movie_id In ({placeholders})", recommendations["movie_id"].tolist())
    title_map = dict(cursor.fetchall())
    conn.close()
    # transform results into jinja compliant format 
    recommendations["original_title"] = recommendations["movie_id"].map(title_map)
    recommendations = recommendations[["original_title", "similarity"]]

    return templates.TemplateResponse(
        "recommendations.html", 
        {"request": request, "recommendations": recommendations.to_dict(orient="records")}
    )

# returns movie titles that are similar to the searched for title 
@app.get("/search_movies")
def search_movies(q: str = Query("", min_length = 1, desc="Movie search Query")):
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute('''
                    SELECT movie_id, original_title
                    FROM movie 
                    WHERE LOWER(original_title) LIKE LOWER(?)
                    ORDER BY popularity
                    LIMIT 5
                   ''', (f"%{q.replace(' ', '').lower()}%",) )
    results = cursor.fetchall()
    conn.close()

    return JSONResponse([{"id": movie_id, "original_title": original_title} for movie_id, original_title in results])
    
