class FavoriteService:
    def __init__(self, favorite_repository):
        self.favorite_repository = favorite_repository

    def get_all_tracks(self,id_user):
        return self.favorite_repository.find_all_tracks(id_user)

