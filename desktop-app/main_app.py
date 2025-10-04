import sys
from PyQt6.QtWidgets import QApplication

from view import NeuroTrackView
from model import NeuroDataModel
from controller import NeuroTrackController

def main():
    """Main function to run the NeuroTrack application."""
    app = QApplication(sys.argv)
    
    # Create instances of the MVC components
    model = NeuroDataModel()
    view = NeuroTrackView()
    # The controller wires the model and view together
    controller = NeuroTrackController(model=model, view=view)
    
    view.resize(1280, 800)
    view.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()