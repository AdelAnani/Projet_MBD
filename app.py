from flask import Flask, render_template, flash, redirect, url_for, session, logging
from albums import albums
app = Flask(__name__)

albums = albums()

# Index
# @app.route('/Albums', methods = ['GET'])
# def getAllAlbums():
#     return albumsService.getAllAlbums()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/Albums')
def products():
    return render_template('albums.html', Albums = albums)


@app.route('/Albums/<string:id>/')
def article(id):
    id = request.args.get('id')
    return render_template('album.html', id = id)

if __name__ == '__main__':
	app.run(debug=True)