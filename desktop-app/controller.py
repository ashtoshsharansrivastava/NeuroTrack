from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QDialog  # <<< THE MISSING IMPORT IS ADDED HERE
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog

from view import ModeSelectionDialog

class NeuroTrackController:
    """
    The Controller in MVC. Connects the View and the Model.
    Handles user input, application state, and timers.
    """
    def __init__(self, model, view):
        self._model = model
        self._view = view
        self._connect_signals()
        
        # State management
        self.app_state = 'idle' # idle, calibrating, guided, monitoring, paused
        self.is_running = False

        # Timers
        self.data_timer = QTimer()
        self.data_timer.timeout.connect(self._model.update_data)

        self.calibration_timer = QTimer()
        self.calibration_timer.setSingleShot(True)
        self.calibration_timer.timeout.connect(self._on_calibration_complete)

        self.calibration_countdown_timer = QTimer()
        self.calibration_countdown_timer.timeout.connect(self._update_calibration_countdown)
        
    def _connect_signals(self):
        """Connect signals from the View to Controller slots."""
        self._view.new_session_button.clicked.connect(self.start_new_session)
        self._view.pause_resume_button.clicked.connect(self.toggle_pause_resume)
        self._view.print_button.clicked.connect(self.print_report)
        self._model.data_updated.connect(self._view.update_view)

    def start_new_session(self):
        """Shows the mode selection dialog and configures a new session."""
        self.stop_session() # Stop any existing session first
        
        dialog = ModeSelectionDialog(self._view)
        if dialog.exec():
            mode = dialog.selected_mode
            if mode:
                self._model.reset()
                self._view.pause_resume_button.setVisible(True)
                self._view.print_button.setEnabled(True)
                
                if mode == 'immediate':
                    self.app_state = 'monitoring'
                    self.start_monitoring()
                else: # calibrating or guided
                    self.app_state = mode
                    duration = 180 if mode == 'calibrating' else 90
                    self.start_calibration(mode, duration)

    def start_calibration(self, mode, duration):
        """Starts the calibration/guided relaxation process."""
        self.calibration_duration = duration
        self._view.calibration_overlay.start(mode, duration)
        self.calibration_countdown_timer.start(1000)
        self.calibration_timer.start(duration * 1000)

    def _update_calibration_countdown(self):
        """Updates the countdown timer on the overlay."""
        self.calibration_duration -= 1
        self._view.calibration_overlay.update_countdown()
        if self.calibration_duration <= 0:
            self.calibration_countdown_timer.stop()

    def _on_calibration_complete(self):
        """Called when the calibration timer finishes."""
        self._view.calibration_overlay.stop()
        self.app_state = 'monitoring'
        self.start_monitoring()

    def start_monitoring(self):
        """Starts the main data acquisition and plotting."""
        self.is_running = True
        self.data_timer.start(4)
        self._update_pause_resume_button()

    def stop_session(self):
        """Stops the current session completely and resets the UI."""
        self.is_running = False
        self.data_timer.stop()
        self.calibration_timer.stop()
        self.calibration_countdown_timer.stop()
        
        self.app_state = 'idle'
        self._model.reset()
        self._view.pause_resume_button.setVisible(False)
        self._view.print_button.setEnabled(False)
        self._view.calibration_overlay.stop()
        self._update_pause_resume_button()

    def toggle_pause_resume(self):
        """Toggles the running state of the monitoring."""
        if self.app_state not in ['monitoring', 'paused']:
            return
            
        self.is_running = not self.is_running
        if self.is_running:
            self.app_state = 'monitoring'
            self.data_timer.start()
        else:
            self.app_state = 'paused'
            self.data_timer.stop()
        self._update_pause_resume_button()

    def _update_pause_resume_button(self):
        """Updates the text, icon, and style of the pause/resume button."""
        self._view.update_pause_resume_button_state(self.is_running)

    def print_report(self):
        """Captures the current view and sends it to a printer."""
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog = QPrintDialog(printer, self._view)
        
        # --- CORRECTED LINE ---
        # We now correctly refer to QDialog.DialogCode.Accepted
        if dialog.exec() == QDialog.DialogCode.Accepted:
            painter = QPainter(printer)
            pixmap = self._view.central_widget.grab()
            
            page_rect = printer.pageLayout().paintRectPixels(printer.resolution())

            pixmap_scaled = pixmap.scaled(
                page_rect.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            
            x = (page_rect.width() - pixmap_scaled.width()) / 2
            y = (page_rect.height() - pixmap_scaled.height()) / 2
            
            painter.drawPixmap(int(x), int(y), pixmap_scaled)
            painter.end()