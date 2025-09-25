
# Install dependencies as needed:
# pip install kagglehub[pandas-datasets]
import kagglehub
from kagglehub import KaggleDatasetAdapter
'''
movies = kagglehub.dataset_load(
  KaggleDatasetAdapter.PANDAS,
  "rounakbanik/the-movies-dataset",
  "movies_metadata.csv", pandas_kwargs={"low_memory": True})
'''
keywords = kagglehub.dataset_load(
  KaggleDatasetAdapter.PANDAS,
  "rounakbanik/the-movies-dataset",
  "keywords.csv", pandas_kwargs={"low_memory": True, "dtype": {"id": int, "keywords": str}})

