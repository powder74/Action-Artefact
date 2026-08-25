# Spotify Controller — Action Artefact

This folder contains the simplified Spotify controller I created while learning the core programming needed for my projects software, I have also added my own personal notes so that I can look back and understand what's going on.

## What the prototype demonstrates

- Connecting a Python program to Spotify through its Web API
- Displaying the current song, artists and album artwork
- Controlling play, pause, previous and next
- Displaying and controlling the song timeline
- Refreshing the interface to match Spotify's current playback state

## Files

- `app.py` — starts the PySide6 application, creates the Spotify controller and opens the window.
- `config.py` — loads the Spotify client ID from a private local environment file.
- `spotify_client.py` — handles authentication and sends playback commands to Spotify.
- `ui.py` — creates the interface and updates its buttons, labels, artwork and timeline.
- `requirements.txt` — lists the Python packages used by the prototype.
- `.env.example` — shows the required environment-variable format without containing a real client ID.

## How to set up and use it (If u want)

1. Install Python 3 and create a virtual environment inside the project folder:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install -r requirements.txt
   ```

2. Create a Spotify application in the Spotify Developer Dashboard. Add `http://127.0.0.1:8888/callback` as its redirect URI.

3. Copy `.env.example` to a new file named `.env`, then replace `your_client_id_here` with the client ID from your Spotify application. Do not share the completed `.env` file.

4. Open Spotify on an active device and begin playing a song. Spotify Premium is required for remote playback controls.

5. Start the controller:

   ```bash
   python app.py
   ```

6. Approve access in the browser when Spotify asks. The window will then display the current song and allow you to play, pause, skip, go back and move through the timeline.

## Privacy Note

The real `.env` file and cached Spotify login token have been removed from this artefact because they contain private account information. The virtual environment and generated cache files were also removed because they are machine-specific and are not part of the code I created.
