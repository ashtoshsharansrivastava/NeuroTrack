import numpy as np
from PyQt6.QtCore import QObject, pyqtSignal

class NeuroDataModel(QObject):
    """
    The Model in MVC. Handles data generation, storage, and business logic.
    It emits signals when data is updated, allowing other parts of the app to react.
    """
    data_updated = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        # --- Configuration & State ---
        self.is_simulation = True
        self.ip_address = None
        self.connection_status = "Disconnected"
        
        # --- Patient Data ---
        self.patient_data = {
            "name": "N/A", "age": "N/A", "weight": "N/A",
            "issues": "N/A", "sleep": "N/A",
        }
        
        # --- Session Data ---
        self.session_time = 0
        self.eeg_waveform = np.zeros(500) # Buffer for 2 seconds of data at 250Hz
        self.alpha_beta_ratio = 1.0
        self.cognitive_state = "Idle"
        self.state_color = "#A0A0A0" # Neutral gray for idle state
        self.acute_event = False
        self.fft_data = {'Theta': 0, 'Alpha': 0, 'Beta': 0, 'Gamma': 0}
        
        # --- Internal Simulation Variables ---
        self.time_offset = 0
        self.ratio_history = [1.0]

    def set_patient_data(self, data):
        """Stores the detailed patient information for the session."""
        self.patient_data = data
        self.data_updated.emit(self.get_data_snapshot())
    
    def set_connection_status(self, status):
        """Updates the current connection status."""
        self.connection_status = status
        self.data_updated.emit(self.get_data_snapshot())

    def update_data(self):
        """
        Generates a new data point and updates the model state.
        This method simulates the continuous flow of data from a sensor.
        """
        if not self.is_simulation:
            # In a real application, this is where you would process live hardware data.
            # For now, we do nothing if not in simulation mode.
            return 

        SAMPLE_RATE = 250
        self.session_time += 1000 / SAMPLE_RATE
        self.time_offset += 1 / SAMPLE_RATE

        # --- Generate a realistic, complex EEG signal ---
        alpha_amplitude = 15 + 10 * np.sin(self.time_offset / 5)
        beta_amplitude = 8 + 6 * np.sin(self.time_offset / 1.5)
        alpha_wave = alpha_amplitude * np.sin(2 * np.pi * 10 * self.time_offset)
        beta_wave = beta_amplitude * np.sin(2 * np.pi * 22 * self.time_offset)
        noise = (np.random.rand() - 0.5) * 10
        new_amplitude = alpha_wave + beta_wave + noise
        
        # Update the waveform buffer using a rolling window for a smooth scroll effect
        self.eeg_waveform = np.roll(self.eeg_waveform, -1)
        self.eeg_waveform[-1] = new_amplitude

        # --- Simulate Analysis (FFT, Ratio, State) ---
        alpha_power = alpha_amplitude**2
        beta_power = beta_amplitude**2
        self.alpha_beta_ratio = alpha_power / beta_power if beta_power > 1 else alpha_power

        # --- State Classification Logic ---
        if self.alpha_beta_ratio > 2.5:
            self.cognitive_state = "Calm"
            self.state_color = "#2ECC71" # Green
        elif self.alpha_beta_ratio > 1.5:
            self.cognitive_state = "Neutral / Focused"
            self.state_color = "#F1C40F" # Yellow
        else:
            self.cognitive_state = "High Cognitive Load"
            self.state_color = "#E74C3C" # Red

        # --- Acute Event Detection Logic ---
        last_ratio = self.ratio_history[-1]
        self.acute_event = (last_ratio - self.alpha_beta_ratio) > 2.0
        if self.acute_event:
            self.cognitive_state = "ACUTE EVENT DETECTED"
        
        # Store the last second of ratio history for event detection
        self.ratio_history.append(self.alpha_beta_ratio)
        if len(self.ratio_history) > 250: 
            self.ratio_history.pop(0)
            
        # --- FFT Data Simulation ---
        self.fft_data = {
            'Theta (4-8Hz)': np.random.rand() * 200,
            'Alpha (8-13Hz)': alpha_power * 10 + np.random.rand() * 50,
            'Beta (13-30Hz)': beta_power * 10 + np.random.rand() * 50,
            'Gamma (>30Hz)': np.random.rand() * 150
        }
        
        # Emit a signal containing a dictionary of the new data for the View to update
        self.data_updated.emit(self.get_data_snapshot())

    def get_data_snapshot(self):
        """Returns a dictionary of the current model state."""
        return {
            "patientData": self.patient_data,
            "sessionTime": self.session_time,
            "eegWaveform": self.eeg_waveform,
            "fftData": self.fft_data,
            "alphaBetaRatio": self.alpha_beta_ratio,
            "cognitiveState": self.cognitive_state,
            "stateColor": self.state_color,
            "acuteEvent": self.acute_event,
            "connectionStatus": self.connection_status,
        }
        
    def reset(self):
        """Resets the model's session data to its initial state."""
        self.session_time = 0
        self.eeg_waveform = np.zeros(500)
        self.alpha_beta_ratio = 1.0
        self.cognitive_state = "Idle"
        self.state_color = "#A0A0A0"
        self.acute_event = False
        self.time_offset = 0
        self.ratio_history = [1.0]
        # Emit the reset state so the UI clears
        self.data_updated.emit(self.get_data_snapshot())