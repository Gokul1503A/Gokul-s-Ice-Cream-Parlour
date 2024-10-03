import sys
import threading
import pygame
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QMessageBox, QVBoxLayout, QWidget
from record_audio import start_recording, stop_save
from speech_to_text import transcribe
from alia import StreamResponse

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        pygame.mixer.init()  # Initialize Pygame mixer once

    def init_ui(self):
        self.setWindowTitle('Ice Cream Shop')
        self.setGeometry(100, 100, 400, 350)

        # Layout and Widgets
        layout = QVBoxLayout()
        self.record_button = QPushButton("Record Now")
        self.record_button.clicked.connect(self.start_recording)
        layout.addWidget(self.record_button)

        self.stop_record_button = QPushButton("Stop and Send")
        self.stop_record_button.clicked.connect(self.stop_and_send)
        layout.addWidget(self.stop_record_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_recording(self):
        self.record_button.setEnabled(False)
        threading.Thread(target=start_recording).start()

    def stop_and_send(self):
        # Disable the button during processing
        self.stop_record_button.setEnabled(False)
        stop_save()
        QMessageBox.information(self, 'Message', 'Your message has been sent!')
        threading.Thread(target=self.get_text).start()

    def get_text(self):
        try:
            text = transcribe()
            print(text)
            StreamResponse(text)
            self.play_sound()
        except Exception as e:
            print(f"Error in GetText: {e}")
        finally:
            # Re-enable the button after processing
            self.record_button.setEnabled(True)
            self.stop_record_button.setEnabled(True)

    def play_sound(self):
        try:
            pygame.mixer.music.load('response.mp3')
            pygame.mixer.music.play()

        except Exception as e:
            print(f"Error playing sound: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
