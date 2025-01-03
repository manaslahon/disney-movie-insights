from scraper.utils.save_json import save_data
from scraper.scraper import get_movie_info
from bs4 import BeautifulSoup as bs
from termcolor import colored
import subprocess
import requests

r = requests.get('https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films')
soup = bs(r.content, 'lxml')
movies = soup.select('.wikitable.sortable i a')

movie_info_list = []
print(colored("⏳Collecting data...", "green"))
for index, movie in enumerate(movies):
    try:
        relative_path = movie['href']
        title = movie['title']
        movie_info_list.append(get_movie_info(relative_path))
    except Exception as e:
        print(colored(f"❌{e}", "red"))
        print(colored(f"⚠️ {movie.get_text()}", "yellow"))

print(colored("📊 Data collected.", "green"))
save_data('disney_data.json', movie_info_list)
print(colored("📥 Data saved successfully.", "green"))

print(colored("Cleaning data >=", "green"))
subprocess.run(["python", "scraper/clean_data.py"], check=True)
print(colored("Running Streamlit >=", "green"))
subprocess.run(["streamlit", "run", "visualization/visualization.py"], check=True)

