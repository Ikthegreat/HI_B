import os
import requests
import json

def get_nowplaying_movie_datas():
    total_data = []

    for i in range(1, 3):
        request_url = f"https://api.themoviedb.org/3/movie/now_playing?api_key=cfd53aecd2706e948680850d6f5811a7&language=ko-KR&page={i}"

        movies = requests.get(request_url).json()
        print(movies)
        for movie in movies['results']:
            if movie.get('release_date', ''):
                fields = {
                    'movie_id': movie['id'],
                    'title': movie['title'],
                    'released_date': movie['release_date'],
                    'vote_average': movie['vote_average'],
                    'overview': movie['overview'],
                    'poster_path': movie['poster_path'],
                }

                data = {
                    "pk": movie['id'],
                    "model": "movies.nowplaying_movie",
                    "fields": fields
                }

                total_data.append(data)

    with open("nowplaying_movies.json", "w", encoding="utf-8") as w:
        json.dump(total_data, w, indent="\t", ensure_ascii=False)

get_nowplaying_movie_datas()
