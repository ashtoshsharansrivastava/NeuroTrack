from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QGridLayout, QLabel, QPushButton, QDialog, QFrame
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap
import pyqtgraph as pg
from icons import create_icon_from_svg

# --- Custom Stylesheet ---
STYLESHEET = """
    QMainWindow, QDialog {
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
    #VitalsStateLabel {
        font-size: 28px;
        font-weight: bold;
        padding: 8px;
        border-radius: 8px;
    }
    #VitalsRatioLabel {
        font-size: 54px;
        font-weight: bold;
        color: #1F2937;
    }
    #PatientLabel {
        font-size: 14px;
        color: #4B5563;
    }
    #PatientValue {
        font-size: 14px;
        font-weight: bold;
        color: #111827;
    }
    #StatusBar {
        font-weight: bold;
        color: #4B5563;
        font-size: 12px;
    }
    QPushButton {
        padding: 10px 16px;
        font-size: 14px;
        font-weight: bold;
        border-radius: 8px;
        color: white;
        icon-size: 18px;
    }
    #NewSessionButton {
        background-color: #3B82F6;
    }
    #NewSessionButton:hover {
        background-color: #2563EB;
    }
    #PrintButton {
        background-color: #4B5563;
    }
    #PrintButton:hover {
        background-color: #374151;
    }
    #PrintButton:disabled {
        background-color: #D1D5DB;
    }
    #PauseButton {
        background-color: #F59E0B;
    }
    #PauseButton:hover {
        background-color: #D97706;
    }
    #ResumeButton {
        background-color: #10B981;
    }
    #ResumeButton:hover {
        background-color: #059669;
    }
"""

