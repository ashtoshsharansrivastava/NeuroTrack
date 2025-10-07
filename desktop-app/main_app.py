import sys
from PyQt6.QtWidgets import QApplication

from view import NeuroTrackView
from model import NeuroDataModel
from controller import NeuroTrackController

def main():
    """Main function to initialize and run the NeuroTrack application."""
    app = QApplication(sys.argv)
    
    # 1. Create instances of the core MVC components
    model = NeuroDataModel()
    view = NeuroTrackView()
    controller = NeuroTrackController(model=model, view=view)
    
    # 2. Hand control over to the controller to manage the startup sequence.
    # The controller will show the initial dialogs and then show the main view
    # only when the setup is complete.
    controller.run_startup_sequence()
    
    # 3. Start the application's main event loop. This line will only
    #    be reached after the main window is closed.
    sys.exit(app.exec())

if __name__ == '__main__':
    main()