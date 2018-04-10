class TracksService:
    def __init__(self, tracks_repository):
        self.tracks_repository = tracks_repository

    def get_all_tracks(self):
        return self.tracks_repository.find_all_albums()

    def find_album_by_id(self, album_id):
        track = self.tracks_repository.find_album_by_id(album_id)

        if track is None:
            raise ValueError("album not found")
        return track
