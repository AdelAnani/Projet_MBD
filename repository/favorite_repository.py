import pymysql

from utils import load_json

# albums repository interface
class FavoriteRepository:
    def find_all_tracks(self):
        raise NotImplemented("must be implemented")


class SqlFavoriteRepository(FavoriteRepository):
    def __init__(self, config_dict):
        self.host = config_dict['host']
        self.user = config_dict['user']
        self.password = config_dict['password']
        self.db_name = config_dict['db_name']

    def _get_db_connection(self):
        return pymysql.connect(self.host, self.user, self.password, self.db_name)

    def find_all_tracks(self,userID):
        get_all_artists_query = "SELECT * FROM favorite WHERE favorite.userId = %s "
        connection = self._get_db_connection()
        cursor = connection.cursor()
        cursor.execute ((get_all_artists_query),userID)
        all_tracks = cursor.fetchall()
        all_tracks_list = []

        for row in all_tracks:
            all_tracks_list.append({
                'id_user': row[0],
                'id_track': row[1],
            })
        cursor.close()
        connection.close()
        return all_tracks_list




