class FavoritesRepository:
    def add_track_to_favorites(self, username, track_id):
        raise NotImplemented("FavoritesRepository: add_track_to_favorites")


class JsonFavoritesRepository(FavoritesRepository):
    def add_track_to_favorites(self, username, track_id):
        pass
