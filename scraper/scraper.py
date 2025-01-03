from bs4 import BeautifulSoup as bs 
import requests


def clean_tags(soup):
    for tag in soup.find_all(["sup", "span"]):
        tag.decompose()

def get_list_content(row_data):
    if row_data.find('li'):
        return [li.get_text(' ', strip=True).replace('\xa0', ' ') for li in row_data.find_all('li')]
    elif row_data.find("br"):
        return [text for text in row_data.stripped_strings]
    else:
        return row_data.get_text(' ', strip=True).replace('\xa0', '')

def get_movie_info(url):
    r = requests.get(f"https://en.wikipedia.org/{url}")
    soup = bs(r.content, 'lxml')
    clean_tags(soup)
    info_box = soup.find(class_='infobox vevent')
    info_rows = info_box.find_all('tr')
    movie_info = {} 

    for index, row in enumerate(info_rows):
        if index ==0:
            movie_info['title'] = row.find('th').get_text(' ', strip=True)
        elif index == 1:
            continue
        else:
            header = row.find("th")
            if header:
                content_key = row.find('th').get_text(' ', strip=True)
                content_value = get_list_content(row.find('td'))
                movie_info[content_key] = content_value
    return movie_info

