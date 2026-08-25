import spotipy
from spotipy.oauth2 import SpotifyPKCE

from config import get_client_id

SCOPES = "user-read-playback-state user-modify-playback-state"
# The permisions we need from spotify

class SpotifyController:
    def __init__(self):
        login = SpotifyPKCE(
            client_id=get_client_id(), # Grabs client ID
            redirect_uri="http://127.0.0.1:8888/callback", # Where to send browser back after access approved
            scope=SCOPES, # Asks for permisions we set prior
            cache_path=".spotify-token", # Saves the login locally so you dont need to log in every time
            open_browser=True, # Allows spotipy to open spotifys auth page
        )

    # Creates the actual connection to the spotify API (again does it in self)
        self.spotify = spotipy.Spotify(auth_manager=login)

    def current_playback(self):
        return self.spotify.current_playback() # Built in spotify command for requesting playback information
        # Sends the response back to wherever called for

    def previous(self):
        self.spotify.previous_track()

    def next(self):
        self.spotify.next_track()

    def play(self):
        self.spotify.start_playback()

    def pause(self):
        self.spotify.pause_playback()

    def seek(self, position_ms):
        self.spotify.seek_track(position_ms)