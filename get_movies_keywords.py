import json
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
django.setup()

from movies.models import Movie, Keyword

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
django.setup()
def import_movie_keywords():
    with open("movies_keywords.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        movie_id = item["movie_id"]
        keyword_ids = item["keywords"]
        
        try:
            movie = Movie.objects.get(movie_id=movie_id)
        except Movie.DoesNotExist:
            continue

        for keyword_id in keyword_ids:
            try:
                keyword = Keyword.objects.get(keyword_id=keyword_id)
                movie.keywords.add(keyword)
            except Keyword.DoesNotExist:
                continue

import_movie_keywords()
