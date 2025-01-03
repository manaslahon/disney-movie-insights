from save_json import load_data_pickle
from dotenv import load_dotenv
import requests
import urllib.parse
import os

load_dotenv()

movie_info_list = load_data_pickle('disney_data_v1.pickle')

def get_omdb_info(title):
    base_url = "http://omdbapi.com/?"
    parameters = {"apikey":os.getenv("OMDB_API_KEY"), "t": title}
    params_encoded = urllib.parse.urlencode(parameters)
    full_url = base_url + params_encoded
    return requests.get(full_url).json()

def get_rotten_tomatoes_score(omdb_info):
    ratings = omdb_info.get("Ratings", [])
    for rating in ratings:
        if rating["Source"] == "Rotten Tomatoes":
            return rating["Value"]
    return None 


