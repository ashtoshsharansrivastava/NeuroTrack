from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QGridLayout, QLabel, QPushButton, QDialog, QFrame,
    QLineEdit, QTextEdit
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap
import pyqtgraph as pg
from icons import create_icon_from_svg

# --- Custom Stylesheet ---
STYLESHEET = """
    #MainWindow, QDialog {
        background-color: #F3F4F6;
    }
    #HeaderLabel {
        font-size: 28px;
        font-weight: bold;
        color: #1F2937;
    }
    #Panel {
        background-color: white;
        border: 1px solid #E5E7EB;
        border-radius: 16px;
    }
    #PanelHeader {
        font-size: 16px;
        font-weight: bold;
        color: #1F2937;
        margin-bottom: 8px;
    }
    #VitalsStateLabel, #VitalsRatioLabel, #PatientLabel, #PatientValue, #StatusBar,
    #DialogLabel, #DialogButtonLabel, #DialogDescLabel {
        color: #1F2937; /* Default to dark text */
    }
    #VitalsStateLabel { font-size: 28px; font-weight: bold; padding: 8px; border-radius: 8px; }
    #VitalsRatioLabel { font-size: 54px; font-weight: bold; }
    #PatientLabel { font-size: 14px; color: #4B5563; }
    #PatientValue { font-size: 14px; font-weight: bold; }
    #StatusBar { font-weight: bold; color: #4B5563; font-size: 12px; }
    
    /* --- DEFINITIVE FIX START --- */
    /* General button styling without a text color */
    QPushButton {
        padding: 10px 16px;
        font-size: 14px;
        font-weight: bold;
        border-radius: 8px;
        icon-size: 18px;
    }
    /* Apply white text color ONLY to the specific header buttons by their object name */
    #NewSessionButton, #PrintButton, #PauseButton, #ResumeButton {
        color: white; 
    }
    /* --- DEFINITIVE FIX END --- */

    #NewSessionButton { background-color: #3B82F6; }
    #NewSessionButton:hover { background-color: #2563EB; }
    #PrintButton { background-color: #4B5563; }
    #PrintButton:hover { background-color: #374151; }
    #PrintButton:disabled { background-color: #D1D5DB; }
    #PauseButton { background-color: #F59E0B; }
    #PauseButton:hover { background-color: #D97706; }
    #ResumeButton { background-color: #10B981; }
    #ResumeButton:hover { background-color: #059669; }
    QLineEdit, QTextEdit {
        border: 1px solid #D1D5DB;
        border-radius: 8px;
        padding: 8px;
        font-size: 14px;
        background-color: #F9FAFB;
    }
"""

