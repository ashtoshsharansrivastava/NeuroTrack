from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPainter
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog

from view import ModeSelectionDialog, ConnectionDialog, PatientInfoDialog

class NeuroTrackController:
    """
    The Controller in MVC. Handles the entire application lifecycle.
    """
    def __init__(self, model, view):
        self._model = model
        self._view = view
        self._connect_signals()
        
        self.app_state = 'idle' 
        self.is_running = False

        self.data_timer = QTimer()
        self.data_timer.timeout.connect(self._model.update_data)
        self.calibration_timer = QTimer()
        self.calibration_timer.setSingleShot(True)
        self.calibration_timer.timeout.connect(self._on_calibration_complete)
        self.calibration_countdown_timer = QTimer()
        self.calibration_countdown_timer.timeout.connect(self._update_calibration_countdown)
        
    def run_startup_sequence(self):
        """Orchestrates the new startup workflow."""
        self._view.hide()
        
        conn_dialog = ConnectionDialog(self._view)
        if conn_dialog.exec():
            # --- DEFINITIVE FIX: Access the 'result' dictionary from the dialog ---
            result = conn_dialog.result
            if result["type"] == 'simulate':
                self._model.is_simulation = True
                self._model.set_connection_status("Simulated")
                self.proceed_to_patient_info()
            elif result["type"] == 'connect':
                self._model.is_simulation = False
                self._model.ip_address = result["ip"]
                self.simulate_connection()
        else:
            self._view.close()

    def simulate_connection(self):
        """Simulates the process of connecting to a device."""
        self._model.set_connection_status("Connecting...")
        QTimer.singleShot(2000, self.on_connection_successful)

    def on_connection_successful(self):
        self._model.set_connection_status("Connected")
        self.proceed_to_patient_info()

    def proceed_to_patient_info(self):
        """Shows the patient info dialog and then the main window."""
        patient_dialog = PatientInfoDialog(self._view)
        if patient_dialog.exec():
            self._model.set_patient_data(patient_dialog.patient_data)
            self._view.new_session_button.setEnabled(True)
            self._view.show()
        else:
            self._view.close()

    def _connect_signals(self):
        self._view.new_session_button.clicked.connect(self.start_new_session)
        self._view.pause_resume_button.clicked.connect(self.toggle_pause_resume)
        self._view.print_button.clicked.connect(self.print_report)
        self._model.data_updated.connect(self._view.update_view)

    def start_new_session(self):
        self.stop_session(reset_patient=False)
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
                else: 
                    self.app_state = mode
                    duration = 180 if mode == 'calibrating' else 90
                    self.start_calibration(mode, duration)

    def start_calibration(self, mode, duration):
        self.calibration_duration = duration
        self._view.calibration_overlay.start(mode, duration)
        self.calibration_countdown_timer.start(1000)
        self.calibration_timer.start(duration * 1000)

    def _update_calibration_countdown(self):
        self.calibration_duration -= 1
        self._view.calibration_overlay.update_countdown()
        if self.calibration_duration <= 0:
            self.calibration_countdown_timer.stop()

    def _on_calibration_complete(self):
        self._view.calibration_overlay.setVisible(False)
        self.app_state = 'monitoring'
        self.start_monitoring()

    def start_monitoring(self):
        self.is_running = True
        self.data_timer.start(4)
        self._view.update_pause_resume_button_state(self.is_running)

    def stop_session(self, reset_patient=True):
        self.is_running = False
        self.data_timer.stop()
        self.calibration_timer.stop()
        self.calibration_countdown_timer.stop()
        self.app_state = 'idle'
        self._model.reset()
        if reset_patient:
            self._model.set_patient_data({
                "name": "N/A", "age": "N/A", "weight": "N/A",
                "issues": "N/A", "sleep": "N/A",
            })
        self._view.pause_resume_button.setVisible(False)
        self._view.print_button.setEnabled(False)
        self._view.calibration_overlay.setVisible(False)
        self._view.update_pause_resume_button_state(False)

    def toggle_pause_resume(self):
        if self.app_state not in ['monitoring', 'paused']: return
        self.is_running = not self.is_running
        self.app_state = 'monitoring' if self.is_running else 'paused'
        if self.is_running: self.data_timer.start()
        else: self.data_timer.stop()
        self._view.update_pause_resume_button_state(self.is_running)

    def print_report(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog = QPrintDialog(printer, self._view)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            painter = QPainter(printer)
            pixmap = self._view.central_widget.grab()
            page_rect = printer.pageLayout().paintRectPixels(printer.resolution())
            pixmap_scaled = pixmap.scaled(page_rect.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            x, y = (page_rect.width() - pixmap_scaled.width()) / 2, (page_rect.height() - pixmap_scaled.height()) / 2
            painter.drawPixmap(int(x), int(y), pixmap_scaled)
            painter.end()