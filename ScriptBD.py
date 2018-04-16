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

createBD = pymysql.connect(host="localhost",user="root",password="glo2005")
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

cursor.close()
createBD.close()

BD = pymysql.connect(host="localhost", user="root", password="glo2005", db="Musika")
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
