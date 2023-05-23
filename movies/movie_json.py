import os
import requests
import json


def get_movie_datas():
    total_data = []

    for i in range(1, 5):
        request_url = f"https://api.themoviedb.org/3/movie/popular?api_key=cfd53aecd2706e948680850d6f5811a7&language=ko-KR&page={i}"
        print(request_url)
        movies = requests.get(request_url).json()
        for movie in movies["results"]:
            url = f"https://api.themoviedb.org/3/movie/{movie['id']}/keywords?api_key=cfd53aecd2706e948680850d6f5811a7"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                keywords = data["keywords"]
                keyword_list = [keyword["id"] for keyword in keywords]
            if movie.get("release_date", ""):
                fields = {
                    "movie_id": movie["id"],
                    "title": movie["title"],
                    "released_date": movie["release_date"],
                    "vote_average": movie["vote_average"],
                    "overview": movie["overview"],
                    "poster_path": movie["poster_path"],
                    "keywords": keyword_list,
                }

                data = {"pk": movie["id"], "model": "movies.movie", "fields": fields}

                total_data.append(data)

    with open("movies_test.json", "w", encoding="utf-8") as w:
        json.dump(total_data, w, indent="\t", ensure_ascii=False)


get_movie_datas()
