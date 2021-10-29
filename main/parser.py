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

    genius = soup.find('ol', class_='chart-list__elements').text.strip()
    data = []
    res = " ".join(genius.split())
    data.append(res)
    return data


# def write_to_csv(data):
#     with open('data.csv', 'a') as f:
#         writer = csv.writer(f)
#         writer.writerow([data])
#
#

def main():
    genius_url = "https://www.billboard.com/charts/hot-100"
    get_data(genius_url)




# with open('data.csv', 'w') as f:
#     writer = csv.writer(f)
#     writer.writerow()
