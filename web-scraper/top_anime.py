from bs4 import BeautifulSoup
import requests
import csv

def grab_anime():
    url = "https://www.imdb.com/list/ls058654847/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    divs = soup.find_all('a', href=lambda href: href and href.startswith('/title/tt'))
    top_anime = [div.get_text() for div in divs]
    top_anime = [item.strip() for item in top_anime if item.strip() and item != 'See full summary']

    return list(set(top_anime))

def write_anime(top_anime):
    filename = 'top_anime.csv'
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for item in top_anime:
            writer.writerow([item]) 

def main():
    write_anime(grab_anime())

if __name__ == "__main__":
    main()
