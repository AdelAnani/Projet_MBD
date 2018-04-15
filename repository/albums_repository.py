import pymysql

from utils import load_json

# albums repository interface
class AlbumsRepository:
    def find_all_albums(self):
        raise NotImplemented("must be implemented")

    def find_album_by_id(self, album_id):
        raise NotImplemented("must be implemented")

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

        getAlbumByIdQuery = "SELECT * FROM album, track WHERE album.albumId = %s and track.albumId = album.albumId"
        connection = self._get_db_connection()
        cursor = connection.cursor()
        cursor.execute(getAlbumByIdQuery, album_id)
        albumData_list = cursor.fetchall()

        album = {
            'id': albumData_list[0][0],
            'name': albumData_list[0][1],
            'description': albumData_list[0][2],
            'image': albumData_list[0][3],
            'dateRelease': albumData_list[0][4],
            'tracks': []
        }

        for track in   albumData_list:
            album['tracks'].append({
                'trackId': track[6],
                'trackName': track[7],
                'trackDuration': track[8]
            })

        cursor.close()
        connection.close()
        return album
    def find_album_by_name (self, album_name):

        getAlbumByIdQuery = "SELECT * FROM album WHERE albumName = %s"
        connection = self._get_db_connection()
        cursor = connection.cursor()
        cursor.execute(getAlbumByIdQuery, album_name)
        albumData_list = cursor.fetchall()
        if albumData_list > 0 :
            album = {
                'id': albumData_list[0],
                'name': albumData_list[1],
                'description': albumData_list[2],
                'image': albumData_list[3],
                'tracks': []
            }
            cursor.close()
            connection.close()

        else :
            album = None
        return album


