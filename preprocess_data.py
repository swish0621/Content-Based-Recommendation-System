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

# create new CountVectorizer obj
vectorizer = CountVectorizer()

# create another column "key_space_sep" with list item keywords converted to space separated strings 
keywords["key_space_sep"] = keywords["keyword_lists"].apply(lambda x: " ".join(x))

# create the vectorized matrix 
keyword_matrix = vectorizer.fit_transform(keywords["key_space_sep"])


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

# for use on columns of metadata include json strings 
def json_col(col):
    try:
        if pd.isna(col) or col == "":
            return []
        try:
            metadata = json.loads(col)
        except json.JSONDecodeError:
            metadata = ast.literal_eval(col)

        if isinstance(metadata, list):
            return [item.get("name", "").lower().replace(" ", "") for item in metadata if "name" in item]
        elif isinstance(metadata, dict) and "name" in metadata:
            return [metadata["name"].lower().replace(" ", "")]
        else:
            return []
    except (ValueError, TypeError, SyntaxError):
        return []
            
def clean_movies(movies):
    movies["id"] = pd.to_numeric(movies["id"], errors="coerce")
    movies["title"] = movies["title"].str.lower().str.replace(" ", "")
    movies["genres"] = movies["genres"].apply(json_col)
    movies["belongs_to_collection"] = movies["belongs_to_collection"].apply(json_col)
    movies["original_language"] = movies["original_language"].str.lower().str.replace(" ", "")
    movies["popularity"] = pd.to_numeric(movies["popularity"], errors="coerce").fillna(0).astype(int)
    movies["production_companies"] = movies["production_companies"].apply(json_col)

    return movies

movies = clean_movies(movies)
print(movies.head(5))


