import requests
import base64

from lib.spotify_secrets import CLIENT_SECRET, CLIENT_ID, REFRESH_TOKEN



class SpotifyUser:
  def __init__(self):
    self.refreshToken = REFRESH_TOKEN
    self.clientId = CLIENT_ID
    self.clientSecret = CLIENT_SECRET
    self.accessToken = self.getAccessToken()

    self.updatePlayback()

    if(self.playbackState == 'Not Playing'):
       self.device = 0
    else:
      self.device = self.playbackState['device']['id']
    
  
  def getAccessToken(self):
    url = "https://accounts.spotify.com/api/token"
    encoded_str = base64.b64encode(f"{self.clientId}:{self.clientSecret}".encode('utf-8')).decode('utf-8')
    data = {'grant_type': 'refresh_token', 'refresh_token': self.refreshToken}
    head = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': f'Basic {encoded_str}'}

    r = requests.post(url=url, data=data, headers=head)
    status = r.status_code

    if(status == 200):  
      return r.json()['access_token']
    else: 
        return "Error " + str(status) 
    
  def updatePlayback(self):
      url = 'https://api.spotify.com/v1/me/player'
      head = {'Authorization': 'Bearer ' + self.accessToken}

      r = requests.get(url = url, headers = head)
      status = r.status_code
      
      #good request
      if(status == 200):
          self.playbackState = r.json()
          self.device = self.playbackState['device']['id']
      #no devices active
      elif(status == 204):
          self.playbackState = 'Not Playing'
          self.device = 0
      #need a new access token
      elif(status == 401):
          self.accessToken = self.getAccessToken()
          self.updatePlayback()
      #other errors and ??
      else:
          self.playbackState = 'Error ' + str(r.status_code)

  def alterPlayback(self, alteration_type):
    url = 'https://api.spotify.com/v1/me/player/' + alteration_type + '?device_id=' + self.device
    head = {'Authorization': 'Bearer ' + self.accessToken, 'Content-Type': 'application/json'}

    if(alteration_type == 'play' or alteration_type == 'pause'):
      r = requests.put(url = url, headers = head)
    else:
      r = requests.post(url = url, headers = head)

    status = r.status_code

    if(status == 204 or status == 200):
      match alteration_type:
        case 'play':
            return 'Song Resumed!'
        case 'pause':
            return 'Song Paused!'
        case 'next':
            return 'Next Song!'
        case 'previous':
            return 'Previous Song!'
        case _:
            return 'Song Altered?'  
        
    elif(status == 401):
      self.accessToken = self.getAccessToken()
      return self.alterPlayback(alteration_type)
    else:
      return 'Error ' + str(status)
