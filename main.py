import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QComboBox, QLabel, QPushButton
from moviepy.video.io.VideoFileClip import VideoFileClip

class VideoSegmenter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Video Segmenter')
        self.setGeometry(100, 100, 500, 300)

        # Create widgets
        self.choose_button = QPushButton('Choose Video', self)
        self.choose_button.setGeometry(50, 50, 200, 50)

        self.segment_label = QLabel('Choose segment ratio:', self)
        self.segment_label.setGeometry(50, 120, 200, 20)

        self.segment_combo = QComboBox(self)
        self.segment_combo.setGeometry(50, 150, 200, 30)
        self.segment_combo.addItems(['25%', '33%', '50%', '66%', '75%'])

        self.segment_button = QPushButton('Segment Video', self)
        self.segment_button.setGeometry(50, 200, 200, 50)

        # Connect signals and slots
        self.choose_button.clicked.connect(self.choose_video)
        self.segment_button.clicked.connect(self.segment_video)

        # Initialize variables
        self.video_path = None
        self.segment_ratio = 0.25

    def choose_video(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter('Videos (*.mp4 *.avi *.mov)')
        if file_dialog.exec_():
            self.video_path = file_dialog.selectedFiles()[0]
            QMessageBox.information(self, 'Video Selected', f'You have selected:\n{self.video_path}')

    def segment_video(self):
        if not self.video_path:
            QMessageBox.warning(self, 'No Video Selected', 'Please select a video to segment.')
            return

        self.segment_ratio = float(self.segment_combo.currentText().strip('%')) / 100

        video_name = os.path.splitext(os.path.basename(self.video_path))[0]
        video = VideoFileClip(self.video_path)

        segments_dir = os.path.join(os.path.dirname(self.video_path), f'{video_name}_segments')
        os.makedirs(segments_dir, exist_ok=True)

        total_duration = video.duration
        segment_duration = total_duration * self.segment_ratio

        for i in range(int(1/self.segment_ratio)):
            start_time = segment_duration * i
            end_time = segment_duration * (i+1)

            segment_name = f'{video_name}_segment{i+1}.mp4'
            segment_path = os.path.join(segments_dir, segment_name)

            video.subclip(start_time, end_time).write_videofile(segment_path)

        QMessageBox.information(self, 'Video Segmented', f'Your video has been segmented into {i+1} segments.')

# Run the application
if __name__ == '__main__':
    app = QApplication([])
    window = VideoSegmenter()
    window.show()
    app.exec_()
