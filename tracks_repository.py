from utils import load_json

# albums repository interface
class TracksRepository:
    def find_all_tracks(self):
        raise NotImplemented("must be implemented")

    def find_track_by_id(self, track_id):
        raise NotImplemented("must be implemented")


class JsonTrackRepository(TracksRepository):
    def __init__(self, path):
        self.path = path

    def find_all_tracks(self):
        return load_json(self.path)

    def find_album_by_id(self, track_id):
        tracks = load_json(self.path)
        tracks_to_return = None
        for track in tracks:
            if track['id'] == track_id:
                tracks_to_return = track
        return tracks_to_return

