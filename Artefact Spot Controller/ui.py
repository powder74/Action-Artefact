import requests

# Import PySide6 Existing window type
from PySide6.QtWidgets import (
    QLabel, # For text
    QMainWindow, # The window itself
    QVBoxLayout, # Veritcal layout
    QWidget, # A container for our things
    QHBoxLayout, # Horizontal layout
    QPushButton, # Lets us add clickable buttons
    QSlider, # For the timeline slider
)

from PySide6.QtCore import Qt, QTimer # for the timeline
from PySide6.QtGui import QPixmap # needed for image display

# Create our new Window Type while using defaults from QMainWindow
class MainWindow(QMainWindow):
    # recieves our spotify controller from app.py
    def __init__(self, spotify): # Runs whenever a new MainWindow is created
        super().__init__() # Runs the original QMainWindow setup

        self.spotify = spotify
# Saves the supplied controller as self.spotify so other window methods can use it

        self.is_playing = False
        self.just_seeked = False # so that the player doesnt just tp back to original spot after moving timeline
        # It just doenst do the next refresh cycle for the timeline after we move the player head

        self.current_artwork_url = None

        self.setWindowTitle("Spotify Controller")
        self.resize(420, 220) # Resize the window but allow user resize

        self.artwork_label = QLabel("No Cover")
        self.artwork_label.setFixedSize(250, 250)
        self.artwork_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.timeline = QSlider(Qt.Orientation.Horizontal) # make a slider that can move left to right
        self.elapsed_label = QLabel("0:00") # Label for how far into the song we are
        self.duration_label = QLabel("0:00") # Label for total song length

        timeline_row = QHBoxLayout() # A sort of group of widgets to add for the timeline
        timeline_row.addWidget(self.elapsed_label)
        timeline_row.addWidget(self.timeline)
        timeline_row.addWidget(self.duration_label)

    # Creates the placeholders for the text
        self.track_label = QLabel("Nothing Playing") 
        self.artist_label = QLabel("No Artist")
    # Creates placholder buttons
        self.track_label.setWordWrap(True)
        self.artist_label.setWordWrap(True) #dont go off scren cuh

        self.previous_button = QPushButton("Previous")
        self.play_button = QPushButton("Play")
        self.next_button = QPushButton("Next")
    # Creates these as self variables so they can be reused and changed outside __init__

        buttons = QHBoxLayout()
        buttons.addWidget(self.previous_button)
        buttons.addWidget(self.play_button)
        buttons.addWidget(self.next_button)
    # Adds the buttons in the correct horizontal order

    # Connect each button's clicked signal to its matching method
        self.previous_button.clicked.connect(self.previous_clicked)
        self.play_button.clicked.connect(self.play_clicked)
        self.next_button.clicked.connect(self.next_clicked)

        layout = QVBoxLayout() # Creates empty vertical layout

        layout.addWidget(
            self.artwork_label,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        layout.addWidget(self.track_label)
        layout.addWidget(self.artist_label)
    # Adds the labels in correct order
        layout.addLayout(timeline_row) # Adds in that timeline group of things
        layout.addLayout(buttons) # addLayout instead of widget bc buttons are a lot of widgets in one
    # Adds the buttons below the text and timeline above that

        self.timeline.sliderReleased.connect(self.timeline_released) # Once user is done draggin run timeline_released

        container = QWidget()
        container.setLayout(layout)
    # Creates widget and attaches the vertical layout to it
    # This is because QMainWindow doesnt just take the layout
    # It needs a central widget/container, which is this


        self.setCentralWidget(container)
    # Puts the container into QMainWindow

        self.timer = QTimer() # Creates the timer
        self.timer.timeout.connect(self.refresh) # Once reaches its interval it timeout
        self.timer.start(2000) # Starts the timer with interval of 2,000 ms

        self.refresh()

    def play_clicked(self): # The function called from the button
        if self.is_playing: # Ask if its true
            self.spotify.pause()
        else: # If not true
            self.spotify.play()

        self.refresh()

    def previous_clicked(self): # Function ran when u click previous
        self.spotify.previous()
        self.refresh()

    def next_clicked(self): # Function ran when u click next
        self.spotify.next()
        self.refresh()

    def timeline_released(self): # Function for when we release the dragger on the timeline
        position_ms = self.timeline.value() # Get the value user released at
        self.spotify.seek(position_ms) # Send it to spotify
        self.just_seeked = True # Prevents the next refresh from taking our player back temporarily

    def format_time(self, milliseconds):
        total_seconds = milliseconds // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        #spotify returns milliseconds so we just use this to convert it to seconds and minutes
        return f"{minutes}:{seconds:02d}" # The display of the numbers

    def update_artwork(self, artwork_url):
        if artwork_url == self.current_artwork_url:
            return # if artwork unchanged then dont update it

        self.current_artwork_url = artwork_url # remember the url so we dont repeatedly download it

        response = requests.get(artwork_url, timeout=5) # downloads the image, timeout stops it from waiting forever if something goes wrong
        response.raise_for_status() # raises error if the download failed

        artwork = QPixmap()
        artwork.loadFromData(response.content)
    # creates an empty PySide6 image and loads the downloaded bytes into it

        artwork = artwork.scaled(
            self.artwork_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        ) # Creates a resized version that can fit inside the label and keeps the square proportions along side with smooth resizing

        self.artwork_label.setText("") #sets text to nothin
        self.artwork_label.setPixmap(artwork) #displays it
        

    def refresh(self): # Gets spotify latest data and updates window to match
        playback = self.spotify.current_playback() # Asks for our data we took earlier

        if playback and playback.get("item"): # Checks if we got data back from spotify and its a valid item
            track = playback["item"] # so we dont have to keep writing playback["item"]["name"]
            artists = track["artists"] # Gets the list of artists from the song
            artist_names = ", ".join(artist["name"] for artist in artists) # Grabs all the names and puts a comma between if multiple

            images = track["album"]["images"]
            artwork_url = images[0]["url"]
            self.update_artwork(artwork_url)


            self.is_playing = playback["is_playing"]
            # gets spotify's real playback state

            self.track_label.setText(track["name"]) # set the labels to the data provided by spotify
            self.artist_label.setText(artist_names) # sets the names

            self.timeline.setEnabled(True)
            self.timeline.setRange(0, track["duration_ms"]) # Sets the length of the song so the slider can work

            self.elapsed_label.setText(
                self.format_time(playback["progress_ms"])
            )

            self.duration_label.setText(
                self.format_time(track["duration_ms"])
            )

            if self.just_seeked: # just seeked happens in our release of timeline to say that we seeked so that it can skip a refresh so that the timeline doesnt randomly jump
                self.just_seeked = False
            elif not self. timeline.isSliderDown(): # Checks if we are holding the slider
                self.timeline.setValue(playback["progress_ms"]) # Then this value sets the time where the player is at on that slider


            if self.is_playing:
                self.play_button.setText("Pause")
                # If spotify is playing, make the button "Pause"
            else:
                self.play_button.setText("Play")
                # If spotify is not playing, make the button "Play"

        else: # Runs when spotify returns no playback
            self.is_playing = False

            self.timeline.setRange(0, 100)
            self.timeline.setValue(0)
            self.timeline.setEnabled(False)
            self.track_label.setText("Nothing Playing")
            self.artist_label.setText("No Artist")
            self.play_button.setText("Play")
            self.elapsed_label.setText("0:00")
            self.duration_label.setText("0:00")
            self.current_artwork_url = None
            self.artwork_label.setPixmap(QPixmap())
            self.artwork_label.setText("No Cover")
            # Resets back to default
