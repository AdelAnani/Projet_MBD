import pymysql

# artisterepository interface
class TracksRepository:
    def find_all_tracks(self):
        raise NotImplemented("must be implemented")

    def find_tracks_by_id(self, album_id):
        raise NotImplemented("must be implemented")

class SqlTracksRepository(TracksRepository):
    def __init__(self, config_dict):
        self.host = config_dict['host']
        self.user = config_dict['user']
        self.password = config_dict['password']
        self.db_name = config_dict['db_name']

    def _get_db_connection(self):
        return pymysql.connect(self.host, self.user, self.password, self.db_name)

    def find_all_tracks(self,):
        get_all_tracks_query = "SELECT * FROM track"
        connection = self._get_db_connection()
        cursor = connection.cursor()
        cursor.execute(get_all_tracks_query)
        all_tracks = cursor.fetchall()
        all_tracks_list = []
        for row in all_tracks:
            all_tracks_list.append({
             'id': row[0],
             'name': row[1],
             'duration': row[2],
             'id_album': row[3]
            })
        cursor.close()
        connection.close()
        return all_tracks_list

    def find_tracks_by_id(self, track_id):
        get_track_by_id_query = "SELECT * FROM track WHERE trackId = %s"
        connection = self._get_db_connection()
        cursor = connection.cursor()
        cursor.execute(get_track_by_id_query, track_id)
        tracks_data_list = cursor.fetchall()
        list_tracks_id = []
        for row in tracks_data_list :
            list_tracks_id.append({
                'id': row[0],
                'name': row[1],
                'duration': row[2],
                'id_album': row[3]
                })

        cursor.close()
        connection.close()
        return list_tracks_id
