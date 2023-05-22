import requests

url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjZmQ1M2FlY2QyNzA2ZTk0ODY4MDg1MGQ2ZjU4MTFhNyIsInN1YiI6IjYzZDIwM2NjZmJhNjI1MDA5ZGU5OGQzOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.H_-DEfImhV3nDonoaVeNuu-ya8KT8FxU0wesg-zT0Fg"
}

response = requests.get(url, headers=headers)
data = response.json()

print(data["results"][0]["id"])
print(data["results"][1]["id"])
print(data["results"][2]["id"])
movie_id = [502356,385687,713704]
