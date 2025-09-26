🧠 NeuroTrack: An EEG-Based Stress and Depression Analyzer
A B.Tech Final Year Project for the Department of Electronics & Communication Engineering at CSJM University.

Welcome to the official repository for the NeuroTrack project. Our goal is to build an accessible, real-time system for monitoring mental wellness through brainwave analysis.

📖 Table of Contents
🎯 About the Project

👥 Team Members

🛠️ Technology Stack

🚀 Getting Started: Wokwi Simulation

📋 Workflow & Roles for Team Members

📂 Project Structure

🎯 About the Project
NeuroTrack aims to develop a low-cost, non-invasive system for the real-time monitoring of mental health indicators such as anxiety, depression, and stress (ADS). The system will acquire and analyze EEG (brainwave) signals to provide objective, quantitative data, moving beyond traditional subjective assessment methods.

The core of our analysis is based on the Alpha-to-Beta brainwave ratio, a scientifically recognized indicator of a person's cognitive and emotional state.

👥 Team Members
Ashutosh Sharan Srivastava

Aditya Gupta

Sai Ujwal Ramula

Abhay Pratap Singh

Shefali Yadav

🛠️ Technology Stack
Component

Technology

Hardware

Raspberry Pi Pico

Sensor (Final)

BioAmp EXG Pill

Sensor (Sim)

Potentiometer

Firmware

C/C++ (using the Raspberry Pi Pico SDK)

Desktop App

Python 3.x with PyQt6 & PyQtGraph

Simulation

Wokwi Online Simulator

🚀 Getting Started: Wokwi Simulation
This section covers how to run the current simulation, which uses a potentiometer to generate a variable analog signal to test our data pipeline.

Prerequisites
Python: Ensure you have Python 3.8+ installed.

Required Libraries: Install the necessary Python packages using pip:

pip install pyserial pyqt6 pyqtgraph

Wokwi Project: You need access to our shared Wokwi project link.

Running the Full Simulation
Follow these steps in order:

Start Wokwi Simulation: Open the Wokwi project and press the "Start Simulation" button.

Run Python App: Navigate to the desktop-app directory in your local project folder and run the main application file from your terminal:

python main_app.py

View the Graph: The Python application window will appear. As you turn the potentiometer knob in Wokwi, you will see the graph on the desktop app move up and down in real-time.

📋 Workflow & Roles for Team Members
This section outlines our development process and assigns initial focus areas. All work should follow the Git workflow described at the end.

Initial Focus Areas:
Ashutosh (Team Lead & UI/UX):

Oversee the integration of all parts.

Lead the development of the Python desktop application's UI/UX (view.py) and application logic (controller.py).

Aditya (Algorithm Specialist):

Begin research and development of the Fast Fourier Transform (FFT) algorithm.

Focus on how to process the incoming data stream to extract frequency information.

Sai (Firmware Engineer):

Take ownership of the Pico firmware (sketch.cpp).

Ensure the potentiometer data is read cleanly and transmitted reliably over USB.

Abhay & Shefali (Hardware & Research):

Take the lead on the physical hardware setup when the components arrive.

Research the BioAmp EXG Pill, focusing on electrode placement for EEG and best practices for getting a clean signal.

Git Contribution Workflow:
Rule #1: Never commit directly to the main branch.

Create a Branch: For any new feature or fix, create a new branch from main.

# Example: git checkout -b feature/python-ui-update
git checkout -b <type>/<short-description>

Commit Your Work: Make your changes and commit them with clear, descriptive messages.

Push Your Branch: Push your new branch to the GitHub repository.

git push origin <your-branch-name>

Create a Pull Request (PR): Go to the GitHub repository and open a Pull Request to merge your branch into main.

Review & Merge: At least one other team member must review the PR before it is merged.

📂 Project Structure
The repository is organized into two main parts:

.
├── 펌 firmware-pico/      # All C/C++ code for the Raspberry Pi Pico
│   ├── sketch.cpp
│   └── CMakeLists.txt
│
└── 💻 desktop-app/        # Python application for data visualization
    ├── model.py        # Handles serial communication
    ├── view.py         # Defines the GUI layout (PyQt6)
    ├── controller.py   # Connects the model and view (app logic)
    └── main_app.py     # Entry point to run the application
