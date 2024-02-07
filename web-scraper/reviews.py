from imdb import Cinemagoer, IMDbError
from bs4 import BeautifulSoup
import requests
import json
import csv
import time

reviews = {}
ia = Cinemagoer()

def retrieve_titles(filename='top_anime.csv'):
    titles = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            titles.append(row[0])
    return titles

def get_movie_id(title):
    try:
        movie = ia.search_movie(title)
        if movie:
            return movie[0].movieID
        return ""
    except Exception as e:
        print(f"Error getting movie ID for {title}: {e}")
        return ""

def grab_reviews(movie_id):
    url = f"https://www.imdb.com/title/tt{movie_id}/reviews?sort=reviewVolume&dir=desc&ratingFilter=0"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            divs = soup.find_all('div', class_='text show-more__control')
            return [div.get_text() for div in divs]
        else:
            print(f"Failed to fetch reviews for {movie_id}, Status code: {response.status_code}")
    except Exception as e:
        print(f"Error fetching reviews for {movie_id}: {e}")
    return []

def write_reviews(filename='reviews.json'):
    with open(filename, 'w') as file:
        json.dump(reviews, file, indent=4)

def main():
    movie_titles = retrieve_titles()
    with requests.Session() as session:
        for title in movie_titles:
            movie_id = get_movie_id(title)
            if movie_id:
                review_docs = grab_reviews(movie_id)
                if len(review_docs) > 0:
                    reviews[title] = review_docs
                    print(f"{title} completed")
                else:
                    print(f"failed to find reviews for {title}")
    write_reviews()

if __name__ == "__main__":
    main()