class NeuroTrackView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.setWindowTitle("🧠 NeuroTrack Dashboard")
        self.setStyleSheet(STYLESHEET)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        self.play_icon = create_icon_from_svg("play", "white")
        self.pause_icon = create_icon_from_svg("pause", "white")
        self.print_icon = create_icon_from_svg("printer", "white")

        self._create_widgets()
        self._configure_layout()
        
    def _create_widgets(self):
        self._create_header()
        self._create_patient_panel()
        self._create_vitals_panel()
        self._create_eeg_chart()
        self._create_fft_chart()
        self._create_status_bar()
        self._create_calibration_overlay()

    def _configure_layout(self):
        top_row_layout = QHBoxLayout()
        top_row_layout.addWidget(self.patient_panel, 1)
        top_row_layout.addWidget(self.vitals_panel, 2)
        
        self.main_layout.addLayout(self.header_layout)
        self.main_layout.addLayout(top_row_layout)
        self.main_layout.addWidget(self.eeg_plot_widget)
        self.main_layout.addWidget(self.fft_plot_widget)
        self.main_layout.addWidget(self.status_bar_panel)

    def _create_header(self):
        self.header_layout = QHBoxLayout()
        title = QLabel("🧠 NeuroTrack Dashboard")
        title.setObjectName("HeaderLabel")
        
        self.print_button = QPushButton(" Print Report")
        self.print_button.setObjectName("PrintButton")
        self.print_button.setIcon(self.print_icon)
        self.print_button.setEnabled(False)

        self.new_session_button = QPushButton("New Session")
        self.new_session_button.setObjectName("NewSessionButton")
        
        self.pause_resume_button = QPushButton()
        self.pause_resume_button.setVisible(False)

        self.header_layout.addWidget(title)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.print_button)
        self.header_layout.addWidget(self.new_session_button)
        self.header_layout.addWidget(self.pause_resume_button)

    def _create_patient_panel(self):
        self.patient_panel = QFrame()
        self.patient_panel.setObjectName("Panel")
        layout = QVBoxLayout(self.patient_panel)
        header = QLabel("PATIENT INFORMATION")
        header.setObjectName("PanelHeader")
        self.patient_details = {}
        fields = {"name": "Name", "age": "Age", "weight": "Weight (kg)", "sleep": "Sleep (hrs/night)", "issues": "Presenting Issues"}
        info_layout = QGridLayout()
        info_layout.setColumnStretch(1, 1)
        for i, (key, label_text) in enumerate(fields.items()):
            label = QLabel(f"{label_text}:")
            label.setObjectName("PatientLabel")
            value = QLabel("...")
            value.setObjectName("PatientValue")
            if key == "issues":
                value.setWordWrap(True)
                value.setAlignment(Qt.AlignmentFlag.AlignTop)
            info_layout.addWidget(label, i, 0)
            info_layout.addWidget(value, i, 1)
            self.patient_details[key] = value
        layout.addWidget(header)
        layout.addLayout(info_layout)
        layout.addStretch()

    def _create_vitals_panel(self):
        self.vitals_panel = QFrame()
        self.vitals_panel.setObjectName("Panel")
        layout = QHBoxLayout(self.vitals_panel)
        state_layout = QVBoxLayout()
        state_header = QLabel("COGNITIVE STATE")
        state_header.setObjectName("PanelHeader")
        state_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cognitive_state_label = QLabel("Idle")
        self.cognitive_state_label.setObjectName("VitalsStateLabel")
        self.cognitive_state_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        state_layout.addWidget(state_header)
        state_layout.addWidget(self.cognitive_state_label)
        ratio_layout = QVBoxLayout()
        ratio_header = QLabel("ALPHA/BETA RATIO")
        ratio_header.setObjectName("PanelHeader")
        ratio_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.alpha_beta_ratio_label = QLabel("1.00")
        self.alpha_beta_ratio_label.setObjectName("VitalsRatioLabel")
        self.alpha_beta_ratio_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ratio_layout.addWidget(ratio_header)
        ratio_layout.addWidget(self.alpha_beta_ratio_label)
        layout.addLayout(state_layout)
        layout.addLayout(ratio_layout)

    def _create_eeg_chart(self):
        self.eeg_plot_widget = pg.PlotWidget()
        self.eeg_plot_widget.setBackground('w')
        self.eeg_plot_widget.setTitle("Live EEG Waveform", color="#1F2937", size="16pt")
        self.eeg_plot_widget.setLabel('left', 'Amplitude (μV)', color='#4B5563')
        self.eeg_plot_widget.setLabel('bottom', 'Time (Samples)', color='#4B5563')
        self.eeg_plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self.eeg_plot_widget.setYRange(-50, 50)
        self.eeg_curve = self.eeg_plot_widget.plot(pen=pg.mkPen(color="#3B82F6", width=2))

    def _create_fft_chart(self):
        self.fft_plot_widget = pg.PlotWidget()
        self.fft_plot_widget.setBackground('w')
        self.fft_plot_widget.setTitle("Frequency Power Spectrum (FFT)", color="#1F2937", size="16pt")
        self.fft_plot_widget.setLabel('left', 'Power', color='#4B5563')
        self.fft_plot_widget.getAxis('bottom').setTicks([[(i, k.split(' ')[0]) for i, k in enumerate(
            ['Theta (4-8Hz)', 'Alpha (8-13Hz)', 'Beta (13-30Hz)', 'Gamma (>30Hz)'])]])
        self.fft_bargraph = pg.BarGraphItem(x=range(4), height=[0]*4, width=0.6, brush='#6366F1')
        self.fft_plot_widget.addItem(self.fft_bargraph)

    def _create_status_bar(self):
        self.status_bar_panel = QFrame()
        self.status_bar_panel.setObjectName("Panel")
        layout = QHBoxLayout(self.status_bar_panel)
        layout.setContentsMargins(20, 10, 20, 10)
        self.connection_status_label = QLabel("CONNECTION: DISCONNECTED")
        self.connection_status_label.setObjectName("StatusBar")
        self.session_time_label = QLabel("SESSION TIME: 00:00:00")
        self.session_time_label.setObjectName("StatusBar")
        layout.addWidget(self.connection_status_label)
        layout.addStretch()
        layout.addWidget(self.session_time_label)
        
    def _create_calibration_overlay(self):
        self.calibration_overlay = CalibrationOverlay(self.central_widget)
        self.calibration_overlay.hide()

    def update_view(self, data):
        for key, value in data["patientData"].items():
            if key in self.patient_details:
                self.patient_details[key].setText(str(value))

        self.cognitive_state_label.setText(data["cognitiveState"])
        self.alpha_beta_ratio_label.setText(f"{data['alphaBetaRatio']:.2f}")
        
        bg_color = data['stateColor'] + '33'
        self.cognitive_state_label.setStyleSheet(f"background-color: {bg_color}; color: {'#DC2626' if data['acuteEvent'] else '#111827'}; border-radius: 8px; padding: 8px;")
        self.vitals_panel.setStyleSheet(f"#Panel {{ border: 2px solid {'#EF4444' if data['acuteEvent'] else '#E5E7EB'}; background-color: {'#FEE2E2' if data['acuteEvent'] else 'white'}; border-radius: 16px; }}")

        self.eeg_curve.setData(data["eegWaveform"])
        fft_values = list(data["fftData"].values())
        self.fft_bargraph.setOpts(height=fft_values)

        ms = data["sessionTime"]
        seconds, minutes, hours = int((ms/1000)%60), int((ms/(1000*60))%60), int((ms/(1000*60*60))%24)
        self.session_time_label.setText(f"SESSION TIME: {hours:02d}:{minutes:02d}:{seconds:02d}")
        
        self.connection_status_label.setText(f"CONNECTION: {data['connectionStatus'].upper()}")
        status_colors = {"Disconnected": "#EF4444", "Connecting...": "#3B82F6", "Connected": "#10B981", "Simulated": "#F59E0B"}
        self.connection_status_label.setStyleSheet(f"font-weight: bold; color: {status_colors.get(data['connectionStatus'], '#4B5563')};")

    def update_pause_resume_button_state(self, is_running):
        self.pause_resume_button.setText(" Pause" if is_running else " Resume")
        self.pause_resume_button.setIcon(self.pause_icon if is_running else self.play_icon)
        self.pause_resume_button.setObjectName("PauseButton" if is_running else "ResumeButton")
        self.pause_resume_button.style().unpolish(self.pause_resume_button)
        self.pause_resume_button.style().polish(self.pause_resume_button)

class ModeSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Start New Monitoring Mode")
        self.setModal(True)
        self.selected_mode = None
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        title = QLabel("Select Monitoring Mode")
        title.setObjectName("HeaderLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        modes = [
            ('calibrating', 'Full Calibration (3 min)', 'For routine checkups.', 'brain'),
            ('guided', 'Guided Relaxation (90 sec)', 'For stressed patients.', 'wind'),
            ('immediate', 'Immediate Monitoring', 'For acute events.', 'play')
        ]
        
        for mode, title_text, desc, icon_key in modes:
            button = self._create_mode_button(mode, title_text, desc, icon_key)
            layout.addWidget(button)
            
    def _create_mode_button(self, mode, title_text, desc, icon_key):
        button = QPushButton()
        button.setStyleSheet("""
            QPushButton { 
                padding: 12px; 
                text-align: left; 
                border: 1px solid #D1D5DB; 
                border-radius: 8px; 
                background-color: white;
            }
            QPushButton:hover {
                border-color: #3B82F6;
                background-color: #EFF6FF;
            }
        """)
        button.clicked.connect(lambda _, m=mode: self._on_mode_selected(m))
        btn_layout = QHBoxLayout(button)
        
        icon = QLabel()
        icon.setPixmap(create_icon_from_svg(icon_key, "#3B82F6").pixmap(QSize(32, 32)))
        icon.setFixedSize(48, 48)
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        text_layout = QVBoxLayout()
        title_label = QLabel(title_text)
        title_label.setObjectName("DialogButtonLabel")
        desc_label = QLabel(desc)
        desc_label.setObjectName("DialogDescLabel")
        text_layout.addWidget(title_label)
        text_layout.addWidget(desc_label)

        btn_layout.addWidget(icon)
        btn_layout.addLayout(text_layout)
        return button
            
    def _on_mode_selected(self, mode):
        self.selected_mode = mode
        self.accept()

