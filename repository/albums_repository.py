import pymysql

from utils import load_json

# albums repository interface
class AlbumsRepository:
    def find_all_albums(self):
        raise NotImplemented("must be implemented")

    def find_album_by_id(self, album_id):
        raise NotImplemented("must be implemented")


class JsonAlbumsRepository(AlbumsRepository):
    def __init__(self, path):
        self.path = path

    def find_all_albums(self):
        return load_json(self.path)

    def find_album_by_id(self, album_id):
        albums = load_json(self.path)
        album_to_return = None
        for album in albums:
            if album['id'] == album_id:
                album_to_return = album
        return album_to_return


class SqlAlbumsRepository(AlbumsRepository):
    def __init__(self, config_dict):
        self.host = config_dict['host']
        self.user = config_dict['user']
        self.password = config_dict['password']
        self.db_name = config_dict['db_name']

    def _get_db_connection(self):
        return pymysql.connect(self.host, self.user, self.password, self.db_name)

    def find_all_albums(self):
        get_all_artists_query = "SELECT album.albumId, album.albumName, album.albumPhoto, artist.artistName  FROM album, artist WHERE album.artistId = artist.artistId"
        connection = self._get_db_connection()
        cursor = connection.cursor()
        cursor.execute(get_all_artists_query)
        all_albums = cursor.fetchall()
        all_albums_list = []

        for row in all_albums:
            all_albums_list.append({
                'id': row[0],
                'name': row[1],
                'image': row[2],
                'artist': row[3],
            })
        cursor.close()
        connection.close()
        return all_albums_list

    def find_album_by_id(self, album_id):
        getAlbumByIdQuery = "SELECT * FROM album WHERE albumId = %s"
        connection = self._get_db_connection()
        cursor = connection.cursor()
        cursor.execute(getAlbumByIdQuery, id)
        albumData = cursor.fetchone()
        print(albumData)
        album = {
            'id': albumData[0],
            'name': albumData[1],
            'description': albumData[2],
            'image': albumData[3],
            'dateRelease': albumData[4]
        }
        cursor.close()
        connection.close()
        return album
