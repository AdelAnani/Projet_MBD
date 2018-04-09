from utils import load_json

# albums repository interface
class AlbumsRepository:
    def find_all_albums(self):
        raise NotImplemented("must be implemented")

    def find_album_by_id(self, album_id):
        raise NotImplemented("must be implemented")


class JsonAlbumsRepository(AlbumsRepository):
    def __init__(self, path):
        self.path = path

    def find_all_albums(self):
        return load_json(self.path)

    def find_album_by_id(self, album_id):
        albums = load_json(self.path)
        album_to_return = None
        for album in albums:
            if album['id'] == album_id:
                album_to_return = album
        return album_to_return

