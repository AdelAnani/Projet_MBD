import pymysql

readArtistData = open("dataQuery/artistDataQuery.txt", 'r')
readAlbumData = open("dataQuery/albumDataQuery.txt", 'r')
readTrackData = open("dataQuery/trackDataQuery.txt", 'r')
readArtistAlbumData = open("dataQuery/artistAlbumDataQuery.txt", 'r')
readArtistTrackData = open("dataQuery/artistTrackDataQuery.txt", 'r')
readAlbumTrackData = open("dataQuery/albumTrackDataQuery.txt", 'r')
artistDatas = readArtistData.readlines()
albumDatas = readAlbumData.readlines()
trackDatas = readTrackData.readlines()
artistAlbumDatas = readArtistAlbumData.readlines()
artistTrackDatas = readArtistTrackData.readlines()
albumTrackDatas = readAlbumTrackData.readlines()
readArtistData.close()
readAlbumData.close()
readTrackData.close()
readArtistAlbumData.close()
readArtistTrackData.close()
readAlbumTrackData.close()

DB_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'glo2005',
}

createBD = pymysql.connect(host= DB_config ['host'] ,user= DB_config ['user'],password= DB_config['password'])
cursor = createBD.cursor()

queryCreateBD = 'CREATE DATABASE Musika;'
queryUseBD = 'USE Musika;'
queryCreateTableArtist = 'CREATE TABLE `artist` (`artistId` INT NOT NULL, `artistName` VARCHAR(45) NOT NULL, `artistDescription` MEDIUMTEXT NOT NULL, `artistPhoto` MEDIUMTEXT NOT NULL, PRIMARY KEY (`artistId`));'
queryCreateTableAlbum = 'CREATE TABLE `album` (`albumId` INT NOT NULL, `albumName` VARCHAR(45) NOT NULL, `albumDescription` MEDIUMTEXT NOT NULL, `albumPhoto` MEDIUMTEXT NOT NULL, PRIMARY KEY (`albumId`));'
queryCreateTableTrack = 'CREATE TABLE `track` (`trackId` INT NOT NULL, `trackName` VARCHAR(45) NOT NULL, `trackDuration` VARCHAR(45) NOT NULL, PRIMARY KEY (`trackId`));'
queryCreateTableFavorite = 'CREATE TABLE `favorite` (`userId` INT NOT NULL, `trackId` INT NOT NULL, INDEX `fk_track_idx` (`trackId` ASC), CONSTRAINT `fk_trackId` FOREIGN KEY (`trackId`) REFERENCES `track` (`trackId`) ON DELETE NO ACTION ON UPDATE NO ACTION);'
queryCreateTableArtistAlbum = 'CREATE TABLE `artistAlbum` (`artistId` INT NOT NULL, `albumId` INT NOT NULL, INDEX `fk_artistId_idx` (`artistId` ASC), INDEX `fk_albumId_idx` (`albumId` ASC), CONSTRAINT `fk_artistId` FOREIGN KEY (`artistId`) REFERENCES `artist` (`artistId`) ON DELETE NO ACTION ON UPDATE NO ACTION, CONSTRAINT `fk_albumId` FOREIGN KEY (`albumId`) REFERENCES `album` (`albumId`) ON DELETE NO ACTION ON UPDATE NO ACTION);'
queryCreateTableArtistTrack = 'CREATE TABLE `artistTrack` (`artistId` INT NOT NULL, `trackId` INT NOT NULL, INDEX `fk_artistId2_idx` (`artistId` ASC), INDEX `fk_trackId2_idx` (`trackId` ASC), CONSTRAINT `fk_artistId2` FOREIGN KEY (`artistId`) REFERENCES `artist` (`artistId`) ON DELETE NO ACTION ON UPDATE NO ACTION, CONSTRAINT `fk_trackId2` FOREIGN KEY (`trackId`) REFERENCES `track` (`trackId`) ON DELETE NO ACTION ON UPDATE NO ACTION);'
queryCreateTableAlbumTrack = 'CREATE TABLE `albumTrack` (`albumId` INT NOT NULL, `trackId` INT NOT NULL, INDEX `fk_albumId2_idx` (`albumId` ASC), INDEX `fk_trackId3_idx` (`trackId` ASC), CONSTRAINT `fk_albumId2` FOREIGN KEY (`albumId`) REFERENCES `album` (`albumId`) ON DELETE NO ACTION ON UPDATE NO ACTION, CONSTRAINT `fk_trackId3` FOREIGN KEY (`trackId`) REFERENCES `track` (`trackId`) ON DELETE NO ACTION ON UPDATE NO ACTION);'

cursor.execute(queryCreateBD)
cursor.execute(queryUseBD)
cursor.execute(queryCreateTableArtist)
cursor.execute(queryCreateTableAlbum)
cursor.execute(queryCreateTableTrack)
cursor.execute(queryCreateTableFavorite)
cursor.execute(queryCreateTableArtistAlbum)
cursor.execute(queryCreateTableArtistTrack)
cursor.execute(queryCreateTableAlbumTrack)

queryAddIndexTableArtistName = 'CREATE INDEX artistName_idx ON `artist` (artistName) USING HASH'
queryAddIndexTableAlbumName = 'CREATE INDEX albumName_idx ON `album` (albumName) USING HASH'
queryAddIndexTableTrackName = 'CREATE INDEX trackName_idx ON `track` (trackName) USING HASH'
queryAddIndexTablealbumtrack = 'CREATE INDEX trackAlbum_idx ON `albumtrack` (albumId,trackId) USING HASH'
queryAddIndexTartistalbum = 'CREATE INDEX trackAlbum_idx ON `artistalbum` (artistId,albumId) USING HASH'

cursor.execute(queryAddIndexTableArtistName)
cursor.execute(queryAddIndexTableAlbumName)
cursor.execute(queryAddIndexTableTrackName)
cursor.execute(queryAddIndexTablealbumtrack)
cursor.execute(queryAddIndexTartistalbum)
cursor.close()
createBD.close()

BD = pymysql.connect(host= DB_config ['host'] ,user= DB_config ['user'],password= DB_config['password'])
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

for artistAlbumData in artistAlbumDatas:
    print(artistAlbumData)
    cursor2.execute(str(artistAlbumData))
    BD.commit()

for artistTrackData in artistTrackDatas:
    print(artistTrackData)
    cursor2.execute(str(artistTrackData))
    BD.commit()

for albumTrackData in albumTrackDatas:
    print(albumTrackData)
    cursor2.execute(str(albumTrackData))
    BD.commit()

cursor2.close()
BD.close()

createBD2 = pymysql.connect(host= DB_config ['host'] ,user= DB_config ['user'],password= DB_config['password'])
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