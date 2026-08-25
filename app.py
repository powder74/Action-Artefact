import sys

# Qapplication manages the Graphical Application
from PySide6.QtWidgets import QApplication

# Lets us control window elsewhere but still call it from here
from ui import MainWindow
# Link our controller to app
from spotify_client import SpotifyController

# Creates the application manager. All PySide6 programs must have ONE Qapplication
# Calling it app doesnt really matter
app = QApplication(sys.argv)

spotify = SpotifyController() # Creates the controller
window = MainWindow(spotify) # Passes the controller into the mainwindow
window.show()

# Keeps the program alive and closes when closed etc
sys.exit(app.exec())