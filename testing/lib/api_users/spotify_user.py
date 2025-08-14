from lib.api_users.spotify_api import SpotifyAPI

class SpotifyUser():
    def __init__(self):
        self.SpotifyAPI = SpotifyAPI()
        
        self.device = ""
        self.raw_playback = {}
        self.parsed_playback = {}

    def update_data(self) -> bool:
        updated_raw = self.SpotifyAPI.get_playback()
        
        if "Error" in updated_raw:
            self.raw_playback = "Error updating playback"
            self.parsed_playback = {}
            
            return True
        
        if updated_raw == self.raw_playback:
            return False
        
        if updated_raw == "No device playing":
            self.raw_playback = "No device playing"
            self.parsed_playback = {}
            
            return True
        
        self.raw_playback = updated_raw
        self.parsed_playback = self._get_parsed_playback(updated_raw)

        return True

    def _get_parsed_playback(self, raw_data: dict):
        song = raw_data["item"]
        
        song_name = song["name"]
        artist_name = song["artists"][0]["name"]
        album_cover_url = song["album"]["images"][0]["url"]
        
        duration = song["duration_ms"]
        progress_ms = raw_data["progress_ms"]

        progress = float(progress_ms) / duration

        return {
            "song": song_name,
            "artist": artist_name,
            "album_cover_url": album_cover_url,
            "progress": progress
        }

    def alter_playback(self):
        pass

