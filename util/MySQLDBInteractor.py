import pymysql

class MySQLDBInteractor:
    def __init__(self):
        self.connection = pymysql.connect(host="localhost", user="root", password="Hazard10", db="Musika")
        self.cursor = self.connection.cursor()

    def select(self, sql):
        self.cursor.execute(sql)
        sel = self.cursor.fetchone()
        self.cursor.close()
        self.connection.close()
        return sel

    def update(self, sql):
        self.cursor.execute(sql)
        upd = self.connection.commit()
        self.cursor.close()
        self.connection.close()
        return upd