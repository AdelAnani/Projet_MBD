from repository.albums_repository import AlbumsRepository


class AlbumsService:
    def __init__(self, albums_repository):
        self.albums_repository = albums_repository

    def get_all_albums(self):
        return self.albums_repository.find_all_albums()

    def find_album_by_id(self, album_id):
        album = self.albums_repository.find_album_by_id(album_id)

        if album is None:
            raise ValueError("album not found")
        return album

    def find_album_by_name(self, album_name):
        album = self.albums_repository.find_album_by_name(album_name)
        if album is None:
            raise ValueError("album not found")
        return album




