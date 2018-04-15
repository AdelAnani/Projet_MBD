from functools import wraps

import pymysql
from flask import Flask, render_template, flash, redirect, url_for, session, request
from wtforms import Form, StringField, PasswordField, validators

from repository.albums_repository import  SqlAlbumsRepository
from repository.artistes_repository import SQLArtistesRepository
from repository.tracks_repository import SqlTracksRepository
from repository.playlist_repository import JsonPlaylistRepository

from service.albums_service import AlbumsService
from service.artistes_service import ArtistesService
from service.playlist_service import PlaylistService
from service.tracks_service import TracksService

app = Flask(__name__)

DB_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'glo2005',
    'db_name': 'Musika'
}


album_repository = SqlAlbumsRepository(DB_config)
albums_service = AlbumsService(album_repository)

artistes_repository = SQLArtistesRepository(DB_config)
artistes_service = ArtistesService(artistes_repository)

track_repository = SqlTracksRepository(DB_config)
tracks_service = TracksService(track_repository)



playlist_repository = JsonPlaylistRepository("playlist.json")

playlist_service = PlaylistService(playlist_repository)



########################################
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))

    return wrap


#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         # Get Form Fields
#         username = request.form['username']
#         password_candidate = request.form['password']
#
#         # Create cursor
#         cur = mysql.connection.cursor()
#
#         # Get user by username
#         result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
#
#         if result > 0:
#             # Get stored hash
#             data = cur.fetchone()
#             password = data['password']
#
#             # Compare Passwords
#             if sha256_crypt.verify(password_candidate, password):
#                 # Passed
#                 session['logged_in'] = True
#                 session['username'] = username
#
#                 flash('You are now logged in', 'success')
#                 return redirect(url_for('dashboard'))
#             else:
#                 error = 'Invalid login'
#                 return render_template('login.html', error=error)
#             # Close connection
#             cur.close()
#         else:
#             error = 'Username not found'
#             return render_template('login.html', error=error)
#
#     return render_template('login.html')

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.html', Playlists=playlist_service.get_all_playlists())


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/Albums')
def albums():
    return render_template('albums.html', Albums=albums_service.get_all_albums())


@app.route('/albums/<int:id>/')
def albumss(id):
    album_id = id
    try:
        album = albums_service.find_album_by_id(int(album_id))
        return render_template('album.html', album=album)
    except Exception as e:
        print(e)
        return render_template('not_found.html')


@app.route('/albums/search')
def search_by_term():
    name_album = request.args.get('term')
    try:
        return render_template('albums.html', Albums=albums_service.find_album_by_name(str(name_album)))
    except Exception as e:
        print(e)
        return render_template('not_found.html')





@app.route('/Artistes')
def artistess():
    return render_template('artistes.html', Artistes= artistes_service.get_all_artistes())


@app.route('/Artistes/<int:id>/')
def artistesss(id):
    artiste_id = id
    try:
        print(5)
        artist = artistes_service.find_artiste_by_id(int(artiste_id))
        print(artist)
        return render_template('artiste.html', artist= artist)
    except Exception as e:
        print(e)
        return render_template('not_found.html')


@app.route('/tracks')
def chanson():
    return render_template('tracks.html', tracks= tracks_service.get_all_tracks())


class RegisterForm(Form):
    name = StringField('Name', [validators.length(min=1, max=50)])
    username = StringField('Username', [validators.length(min=4, max=25)])
    email = StringField('Email', [validators.length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('confirm Password')


#
# @app.route('/register', methods=['GET','POST'])
# def register():
#     form = RegisterForm(request.form)
#     if request.method == 'POST' and form.validate():
#         name = form.name.data
#         email = form.email.data
#         username = form.username.data
#         password = sha256_crypt.encrypt(str(form.password.data))
#
#         # Create cursor
#         cur = mysql.connection.cursor()
#
#         # Execute query
#         cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)",
#                     (name, email, username, password))
#
#         # Commit to DB
#         mysql.connection.commit()
#
#         # Close connection
#         cur.close()
#
#         flash('You are now registered and can log in', 'success')
#
#         return render_template('not_found.html')
#     return render_template('register.html', form=form)


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
