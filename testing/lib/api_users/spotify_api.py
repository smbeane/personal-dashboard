import requests
import base64
from typing import Dict

from lib.spotify_secrets import CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN

TOKEN_URL = "https://accounts.spotify.com/api/token"
PLAYBACK_URL = "https://api.spotify.com/v1/me/player"

class SpotifyAPI():
    def __init__(self):
        self.refresh_token = REFRESH_TOKEN
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.access_token = self._get_access_token()

    def get_playback(self) -> Dict[str, str] | str:
        headers = {"Authorization": "Bearer " + self.access_token}

        response = requests.get(url=PLAYBACK_URL, headers=headers)
        response_status = response.status_code

        if response_status == 200:
            return response.json()
        
        elif response_status == 204:
            return "No device playing"
        
        elif response_status == 401:
            access_token = self._get_access_token()
            if "Error" in access_token:
                return "Error: can't recieve access token"
            else: 
                self.access_token = access_token
                return self.get_playback()
            
        else:
            return "Error " + str(response_status)

    def alter_playback(self, alteration_type: str):
        pass

    def _get_access_token(self) -> str:
        encoded_client = self._encode_client()
        
        data = {"grant_type": "refresh_token", "refresh_token": self.refresh_token}
        headers = {"Content-type": "application/x-www-form-urlencoded", "Authorization": f'Basic {encoded_client}'}

        response = requests.post(url=TOKEN_URL, data=data, headers=headers)
        response_status = response.status_code

        if response_status == 200:
            return response.json()['access_token']
        else:
            return "Error " + str(response_status)
        
    def _encode_client(self) -> str:
        client = ":".join([self.client_id, self.client_secret])
        encoded_client = base64.b64encode(client.encode("utf-8"))
        decoded_client = encoded_client.decode("utf-8")
        
        return decoded_client
