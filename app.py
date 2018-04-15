from flask import Flask, render_template, flash, redirect, url_for,session,logging,request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from repository.albums_repository import JsonAlbumsRepository
from service.albums_service import AlbumsService
from repository.tracks_repository import  JsonTrackRepository
from service.tracks_service import TracksService
from functools import wraps
from repository.playlist_repository import JsonPlaylistRepository
from service.playlist_service import PlaylistService
from repository.artistes_repository import SQLArtistesRepository
from service.artistes_service import ArtistesService
import pymysql

app = Flask(__name__)

musikaDB =("localhost","root","Hazard10","Musika")
#userDB =("localhost","root","1234","users")

def connectionMusika():
    connect= pymysql.connect(musikaDB[0],musikaDB[1],musikaDB[2],musikaDB[3])
    return connect

def find_all_artists():
    getAllArtistsQuery = "SELECT * FROM artist"
    connectionMusika()
    cursor = connectionMusika().cursor()
    cursor.execute(getAllArtistsQuery)
    allArtistesData = cursor.fetchall()
    allArtistes = []
    for row in allArtistesData:
        allArtistes.append({
            'id': row[0],
            'name': row[1],
            'image': row[3],
        })
    cursor.close()
    connectionMusika().close()
    return allArtistes

def find_artist_by_id(id):
    getAllArtistsQuery = "SELECT * FROM artist WHERE artistId = %s"
    connectionMusika()
    cursor = connectionMusika().cursor()
    cursor.execute(getAllArtistsQuery, id)
    artistData = cursor.fetchone()
    print(artistData)
    artist = {
        'id': artistData[0],
        'name': artistData[1],
        'description': artistData[2],
        'image': artistData[3]
    }
    cursor.close()
    connectionMusika().close()
    return artist

def find_all_albums():
    getAllArtistsQuery = "SELECT album.albumId, album.albumName, album.albumPhoto, artist.artistName  FROM album, artist WHERE album.artistId = artist.artistId"
    connectionMusika()
    cursor = connectionMusika().cursor()
    cursor.execute(getAllArtistsQuery)
    allAlbums = cursor.fetchall()
    allAlbumsList = []
    print(allAlbums)
    for row in allAlbums:
        allAlbumsList.append({
            'id': row[0],
            'name': row[1],
            'image': row[2],
            'artist': row[3],
        })
    cursor.close()
    connectionMusika().close()
    return allAlbumsList

def find_album_by_id(id):
    getAlbumByIdQuery = "SELECT * FROM album WHERE albumId = %s"
    connectionMusika()
    cursor = connectionMusika().cursor()
    cursor.execute(getAlbumByIdQuery, id)
    albumData = cursor.fetchone()
    print(albumData)
    album = {
        'id': albumData[0],
        'name': albumData[1],
        'description': albumData[2],
        'image': albumData[3],
        'dateRelease':albumData[4]
    }
    cursor.close()
    connectionMusika().close()
    return album

def find_all_tracks():
    # getAllArtistsQuery = "SELECT * FROM track"
    # connectionMusika()
    # cursor = connectionMusika().cursor()
    # cursor.execute(getAllArtistsQuery)
    # allArtistes = cursor.fetchall()
    # allArtistesList = []
    # print(allArtistes)
    # for row in allArtistes:
    #     allArtistesList.append({
    #         'id': row[0],
    #         'name': row[1],
    #         'image': row[3],
    #     })
    # cursor.close()
    # connectionMusika().close()
    return allArtistesList

album_repository = JsonAlbumsRepository("albums.json")
albums_service = AlbumsService(album_repository)
tracks_repository = JsonAlbumsRepository("tracks.json")
tracks_service = TracksService(tracks_repository)
playlist_repository = JsonPlaylistRepository("playlist.json")
playlist_service = PlaylistService(playlist_repository)
artistes_repository = SQLArtistesRepository()
artistes_service = ArtistesService(artistes_repository )



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
    return render_template('dashboard.html', Playlists= playlist_service.get_all_playlists())



@app.route('/')
def index():
    return render_template('home.html')


@app.route('/Albums')
def products():
    return render_template('albums.html', Albums=find_all_albums())


@app.route('/albums/<int:id>/')
def albumss(id):
    album_id = id
    try:
        album = find_album_by_id(int(album_id))
        return render_template('album.html', album = album)
    except:
        return render_template('not_found.html')

@app.route('/Artistes')

def artistess ():
    return render_template('artistes.html', Artistes = find_all_artists())

@app.route('/Artistes/<int:id>/')
def artistesss(id):
    artiste_id = id
    try:
        artist = find_artist_by_id(int(artiste_id))
        return render_template('artiste.html', artiste = artist )
    except:
        return render_template('not_found.html')



@app.route('/tracks')
@is_logged_in
def chanson():
    return render_template('tracks.html', tracks= tracks_service.get_all_tracks())


class RegisterForm(Form):

    name = StringField ('Name',[validators.length(min=1, max=50)])
    username = StringField('Username', [validators.length(min=4, max=25)])
    email = StringField('Email', [validators.length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message= 'Passwords do not match')
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

