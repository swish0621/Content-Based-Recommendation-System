# ------------------------
# Data Preprocessing Script 
# ------------------------
# Cleans Movie and Keyword Data for Database Input


import pandas as pd
import ast
import json

# Import the dataframes created in download_data
from data_processing.download_data import keywords
from data_processing.download_data import movies

from sklearn.feature_extraction.text import CountVectorizer



# Convert keywords from string to python data values and create a new column of cleaned keyword names
def convert_keywords(keyword):
    try: 
        key_lst = ast.literal_eval(keyword)
        result = []
        for key in key_lst:
            result.append(key["name"].lower().replace(" ", ""))
        return result
    except (ValueError):
        return []

# Create new column keyword_lists with cleaned keywords in list form 
keywords["keyword_lists"] = keywords["keywords"].apply(convert_keywords)

# Create another column "key_space_sep" with list item keywords converted to space separated strings 
keywords["key_space_sep"] = keywords["keyword_lists"].apply(lambda x: " ".join(x))

keywords = keywords.rename(columns={"id": "original_id"})
keywords["original_id"] = pd.to_numeric(keywords["original_id"], errors="coerce").astype(int)

# Remove excess columns from data 
columns = [
    "id",
    "title",
    "genres",
    "belongs_to_collection",
    "original_language",
    "popularity",
    "production_companies"
]

movies = movies[columns].copy()
movies["original_title"] = movies["title"]

# REMOVE THESE 2 LINES TO USE THE FULL DATASET
# DATA LIMITED TO WORK WITH FREE TIER RENDER 
movies = movies.head(5000)
keywords = keywords.head(5000)

# Function to parse metadata columns (could be json string or string converted python lists)
def json_col(col):
    try:
        # Handle empty / missing values
        if pd.isna(col) or col == "":
            return []
        
        # Try json parsing first
        try:
            metadata = json.loads(col)
        # If unsuccessful switch to python list 
        except json.JSONDecodeError:
            metadata = ast.literal_eval(col)

        # Extract name from list / dict and lowercase / remove spaces
        if isinstance(metadata, list):
            return [item.get("name", "").lower().replace(" ", "") for item in metadata if "name" in item]
        
        elif isinstance(metadata, dict) and "name" in metadata:
            return [metadata["name"].lower().replace(" ", "")]
        
        else:
            return []
        
    # Catch any errors and return an empty list
    except (ValueError, TypeError, SyntaxError):
        return []
            

# Function to clean and normalize movies dataframe
def clean_movies(movies):
    # Drop any rows that would violate the db rules
    movies = movies.dropna(subset=["title", "id"])

    # Convert id to numeric if invalid coerce to NaN and rename to original_id
    movies["id"] = pd.to_numeric(movies["id"], errors="coerce").astype(int)
    movies = movies.rename(columns={"id": "original_id"})

    # Normalize to lowercase and no spaces
    movies["title"] = movies["title"].str.lower().str.replace(" ", "", regex=False)
    movies["original_language"] = movies["original_language"].str.lower().str.replace(" ", "", regex=False)

    # Parse columns with json lists 
    movies["genres"] = movies["genres"].apply(json_col)
    movies["belongs_to_collection"] = movies["belongs_to_collection"].apply(json_col)
    movies["production_companies"] = movies["production_companies"].apply(json_col)

    # Convert to integer / replace invalid vals with 0
    movies["popularity"] = pd.to_numeric(movies["popularity"], errors="coerce").fillna(0).astype(int)

    return movies

movies = clean_movies(movies)



