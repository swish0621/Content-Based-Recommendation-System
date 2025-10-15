# Nicholas Swisher
# Purpose: to preprocess and vectorize the data
# download_data.py must be run before this file

import pandas as pd
import ast
import json

# import the dataframes created in download_data
from download_data import keywords
from download_data import movies

from sklearn.feature_extraction.text import CountVectorizer



# convert keywords from string to python data values and create a new column of cleaned keyword names
def convert_keywords(keyword):
    try: 
        key_lst = ast.literal_eval(keyword)
        result = []
        for key in key_lst:
            result.append(key["name"].lower().replace(" ", ""))
        return result
    except (ValueError):
        return []

# create new column keyword_lists with cleaned keyswords in list form 
keywords["keyword_lists"] = keywords["keywords"].apply(convert_keywords)

# create another column "key_space_sep" with list item keywords converted to space separated strings 
keywords["key_space_sep"] = keywords["keyword_lists"].apply(lambda x: " ".join(x))

# remove excess columns from data 
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

# function to parse metadata columns (could be json string or string converted python lists)
def json_col(col):
    try:
        # handle empty / missing values
        if pd.isna(col) or col == "":
            return []
        
        # try json parsing first
        try:
            metadata = json.loads(col)
        # if unsuccessful switch to python list 
        except json.JSONDecodeError:
            metadata = ast.literal_eval(col)

        # extract name from list / dict and lowercase / remove spaces
        if isinstance(metadata, list):
            return [item.get("name", "").lower().replace(" ", "") for item in metadata if "name" in item]
        
        elif isinstance(metadata, dict) and "name" in metadata:
            return [metadata["name"].lower().replace(" ", "")]
        
        else:
            return []
        
    # catch any errors and return an empty list
    except (ValueError, TypeError, SyntaxError):
        return []
            

# function to clean and normalize movies dataframe
def clean_movies(movies):
    # convert id to numeric if invalid coerce to NaN and rename to original_id
    movies["id"] = pd.to_numeric(movies["id"], errors="coerce")
    movies = movies.rename(columns={"id": "original_id"})

    # normalize to lowercase and no spaces
    movies["title"] = movies["title"].str.lower().str.replace(" ", "")
    movies["original_language"] = movies["original_language"].str.lower().str.replace(" ", "")

    # parse columns with json lists 
    movies["genres"] = movies["genres"].apply(json_col)
    movies["belongs_to_collection"] = movies["belongs_to_collection"].apply(json_col)
    movies["production_companies"] = movies["production_companies"].apply(json_col)

    # convert to integer / replace invalid vals with 0
    movies["popularity"] = pd.to_numeric(movies["popularity"], errors="coerce").fillna(0).astype(int)

    # drop any rows that would violate the db rules
    movies = movies.dropna(subset=["title"])
    return movies

movies = clean_movies(movies)



