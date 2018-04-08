from flask import Flask, render_template

from albums_repository import JsonAlbumsRepository
from albums_service import AlbumsService

app = Flask(__name__)

# dependencies injection #
album_repository = JsonAlbumsRepository("albums.json")
albums_service = AlbumsService(album_repository)
########################################


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/Albums')
def products():
    return render_template('albums.html', Albums=albums_service.get_all_albums())


@app.route('/albums/<int:id>/')
def article(id):
    album_id = id
    try:
        album = albums_service.find_album_by_id(album_id)
        return render_template('album.html', album=album)
    except:
        return render_template('not_found.html')


if __name__ == '__main__':
    app.run(debug=True)
