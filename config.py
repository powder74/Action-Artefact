import os

from dotenv import load_dotenv
# gets the info from the .env file
load_dotenv()

def get_client_id():
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
# Grabs the client ID and stores it

    if not client_id: # Checks if Client ID is empty and sends error if so
        raise ValueError("Spotify Client ID is missing from .env")

# sends back client ID back to wherever called
    return client_id