# The rest of the file (PatientInfoDialog, ConnectionDialog, CalibrationOverlay) is correct
# and does not need to be shown again for brevity, but they exist in your full file.

class ConnectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Connection")
        self.setModal(True)
        self.result = {"type": None, "ip": None}
        layout = QVBoxLayout(self)
        title = QLabel("Welcome to NeuroTrack")
        title.setObjectName("HeaderLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        ip_frame = QFrame()
        ip_layout = QGridLayout(ip_frame)
        ip_label = QLabel("Enter Device IP Address:")
        self.ip_input = QLineEdit("192.168.1.100")
        connect_button = QPushButton("Connect to Device")
        connect_button.setObjectName("NewSessionButton")
        connect_button.clicked.connect(self.accept_connection)
        ip_layout.addWidget(ip_label, 0, 0)
        ip_layout.addWidget(self.ip_input, 0, 1)
        ip_layout.addWidget(connect_button, 1, 0, 1, 2)
        layout.addWidget(ip_frame)
        separator = QLabel("or")
        separator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(separator)
        sim_button = QPushButton("Run Simulation")
        sim_button.clicked.connect(self.accept_simulation)
        layout.addWidget(sim_button)
        
    def accept_connection(self):
        self.result["type"] = "connect"
        self.result["ip"] = self.ip_input.text()
        self.accept()
        
    def accept_simulation(self):
        self.result["type"] = "simulate"
        self.accept()

class PatientInfoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Enter Patient Details")
        self.setModal(True)
        self.patient_data = {}
        layout = QGridLayout(self)
        title = QLabel("New Patient Session")
        title.setObjectName("HeaderLabel")
        layout.addWidget(title, 0, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.fields = { "name": QLineEdit("John Doe"), "age": QLineEdit("35"), "weight": QLineEdit("75"), "sleep": QLineEdit("7"), "issues": QTextEdit("Reports anxiety and difficulty concentrating.") }
        self.fields["issues"].setFixedHeight(80)
        for i, (key, widget) in enumerate(self.fields.items()):
            label_text = key.replace('_', ' ').title()
            label = QLabel(f"{label_text}:")
            label.setObjectName("DialogLabel")
            layout.addWidget(label, i + 1, 0)
            layout.addWidget(widget, i + 1, 1)
        submit_button = QPushButton("Start Session")
        submit_button.setObjectName("NewSessionButton")
        submit_button.clicked.connect(self.submit)
        layout.addWidget(submit_button, len(self.fields) + 1, 0, 1, 2)
        
    def submit(self):
        self.patient_data = {key: widget.text() if isinstance(widget, QLineEdit) else widget.toPlainText() for key, widget in self.fields.items()}
        self.accept()

class CalibrationOverlay(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Panel")
        self.setStyleSheet("#Panel { background-color: rgba(243, 244, 246, 0.95); }")
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title = QLabel()
        self.title.setObjectName("HeaderLabel")
        self.prompt = QLabel()
        self.prompt.setStyleSheet("font-size: 16px; color: #4B5563;")
        self.countdown_label = QLabel()
        self.countdown_label.setStyleSheet("font-size: 72px; font-weight: bold; font-family: monospace; color: #1F2937;")
        layout.addWidget(self.title)
        layout.addWidget(self.prompt)
        layout.addWidget(self.countdown_label)
        
    def start(self, mode, duration):
        self.duration = duration
        self.title.setText("Calibrating..." if mode == 'calibrating' else "Guided Relaxation")
        self.prompt.setText("Please relax for the duration." if mode == 'calibrating' else "Please follow the breathing guide.")
        self.update_countdown()
        self.setVisible(True)
        self.resize(self.parent().size())

    def update_countdown(self):
        minutes, seconds = divmod(self.duration, 60)
        self.countdown_label.setText(f"{minutes:02d}:{seconds:02d}")

    def stop(self):
        self.hide()