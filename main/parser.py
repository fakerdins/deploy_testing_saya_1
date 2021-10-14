import csv
import requests
from bs4 import BeautifulSoup


def get_html(url):
    headers = {"User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}
    response = requests.get(url, headers=headers)
    return response.text


def get_data(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')

    anime_list = soup.find_all('article', {'data-appear_type': 'topic'})
    for anime in anime_list:
        data = {}
        data['title'] = anime.find('a', class_='name').text.strip()
        # print(data['title'])
        data['description'] = anime.find('div', class_='body-inner').text.strip()
        # print(data['description'])
        # write_to_csv(data)
        return data

# def write_to_csv(data):
#     with open('data.csv', 'a') as f:
#         writer = csv.writer(f)
#         writer.writerow([data['title'],data['description']])


def main():
    shiki_url = "https://shikimori.one/forum/news"
    print(get_data(shiki_url))


# with open('data.csv', 'w') as f:
#     writer = csv.writer(f)
#     writer.writerow(['title', 'description'])

