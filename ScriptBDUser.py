import pymysql

createBD = pymysql.connect(host="localhost",user="root",password="glo2005")
cursor = createBD.cursor()

queryCreateBD = 'CREATE DATABASE MusikaUsers;'
queryUseBD = 'USE MusikaUsers;'
queryCreateTableUser= 'CREATE TABLE `user` (`userId` INT NOT NULL AUTO_INCREMENT, `userEmail` VARCHAR(50) NOT NULL, `userPassword` VARCHAR(100) NOT NULL, PRIMARY KEY (`userId`), `name` VARCHAR(50) NOT NULL );'

cursor.execute(queryCreateBD)
cursor.execute(queryUseBD)
cursor.execute(queryCreateTableUser)

cursor.close()
createBD.close()