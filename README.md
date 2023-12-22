
# Python Automation Toolkit

## Overview

This project consists of several Python scripts designed to automate various tasks.
Each script serves a specific purpose and can be used independently or in combination with others.

## Scripts

### 1. File Organizer

- **Description**: This script organizes files in the current directory into folders based on their file types (e.g., Images, Videos, Documents).
- **Usage**: Run the script in a directory to automatically sort all files into categorized folders.

### 2. Water Reminder

- **Description**: Sends random water drinking reminders at different times of the day using Pushbullet. It's designed to run on a regular schedule, which can be set up using a service like PythonAnywhere for continuous execution.
- **Dependencies**: Requires the `pushbullet.py` library and a valid Pushbullet API key.
- **Setup**:
  - Place your Pushbullet API key in the script.
  - Ensure you have the `Reminder to Drink Water.txt` file with quotes in the same directory.
  - This script can be run on your local machine or set up on a cloud platform like PythonAnywhere for automated scheduling.

### 3. Image Resizer

- **Description**: Resizes images in the current directory to a specified size and saves them in a designated output folder.
- **Usage**: Run the script, input the desired image size and output folder when prompted.

### 4. PDF to Audio Converter

- **Description**: Converts text from a PDF file into an audio MP3 file using text-to-speech technology. This script is useful for creating audiobooks or for auditory learning.
- **Usage**:
  - Run the script and input the path to the PDF file.
  - The script will process each page of the PDF and convert it into spoken words, saving the output as an MP3 file.
- **Dependencies**: Requires `pdfplumber` for PDF text extraction, `pyttsx3` for text-to-speech conversion, and `tqdm` for progress indication.
- **Setup**:
  - Ensure all dependencies are installed.

### Running on PythonAnywhere

PythonAnywhere is an online IDE and web hosting service based on Python. It allows you to run Python scripts continuously at scheduled intervals. Here's how to set up the Water Reminder script on PythonAnywhere:

1. **Create an Account**: Sign up for an account on [PythonAnywhere]
2. **Upload Your Script**: Upload the `water_reminder.py` script and the `Reminder to Drink Water.txt` file.
3. **Install Dependencies**: Use the Bash console on PythonAnywhere to install any required libraries.
4. **Schedule the Script**: Use PythonAnywhere's task scheduling feature to run your script at your desired frequency.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.