class NeuroTrackView(QMainWindow):
    """
    The View in MVC. Creates and manages all UI widgets.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧠 NeuroTrack Dashboard")
        self.setStyleSheet(STYLESHEET)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # --- CORRECTED ORDER ---
        # Create icons first, so they exist when other widgets need them.
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
        
        self.patient_name_value = QLabel("...")
        self.patient_name_value.setObjectName("PatientValue")

        self.patient_id_value = QLabel("...")
        self.patient_id_value.setObjectName("PatientValue")

        info_layout = QGridLayout()
        info_layout.addWidget(QLabel("Name:", objectName="PatientLabel"), 0, 0)
        info_layout.addWidget(self.patient_name_value, 0, 1)
        info_layout.addWidget(QLabel("Patient ID:", objectName="PatientLabel"), 1, 0)
        info_layout.addWidget(self.patient_id_value, 1, 1)
        
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
        pen = pg.mkPen(color="#3B82F6", width=2)
        self.eeg_curve = self.eeg_plot_widget.plot(pen=pen)

    def _create_fft_chart(self):
        self.fft_plot_widget = pg.PlotWidget()
        self.fft_plot_widget.setBackground('w')
        self.fft_plot_widget.setTitle("Frequency Power Spectrum (FFT)", color="#1F2937", size="16pt")
        self.fft_plot_widget.setLabel('left', 'Power', color='#4B5563')
        self.fft_plot_widget.getAxis('bottom').setTicks([
            [(0, 'Theta'), (1, 'Alpha'), (2, 'Beta'), (3, 'Gamma')]
        ])
        self.fft_bargraph = pg.BarGraphItem(x=range(4), height=[0,0,0,0], width=0.6, brush='#6366F1')
        self.fft_plot_widget.addItem(self.fft_bargraph)

    def _create_status_bar(self):
        self.status_bar_panel = QFrame()
        self.status_bar_panel.setObjectName("Panel")
        layout = QHBoxLayout(self.status_bar_panel)
        layout.setContentsMargins(20, 10, 20, 10)
        
        self.connection_status_label = QLabel("CONNECTION: SIMULATED")
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
        self.patient_name_value.setText(data["patientName"])
        self.patient_id_value.setText(data["patientId"])
        
        self.cognitive_state_label.setText(data["cognitiveState"])
        self.alpha_beta_ratio_label.setText(f"{data['alphaBetaRatio']:.2f}")
        
        bg_color = data['stateColor'] + '33'
        self.cognitive_state_label.setStyleSheet(f"background-color: {bg_color}; color: {'#DC2626' if data['acuteEvent'] else '#111827'}; border-radius: 8px; padding: 8px;")
        
        self.vitals_panel.setStyleSheet(f"#Panel {{ border: 2px solid {'#EF4444' if data['acuteEvent'] else '#E5E7EB'}; background-color: {'#FEE2E2' if data['acuteEvent'] else 'white'}; border-radius: 16px; }}")

        self.eeg_curve.setData(data["eegWaveform"])
        fft_values = list(data["fftData"].values())
        self.fft_bargraph.setOpts(height=fft_values)

        ms = data["sessionTime"]
        seconds = int((ms/1000)%60)
        minutes = int((ms/(1000*60))%60)
        hours = int((ms/(1000*60*60))%24)
        self.session_time_label.setText(f"SESSION TIME: {hours:02d}:{minutes:02d}:{seconds:02d}")

    def update_pause_resume_button_state(self, is_running):
        if is_running:
            self.pause_resume_button.setText(" Pause")
            self.pause_resume_button.setIcon(self.pause_icon)
            self.pause_resume_button.setObjectName("PauseButton")
        else:
            self.pause_resume_button.setText(" Resume")
            self.pause_resume_button.setIcon(self.play_icon)
            self.pause_resume_button.setObjectName("ResumeButton")

        self.pause_resume_button.style().unpolish(self.pause_resume_button)
        self.pause_resume_button.style().polish(self.pause_resume_button)

class ModeSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Start New Session")
        self.setModal(True)
        self.selected_mode = None
        
        layout = QVBoxLayout(self)
        
        title = QLabel("Start New Monitoring Session")
        title.setObjectName("HeaderLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        prompt = QLabel("Choose the appropriate mode based on the patient's current condition.")
        prompt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(title)
        layout.addWidget(prompt)
        
        modes = [
            ('calibrating', 'Full Calibration (3 min)', 'The most accurate mode...', 'brain'),
            ('guided', 'Guided Relaxation (90 sec)', 'A rapid, "best-effort" baseline...', 'wind'),
            ('immediate', 'Immediate Monitoring', 'Emergency fallback...', 'play')
        ]
        
        for mode, title, desc, icon_key in modes:
            button = self._create_mode_button(mode, title, desc, icon_key)
            layout.addWidget(button)
            
    def _create_mode_button(self, mode, title, desc, icon_key):
        button = QPushButton()
        button.setStyleSheet("padding: 12px; text-align: left; border: 1px solid #D1D5DB; border-radius: 8px; background-color: white;")
        layout = QHBoxLayout(button)
        
        icon_widget = QLabel()
        icon_pixmap = create_icon_from_svg(icon_key, "#3B82F6").pixmap(QSize(32, 32))
        icon_widget.setPixmap(icon_pixmap)
        icon_widget.setFixedSize(48, 48)
        icon_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        text_layout = QVBoxLayout()
        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold; font-size: 16px; color: #111827;")
        desc_label = QLabel(desc)
        desc_label.setStyleSheet("color: #4B5563;")
        text_layout.addWidget(title_label)
        text_layout.addWidget(desc_label)

        layout.addWidget(icon_widget)
        layout.addLayout(text_layout)
        button.clicked.connect(lambda _, m=mode: self._on_mode_selected(m))
        return button
        
    def _on_mode_selected(self, mode):
        self.selected_mode = mode
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
        
        layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.prompt, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.countdown_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
    def start(self, mode, duration):
        self.duration = duration
        self.title.setText("Calibrating..." if mode == 'calibrating' else "Guided Relaxation")
        self.prompt.setText("Please relax for the duration." if mode == 'calibrating' else "Please follow the breathing guide.")
        self.update_countdown()
        self.setVisible(True)
        self.resize(self.parent().size())

    def update_countdown(self):
        minutes = self.duration // 60
        seconds = self.duration % 60
        self.countdown_label.setText(f"{minutes:02d}:{seconds:02d}")

    def stop(self):
        self.hide()