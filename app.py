from functools import wraps
from passlib.hash import sha256_crypt
import pymysql
from flask import Flask, render_template, flash, redirect, url_for, session, request
from wtforms import Form, StringField, PasswordField, validators

from repository.albums_repository import  SqlAlbumsRepository
from repository.artistes_repository import SQLArtistesRepository
from repository.tracks_repository import SqlTracksRepository
from repository.favorite_repository import SqlFavoriteRepository

from service.albums_service import AlbumsService
from service.artistes_service import ArtistesService
from service.favorite_service import FavoriteService
from service.tracks_service import TracksService

app = Flask(__name__)

print('Entrez votre mot de passe MySQL : ')
password = input()

DB_config = {
    'host': 'localhost',
    'user': 'root',
    'password': password,
    'db_name': 'Musika'
}
DBUsers_config = {
    'host': 'localhost',
    'user': 'root',
    'password': password,
    'db_name': 'MusikaUsers'
}


album_repository = SqlAlbumsRepository(DB_config)
albums_service = AlbumsService(album_repository)
artistes_repository = SQLArtistesRepository(DB_config)
artistes_service = ArtistesService(artistes_repository)
track_repository = SqlTracksRepository(DB_config)
tracks_service = TracksService(track_repository)
favorite_repository = SqlFavoriteRepository(DB_config)
favotite_service = FavoriteService(favorite_repository)

########################################
class RegisterForm(Form):
    name = StringField('Nom', [validators.length(min=4, max=50)])
    email = StringField('Adresse Courriel', [validators.length(min=4, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Les mots de passes ne concordent pas')
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password_candidate = request.form['password']
        connection = pymysql.connect(DBUsers_config['host'], DBUsers_config['user'], DBUsers_config['password'], DBUsers_config['db_name'])
        cur = connection.cursor()
        result = cur.execute("SELECT * FROM user WHERE userEmail = %s", [email])
        if result > 0:
            data = cur.fetchall()
            password = data[0][2]
            name = data[0][3]
            user_id = data [0][0]
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['user_id'] = user_id
                session['email'] = email
                session['name'] = name
                flash('Vous êtes connecté à Musika !', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Informations invalides'
                return render_template('login.html', error=error)
            cur.close()
        else:
            error = 'Email invalide'
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route('/tracks/add_track/<int:id>')
def favorit(id):
    user_id = session["user_id"]
    id_track = id
    connection = pymysql.connect(DB_config['host'], DB_config['user'], DB_config['password'], DB_config['db_name'])
    cur = connection.cursor()
    cur.execute("INSERT INTO favorite(userId, trackId) VALUES(%s, %s)", (user_id, id_track))
    connection.commit()
    cur.close()
    return redirect(url_for('dashboard'))


@app.route('/tracks/delete_track/<int:id>')
def deleteTrackFromFavorite(id):
    user_id = session["user_id"]
    id_track = id
    connection = pymysql.connect(DB_config['host'], DB_config['user'], DB_config['password'], DB_config['db_name'])
    cur = connection.cursor()
    cur.execute("DELETE FROM favorite WHERE userId = %s AND trackId = %s ", (user_id, id_track))
    connection.commit()
    cur.close()
    return redirect(url_for('dashboard'))


@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('Vous êtes déconnecté', 'success')
    return redirect(url_for('login'))


@app.route('/dashboard')
@is_logged_in
def dashboard():
    id_user = session["user_id"]
    track_favorite = favotite_service.get_all_tracks(id_user)
    tracks_id = []
    for track in track_favorite:
        tracks_id.append(track["id_track"])
    track_list = []
    for id in tracks_id:
        track = tracks_service.get_track_by_id(id)
        track_list.append(track[0])
    return render_template('dashboard.html',tracks = track_list)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/Albums')
@is_logged_in
def albums():
    return render_template('albums.html', Albums=albums_service.get_all_albums())


@app.route('/albums/<int:id>/')
@is_logged_in
def albumss(id):
    album_id = id
    try:
        album = albums_service.find_album_by_id(int(album_id))
        return render_template('album.html', album=album)
    except Exception as e:
        redirect(url_for('albums'))


@app.route('/albums/search')
@is_logged_in
def search_album_by_term():
    name_album = request.args.get('term')
    try:
        return render_template('album.html', album=albums_service.find_album_by_name(str(name_album)))
    except Exception as e:
       return  redirect(url_for('albums'))


@app.route('/Artistes')
@is_logged_in
def artistess():
    return render_template('artistes.html', Artistes= artistes_service.get_all_artistes())


@app.route('/Artistes/<int:id>/')
@is_logged_in
def artistesss(id):
    artiste_id = id
    try:
        return render_template('artiste.html', artist= artistes_service.find_artiste_by_id(int(artiste_id)))
    except:
        return  redirect(url_for('artistess'))


@app.route('/Artistes/search')
@is_logged_in
def search_artist_by_term():
    name_artist = request.args.get('term')
    try:
        return render_template('artiste.html', artist= artistes_service.find_artiste_by_name(name_artist))
    except :
        return redirect(url_for('artistess'))


@app.route('/tracks')
@is_logged_in
def chanson():
    return render_template('tracks.html', tracks= tracks_service.get_all_tracks())


@app.route('/tracks/<int:id>/')
@is_logged_in
def search_trsck_by_id(id):
    tack_id = id
    return render_template('track.html', track= tracks_service.get_track_by_id(tack_id))


@app.route('/tracks/search')
@is_logged_in
def search_track_by_term():
    track_name = request.args.get('term')
    try:
        return render_template('track.html', track=tracks_service.get_track_by_name(track_name))
    except:
        return redirect(url_for('chanson'))


@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        connection = pymysql.connect(DBUsers_config['host'], DBUsers_config['user'], DBUsers_config['password'], DBUsers_config['db_name'])
        cur = connection.cursor()
        result = cur.execute("SELECT userEmail FROM  user WHERE userEmail = %s",email)
        connection.commit()
        cur.close()
        if  result > 0 :
             return render_template('register.html', form=form)
        else:
            connection = pymysql.connect(DBUsers_config['host'], DBUsers_config['user'], DBUsers_config['password'],
                                         DBUsers_config['db_name'])
            cur = connection.cursor()
            cur.execute("INSERT INTO user(userEmail, userPassword, name) VALUES(%s, %s,%s)",
                    (email, password, name))
            connection.commit()
            cur.close()
            flash('Bienvenue sur Musika !', 'success')
            return  redirect(url_for('dashboard'))
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
