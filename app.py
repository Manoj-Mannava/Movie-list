from flask import Flask, render_template, request, jsonify
import urllib.request
from urllib.parse import quote
import json

app = Flask(__name__)

# Dummy storage for playlists (you can use a database for persistence)
playlists = {"default": []}

@app.route('/', methods=['GET', 'POST'])
def home():
    movies_data = None
    if request.method == 'POST':
        query = request.form.get('query')
        encoded_query = quote(query)
        with urllib.request.urlopen(f"https://api.watchmode.com/v1/autocomplete-search/?apiKey=TIX0aWcg37iGhy9i7RVpr54tcTKsKf01cCkmXMNX&search_value="+encoded_query+"&search_type=1") as url:
            movies_data = json.loads(url.read().decode())
            # Ensure each movie has an 'image_url'
            for movie in movies_data.get('results', []):
                if 'image_url' not in movie:
                    movie['image_url'] = 'default_image_url_here'  # Replace with actual default image URL if necessary
    return render_template('home.html', movies_data=movies_data)

@app.route('/add_to_playlist', methods=['POST'])
def add_to_playlist():
    movie = request.json.get('movie')
    playlist_name = request.json.get('playlist', 'default')
    if playlist_name not in playlists:
        playlists[playlist_name] = []
    playlists[playlist_name].append(movie)
    return jsonify({"message": "Movie added to playlist", "playlist": playlists[playlist_name]})

@app.route('/playlists/<playlist_name>', methods=['GET'])
def get_playlist(playlist_name):
    playlist = playlists.get(playlist_name, [])
    return render_template('playlist.html', playlist_name=playlist_name, playlist=playlist)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
