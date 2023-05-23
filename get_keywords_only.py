import os
import django
import requests
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
django.setup()

from movies.models import Movie
import requests
import json

lst = []


def get_keywords_data():
    for i in range(1, 5):
        request_url = f"https://api.themoviedb.org/3/movie/popular?api_key=cfd53aecd2706e948680850d6f5811a7&language=ko-KR&page={i}"
        movies = requests.get(request_url).json()
        for movie in movies["results"]:
            movie_id = movie["id"]
            url = f"https://api.themoviedb.org/3/movie/{movie_id}/keywords"
            headers = {
                "accept": "application/json",
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjZmQ1M2FlY2QyNzA2ZTk0ODY4MDg1MGQ2ZjU4MTFhNyIsInN1YiI6IjYzZDIwM2NjZmJhNjI1MDA5ZGU5OGQzOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.H_-DEfImhV3nDonoaVeNuu-ya8KT8FxU0wesg-zT0Fg",
            }
            response = requests.get(url, headers=headers).json()
            keywords = response.get("keywords", [])
            movie_keywords = {
                "movie_id": movie_id,
                "keywords": [keyword.get("id") for keyword in keywords],
            }
            lst.append(movie_keywords)
            print(movie_keywords)

    with open("movies_keywords.json", "w", encoding="utf-8") as w:
        json.dump(lst, w, indent="\t", ensure_ascii=False)


get_keywords_data()
