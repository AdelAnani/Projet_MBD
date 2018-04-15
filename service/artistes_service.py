from repository.albums_repository import AlbumsRepository


class ArtistesService:
    def __init__(self, artiste_repository):
        self.artiste_repository = artiste_repository

    def get_all_artistes(self):
        return self.artiste_repository.find_all_artistes()

    def find_artiste_by_id(self, artiste_id):
        artiste = self.artiste_repository.find_artiste_by_id(artiste_id)

        if artiste is None:
            raise ValueError("artiste not found")
        return artiste




