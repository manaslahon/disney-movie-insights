from ratings import get_omdb_info, get_rotten_tomatoes_score
from utils.save_json import save_data, load_data
from utils.conversion import money_conversion
from rich.progress import Progress
from datetime import datetime
import pandas as pd


movie_info_list = load_data("../dataset/disney_data.json")
print("Data loaded.")

#Convert runtime to int
def minutes_to_integer(runtime):
    if runtime =="N/A":
        return None
    elif isinstance(runtime, list):
        return int(''.join(filter(str.isdigit, runtime[0])))
    else:
        return int(''.join(filter(str.isdigit, runtime)))

#Convert budget to int
def budget_to_integer(budget):
    if budget == 'N/A':
        return None
    else:
        return money_conversion(budget)


#Convert dates into datetime
dates = [movie.get('Release date', 'N/A') for movie in movie_info_list]

def clean_date(date):
    return date.split("(")[0].strip()

def date_conversion(date):
    if isinstance(date, list):
        date = date[0]
    if date == "N/A":
        return None              
    date_str = clean_date(date)
    print(date_str)
    fmts = ["%B %d, %Y", "%d %B, %Y", "%B %d %Y", "%d %B %Y"]
    for fmt in fmts:
       try:
          return datetime.strptime(date_str, fmt)
       except Exception as e:
          print(e)
    return None


total_size = len(movie_info_list)
with Progress() as progress:
    task = progress.add_task("[cyan]Processing movie data...", total=total_size)

    for movie in movie_info_list: 
        movie["Running Time (int)"] = minutes_to_integer(movie.get("Running time", "N/A"))
        movie['Budget (float)'] = budget_to_integer(movie.get("Budget", "N/A"))
        movie['Box office (float)'] = budget_to_integer(movie.get("Box office", "N/A"))
        movie["Release date (datetime)"] = date_conversion(movie.get("Release date", "N/A"))

        #Update the progress after each movie iteration
        progress.update(task, advance=1)
        #time.sleep(0.1)

#Add IMDB and Rotten Tomatoes score
with Progress() as progress:
    task = progress.add_task("[cyan]Adding OMDB ratings...", total=total_size)

    for movie in movie_info_list: 
        title = movie["title"]
        omdb_info = get_omdb_info(title)
        movie["imdb"] = omdb_info.get("imdbRating", None)
        movie["metascore"] = omdb_info.get("Metascore", None)
        movie["rotten_tomatoes"] = get_rotten_tomatoes_score(omdb_info)

        progress.update(task, advance=1)

#Copy the movie_info_list to convert datetime object back to datetime string
movie_info_copy = [movie.copy() for movie in movie_info_list]
total_size = len(movie_info_copy)
with Progress() as progress:
    task = progress.add_task("[cyan]Converting datetime object -> string...", total=total_size)

    for movie in movie_info_copy:
        current_date = movie["Release date (datetime)"]
        if current_date:
            movie["Release date (datetime)"] = current_date.strftime("%B %d, %Y")
        else:
            movie["Release date (datetime)"] = None

        progress.update(task, advance=1)

#Save data in JSON, CSV and PICKLE format
save_data("disney_final_save_json.json", movie_info_copy)
print("JSON Data saved.")

df = pd.DataFrame(movie_info_list)
df.to_csv("disney_data_csv.csv")
print("CSV Data saved.")
