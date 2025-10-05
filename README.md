<div align="center">

🧠 NeuroTrack: An EEG-Based Stress & Depression Analyzer
A professional, real-time EEG monitoring dashboard for clinical environments.

A preview of the NeuroTrack dashboard in action.

</div>

✨ Core Features
Real-Time EEG Visualization: View a live, scrolling graph of EEG waveform data.

Frequency Spectrum Analysis: See a bar chart of brainwave power in different bands (Alpha, Beta, etc.).

Advanced Clinical Workflow: Includes a Three-Tiered Triage Strategy for patient assessment:

-Full Calibration: A 3-minute personal baseline for maximum accuracy in routine checkups.

-Guided Relaxation: A 90-second "best-effort" baseline for stressed but cooperative patients.

-Immediate Monitoring: An emergency fallback using population data for acute events.

Patient Report Generation: Instantly print or save a PDF report of the current session snapshot.

Cross-Platform: The application can be run and built for both Windows and Linux.

🚀 Quick Start for End-Users
This guide is for users who just want to run the NeuroTrack application without dealing with the source code.

Download the Application:

Go to the Releases Page of this GitHub repository.

Download the latest version for your operating system:

For Windows: NeuroTrack-Windows.zip (contains main_app.exe)

For Linux: NeuroTrack-Linux.zip (contains the main_app executable)

Run the Application:

<details>
<summary>🪟 On Windows</summary>

Unzip the NeuroTrack-Windows.zip file.

Double-click on main_app.exe to launch the dashboard. That's it!

</details>

<details>
<summary>🐧 On Ubuntu/Linux</summary>

Unzip the NeuroTrack-Linux.zip file.

Open a terminal in the folder where you unzipped the files.

Make the application executable by running this command:

chmod +x main_app

Launch the dashboard by running:

./main_app

</details>

💻 Guide for Developers
This guide is for team members and contributors who want to run the application from the source code.

Prerequisites
Git

Python 3.8+

1. Clone the Repository
Open a terminal and clone the project to your local machine:

git clone [https://github.com/your-username/NeuroTrack.git](https://github.com/your-username/NeuroTrack.git)
cd NeuroTrack

2. Set Up & Activate the Virtual Environment
<details>
<summary>🪟 On Windows (PowerShell)</summary>

Create the environment:

python -m venv .venv

Activate it: (You may need to run Set-ExecutionPolicy RemoteSigned -Scope CurrentUser in an Admin PowerShell once if this fails).

.\.venv\Scripts\activate

Your terminal prompt will now start with (.venv).

</details>

<details>
<summary>🐧 On Ubuntu/Linux (Bash)</summary>

Create the environment:

python3 -m venv .venv

Activate it:

source .venv/bin/activate

Your terminal prompt will now start with (.venv).

</details>

3. Install Dependencies
Navigate into the application folder and install the required libraries:

cd desktop-app
pip install -r requirements.txt

4. Run the Application
Launch the NeuroTrack dashboard:

# On Windows
python main_app.py

# On Ubuntu/Linux
python3 main_app.py

📦 Building the Executable from Source
These instructions are for creating the standalone .exe or Linux executable.

1. Install PyInstaller
Make sure your virtual environment is active and run:

pip install pyinstaller

2. Run the Build Command
<details>
<summary>🪟 Building the .exe on Windows</summary>

Navigate to the desktop-app folder and run this command. Note the semicolon ; separator.

pyinstaller --onefile --windowed --add-data "assets;assets" main_app.py

Your final main_app.exe will be in the desktop-app/dist/ folder.

</details>

<details>
<summary>🐧 Building the Executable on Ubuntu/Linux</summary>

Navigate to the desktop-app folder and run this command. Note the colon : separator.

pyinstaller --onefile --windowed --add-data "assets:assets" main_app.py
