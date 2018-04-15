from utils import load_json
import pymysql

# artisterepository interface
class ArtistesRepository:
    def find_all_artistes(self):
        raise NotImplemented("must be implemented")

    def find_artiste_by_id(self, album_id):
        raise NotImplemented("must be implemented")

class SQLArtistesRepository(ArtistesRepository):

    getAllArtistsQuery = "SELECT * FROM artist"
    getArtistById = "SELECT * FROM artist WHERE albumId = 1"

    def __init__(self):
        self.connection = pymysql.connect(host="localhost", user="root", password="Hazard10", db="Musika")

    def find_all_artistes(self):
        getAllArtistsQuery = "SELECT * FROM artist"
        self.cursor = self.connection.cursor()
        self.cursor.execute(getAllArtistsQuery)
        allArtistes = self.cursor.fetchall()
        allArtistesList = []
        print(allArtistes)
        for row in allArtistes:
            allArtistesList.append({
             'id': row[0],
             'name': row[1],
             'image': row[3],
            })
        self.cursor.close()
        self.connection.close()
        return allArtistesList

    def find_artiste_by_id(self, artiste_id):
        self.artiste = MySQLDBInteractor.select(artisteQuery)
        return self.artiste

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