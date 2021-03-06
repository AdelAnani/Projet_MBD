import pymysql

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
        get_all_artists_query = "SELECT album.albumId, album.albumName, album.albumPhoto, artist.artistName  FROM album,artistalbum, artist WHERE album.albumId = artistalbum.albumId AND artistalbum.artistId = artist.artistId "
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

        getAlbumByIdQuery = "SELECT *  FROM album,albumtrack, track WHERE album.albumId = albumtrack.albumId AND albumtrack.trackId = track.trackId AND album.albumId = %s "
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

        get_album_by_name_query = "SELECT *  FROM album,albumtrack, track WHERE album.albumId = albumtrack.albumId AND albumtrack.trackId = track.trackId AND album.albumName = %s "
        connection = self._get_db_connection()
        cursor = connection.cursor()
        cursor.execute(get_album_by_name_query, album_name)
        album_data_list = cursor.fetchall()

        if len(album_data_list) > 0:
            album = {
                'id': album_data_list[0][0],
                'name': album_data_list[0][1],
                'description': album_data_list[0][2],
                'image': album_data_list[0][3],
                'dateRelease': album_data_list[0][4],
                'tracks': []
            }

            for track in album_data_list:
                album['tracks'].append({
                    'trackId': track[6],
                    'trackName': track[7],
                    'trackDuration': track[8]
                })
            cursor.close()
            connection.close()
        else:
            album = None
        return album


