class TracksService:
    def __init__(self, tracks_repository):
        self.tracks_repository = tracks_repository

    def get_all_tracks(self):
        return self.tracks_repository.find_all_tracks()

    def get_track_by_id(self, track_id):
        track = self.tracks_repository.find_track_by_id(track_id)

        if track is None:
            raise ValueError("album not found")
        return track
    def get_track_by_name(self, track_name):
        track = self.tracks_repository.find_track_by_name(track_name)
        if track is None:
            raise ValueError("track not found")
        return track

