class TracksService:
    def __init__(self, tracks_repository):
        self.tracks_repository = tracks_repository

    def get_all_tracks(self):
        return self.tracks_repository.find_all_tracks()

    def find_album_by_id(self, track_id):
        track = self.tracks_repository.find_track_by_id(track_id)

        if track is None:
            raise ValueError("album not found")
        return track
