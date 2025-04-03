import sys
import os
import whisper
import speech_recognition as sr
import tempfile
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QTextEdit, QVBoxLayout
from PyQt6.QtCore import QThread, pyqtSignal

# Load Whisper model
model = whisper.load_model("base")

class SpeechToTextThread(QThread):
    text_signal = pyqtSignal(str)

    def run(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.text_signal.emit("Adjusting for ambient noise... Please wait.")
            recognizer.adjust_for_ambient_noise(source)
            self.text_signal.emit("Ready! Start speaking...")
            
            while True:
                try:
                    audio = recognizer.listen(source)
                    self.text_signal.emit("Processing speech...")
                    text = self.speech_to_text(audio)
                    self.text_signal.emit(text)
                except sr.UnknownValueError:
                    self.text_signal.emit("⚠️ Couldn't understand, please speak again.")
                except sr.RequestError:
                    self.text_signal.emit("❌ API unavailable or connection issue.")
                except Exception as e:
                    self.text_signal.emit(f"Error: {str(e)}")

    def speech_to_text(self, audio):
        try:
            # Create temp directory with appropriate permissions
            temp_dir = tempfile.mkdtemp()
            temp_file_path = os.path.join(temp_dir, "speech.wav")
            
            # Save audio data to file
            with open(temp_file_path, "wb") as f:
                f.write(audio.get_wav_data())
            
            # Transcribe using whisper
            result = model.transcribe(temp_file_path)
            
            # Clean up
            try:
                os.remove(temp_file_path)
                os.rmdir(temp_dir)
            except:
                pass
                
            return result["text"]
        except Exception as e:
            return f"Error during transcription: {str(e)}"

class SpeechToTextApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Real-Time Speech-to-Text")
        self.setGeometry(100, 100, 500, 400)

        self.label = QLabel("🎤 Click 'Start' and speak...", self)
        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)
        
        self.start_button = QPushButton("Start Listening", self)
        self.start_button.clicked.connect(self.start_listening)
        
        self.stop_button = QPushButton("Stop Listening", self)
        self.stop_button.clicked.connect(self.stop_listening)
        self.stop_button.setEnabled(False)
        
        self.clear_button = QPushButton("Clear Text", self)
        self.clear_button.clicked.connect(self.clear_text)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.text_area)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.clear_button)
        self.setLayout(layout)

    def start_listening(self):
        self.thread = SpeechToTextThread()
        self.thread.text_signal.connect(self.update_text)
        self.thread.start()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.label.setText("🔴 Listening...")

    def stop_listening(self):
        if hasattr(self, 'thread') and self.thread.isRunning():
            self.thread.terminate()
            self.thread.wait()  # Wait for the thread to properly terminate
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.label.setText("🎤 Click 'Start' and speak...")

    def update_text(self, text):
        self.text_area.append(text)
        # Auto-scroll to the bottom
        cursor = self.text_area.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.text_area.setTextCursor(cursor)

    def clear_text(self):
        self.text_area.clear()

    def closeEvent(self, event):
        # Clean up when closing the application
        self.stop_listening()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpeechToTextApp()
    window.show()
    sys.exit(app.exec())