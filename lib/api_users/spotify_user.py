from typing import Dict

from lib.api_users.spotify_api import SpotifyAPI

class SpotifyUser():
    def __init__(self):
        self.SpotifyAPI = SpotifyAPI()
        
        self.device = ""
        self.raw_playback = {}
        self.parsed_playback = {}

    def update_data(self) -> int:
        updated_raw = self.SpotifyAPI.get_playback()
        
        if "Error" in updated_raw:
            self.raw_playback = "Error updating playback"
            self.parsed_playback = {}
            
            return 400
        
        if updated_raw == "No device playing":
            self.raw_playback = "No device playing"
            self.parsed_playback = {}
            
            return 204
        
        if updated_raw == self.raw_playback:
            return 200

        self.raw_playback = updated_raw
        parsed_playback = self._get_parsed_playback(updated_raw) #type: ignore
        
        if self._song_changed(parsed_playback):
            self.parsed_playback = parsed_playback
            return 202
        
        else: 
            self.parsed_playback = parsed_playback
            return 201

    def _get_parsed_playback(self, raw_data: Dict[str, Dict]):
        song = raw_data["item"]
        
        song_name = song["name"]
        artist_name = song["artists"][0]["name"]
        album_cover_url = song["album"]["images"][0]["url"]
        
        duration = int(song["duration_ms"])
        progress_ms: str = raw_data["progress_ms"] #type: ignore

        progress = float(progress_ms) / duration

        return {
            "song": song_name,
            "artist": artist_name,
            "album_cover_url": album_cover_url,
            "progress": progress
        }

    def alter_playback(self):
        pass

    def _song_changed(self, parsed_playback: dict) -> bool:
        return self.parsed_playback == {} or self.parsed_playback["song"] != parsed_playback["song"]

