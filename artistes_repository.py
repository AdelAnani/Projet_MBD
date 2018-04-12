from utils import load_json

# artisterepository interface
class ArtistesRepository:
    def find_all_artistes(self):
        raise NotImplemented("must be implemented")

    def find_artiste_by_id(self, album_id):
        raise NotImplemented("must be implemented")


class JsonArtistesRepository(ArtistesRepository):
    def __init__(self, path):
        self.path = path

    def find_all_artistes(self):
        return load_json(self.path)

    def find_artiste_by_id(self, artiste_id):
        artistes = load_json(self.path)
        artiste_to_return = None
        for artiste in artistes:
            if artiste['id'] == artiste_id:
                artiste_to_return
        return artiste_to_return

