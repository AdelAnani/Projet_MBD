class PlaylistService:
    def __init__(self, playlists_repository):
        self.playlist_repository = playlists_repository

    def get_all_playlists(self):
        return self.playlist_repository.find_all_playlists()

    def find_playlist_by_id(self, playlist_id):
        playlist = self.playlist_repository.find_playlist_by_id(playlist_id)

        if playlist is None:
            raise ValueError("playlist not found")
        return playlist
