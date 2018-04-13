from utils import load_json

# albums repository interface
class PlaylistRepository:
    def find_all_playlists(self):
        raise NotImplemented("must be implemented")

    def find_playlist_by_id(self, album_id):
        raise NotImplemented("must be implemented")


class JsonPlaylistRepository(PlaylistRepository):
    def __init__(self, path):
        self.path = path

    def find_all_playlists(self):
        return load_json(self.path)

    def find_playlist_by_id(self, playlist_id):
        playlists = load_json(self.path)
        playlist_to_return = None
        for playlist in playlists:
            if playlist['id'] == playlist_id:
                playlist_to_return = playlist
        return playlist_to_return

