# Real-Time Speech-to-Text Converter

## 📌 Overview
This project is a real-time speech-to-text converter using **Python, PyQt6, and OpenAI Whisper**. It captures live audio from the microphone, transcribes it into text, and displays the output in a user-friendly GUI.

## 🚀 Features
- **Real-Time Speech Recognition**: Converts speech into text instantly.
- **Whisper Model Integration**: Uses OpenAI's Whisper for high-accuracy transcription.
- **GUI with PyQt6**: User-friendly interface for ease of use.
- **Error Handling**: Manages microphone and network errors gracefully.

## 📂 Project Structure
```
Speech-to-Text/
│── app.py                # Main application script
│── requirements.txt      # Dependencies
│── README.md             # Project documentation
│── assets/               # Icons, images, and other assets
└── venv/                 # Virtual environment (not included in repo)
```

## 🛠️ Installation
### 1️⃣ Clone the Repository
```sh
git clone https://github.com/Charan3uu/Metasynk-Speech-to-text-converter.git
```

### 2️⃣ Create a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Install FFmpeg (Required for Whisper)
- **Windows**: Download FFmpeg from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/), extract, and add it to the system PATH.
- **Linux/macOS**: Install using a package manager:
  ```sh
  sudo apt install ffmpeg  # Ubuntu/Debian
  brew install ffmpeg      # macOS
  ```

## ▶️ Usage
Run the application:
```sh
python app.py
```
- Click **Start Listening** and begin speaking.
- The transcribed text appears in real time.
- Click **Stop** to terminate the session.

## 🛠 Troubleshooting
### 1️⃣ FFmpeg Errors
Ensure FFmpeg is installed and accessible via the command line:
```sh
ffmpeg -version
```
If not found, add it to your **system PATH**.

### 2️⃣ Permission Issues
If you see `Error opening input file: Permission denied`, manually set full access to the temp folder:
```sh
mkdir C:\Users\India\Desktop\temp_audio
setx TMPDIR C:\Users\India\Desktop\temp_audio
```
