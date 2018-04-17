import pymysql

readArtistData = open("dataQuery/artistDataQuery.txt", 'r')
readAlbumData = open("dataQuery/albumDataQuery.txt", 'r')
readTrackData = open("dataQuery/trackDataQuery.txt", 'r')
artistDatas = readArtistData.readlines()
albumDatas = readAlbumData.readlines()
trackDatas = readTrackData.readlines()
readArtistData.close()
readAlbumData.close()
readTrackData.close()

createBD = pymysql.connect(host="localhost",user="root",password="Hazard10")
cursor = createBD.cursor()

queryCreateBD = 'CREATE DATABASE Musika;'
queryUseBD = 'USE Musika;'
queryCreateTableArtist = 'CREATE TABLE `artist` (`artistId` INT NOT NULL, `artistName` VARCHAR(45) NOT NULL, `artistDescription` MEDIUMTEXT NOT NULL, `artistPhoto` MEDIUMTEXT NOT NULL, PRIMARY KEY (`artistId`));'
queryCreateTableAlbum = 'CREATE TABLE `album` (`albumId` INT NOT NULL, `albumName` VARCHAR(45) NOT NULL, `albumDescription` MEDIUMTEXT NOT NULL, `albumPhoto` MEDIUMTEXT NOT NULL, `albumDateRelease` DATE NOT NULL,`artistId` INT NOT NULL, PRIMARY KEY (`albumId`), INDEX `fk_artistId_idx` (`artistId` ASC), CONSTRAINT `fk_artistId` FOREIGN KEY (`artistId`) REFERENCES `artist` (`artistId`) ON DELETE NO ACTION ON UPDATE NO ACTION);'
queryCreateTableTrack = 'CREATE TABLE `track` (`trackId` INT NOT NULL, `trackName` VARCHAR(45) NOT NULL, `trackDuration` VARCHAR(45) NOT NULL, `albumId` INT NOT NULL, PRIMARY KEY (`trackId`), INDEX `fk_albumId_idx` (`albumId` ASC), CONSTRAINT `fk_albumId` FOREIGN KEY (`albumId`) REFERENCES `album` (`albumId`) ON DELETE NO ACTION ON UPDATE NO ACTION);'
queryCreateTableFavorite = 'CREATE TABLE `favorite` (`userId` INT NOT NULL, `trackId` INT NOT NULL, INDEX `fk_track_idx` (`trackId` ASC), CONSTRAINT `fk_trackId` FOREIGN KEY (`trackId`) REFERENCES `track` (`trackId`) ON DELETE NO ACTION ON UPDATE NO ACTION);'

cursor.execute(queryCreateBD)
cursor.execute(queryUseBD)
cursor.execute(queryCreateTableArtist)
cursor.execute(queryCreateTableAlbum)
cursor.execute(queryCreateTableTrack)
cursor.execute(queryCreateTableFavorite)

queryAddIndexTableArtistName = 'CREATE UNIQUE INDEX artistName_idx ON `artist` (artistName) USING HASH'
queryAddIndexTableAlbumName = 'CREATE UNIQUE INDEX albumName_idx ON `album` (albumName) USING HASH'
queryAddIndexTableTrackName = 'CREATE UNIQUE INDEX trackName_idx ON `track` (trackName) USING HASH'

cursor.execute(queryAddIndexTableArtistName)
cursor.execute(queryAddIndexTableAlbumName)
cursor.execute(queryAddIndexTableTrackName)

cursor.close()
createBD.close()

BD = pymysql.connect(host="localhost", user="root", password="Hazard10", db="Musika")
cursor2 = BD.cursor()

for artistData in artistDatas:
    print(artistData)
    cursor2.execute(str(artistData))
    BD.commit()

for albumData in albumDatas:
    print(albumData)
    cursor2.execute(str(albumData))
    BD.commit()

for trackData in trackDatas:
    print(trackData)
    cursor2.execute(str(trackData))
    BD.commit()

cursor2.close()
BD.close()

createBD2 = pymysql.connect(host="localhost",user="root",password="Hazard10")
cursor3 = createBD2.cursor()

queryCreateBD2 = 'CREATE DATABASE MusikaUsers;'
queryUseBD2 = 'USE MusikaUsers;'
queryCreateTableUser= 'CREATE TABLE `user` (`userId` INT NOT NULL AUTO_INCREMENT, `userEmail` VARCHAR(50) NOT NULL, `userPassword` VARCHAR(100) NOT NULL, PRIMARY KEY (`userId`), `name` VARCHAR(50) NOT NULL );'
queryIndexTableUserEmail = 'CREATE UNIQUE INDEX userEmail_idx ON `user` (userEmail) USING HASH'

cursor3.execute(queryCreateBD2)
cursor3.execute(queryUseBD2)
cursor3.execute(queryCreateTableUser)
cursor3.execute(queryIndexTableUserEmail)

cursor3.close()
createBD2.close()