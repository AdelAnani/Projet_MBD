from utils import load_json
import pymysql

# artisterepository interface
class ArtistesRepository:
    def find_all_artistes(self):
        raise NotImplemented("must be implemented")

    def find_artiste_by_id(self, album_id):
        raise NotImplemented("must be implemented")

class SQLArtistesRepository(ArtistesRepository):

    def __init__(self, config_dict):
        self.host = config_dict['host']
        self.user = config_dict['user']
        self.password = config_dict['password']
        self.db_name = config_dict['db_name']

    def _get_db_connection(self):
        return pymysql.connect(self.host, self.user, self.password, self.db_name)


    def find_all_artistes(self):
        get_all_artists_query = "SELECT * FROM artist"
        connection = self._get_db_connection()
        cursor = connection.cursor()
        cursor.execute(get_all_artists_query)
        all_artistes = cursor.fetchall()
        all_artistes_list = []

        for row in all_artistes:
            all_artistes_list.append({
             'id': row[0],
             'name': row[1],
             'image': row[3],
            })
        cursor.close()
        connection.close()
        return all_artistes_list

    def find_artiste_by_id(self, artiste_id):
        get_artists_by_id_query = "SELECT * FROM artist , album WHERE artist.artistId = %s and artist.artistId = album.artistId  "
        connection = self._get_db_connection()
        cursor = connection.cursor()
        cursor.execute(get_artists_by_id_query, artiste_id)
        artist_data_list = cursor.fetchall()

        artist = {
            'id': artist_data_list[0][0],
            'name': artist_data_list[0][1],
            'description': artist_data_list[0][2],
            'image': artist_data_list[0][3],
            'albums': []
        }

        for row in artist_data_list:
            artist['albums'].append({
                'id': row[4],
                'name': row[5],
                'description': row[6],
                'image': row[7],
                'date_release': row[8],

            })

        cursor.close()
        connection.close()
        return artist

    def find_artiste_by_name(self, artiste_name):
        get_artists_by_name_query = "SELECT * FROM artist, album WHERE artist.artistName = %s and artist.artistId = album.artistId "
        connection = self._get_db_connection()
        cursor = connection.cursor()
        cursor.execute(get_artists_by_name_query, artiste_name)
        artist_data_list = cursor.fetchall()
        if len(artist_data_list)> 0:
            artist = {
                'id': artist_data_list[0][0],
                'name': artist_data_list[0][1],
                'description': artist_data_list[0][2],
                'image': artist_data_list[0][3],
                'albums': []
            }

            for row in artist_data_list:
                artist['albums'].append({
                    'id': row[4],
                    'name': row[5],
                    'description': row[6],
                    'image': row[7],
                    'date_release': row[8],

                })
            connection.close()
        else :
            artist = None
        return artist








# def getCartProduct(idUser):
#     connection = pymysql.connect(user="root", passwd="mysql", host="127.0.0.1", port=3306, database="eShop")
#     cur = connection.cursor()
#     cur.execute("SELECT * FROM products INNER JOIN cart ON products.idProduct = cart.prodId WHERE cart.userId = (%s);",idUser)
#     data = cur.fetchall()
#     productsData = []
#
#     # print(data)
#     for row in data:
#         productsData.append({
#             'idProduct': row[0],
#             'prix': row[1],
#             'description': row[2],
#             'name': row[3],
#             'type': row[4],
#             'image': row[5],
#             'qty': row[6],
#             'idUser': idUser
#         })
#
#     cur.close()
#     connection.close()
#
#     return productsData