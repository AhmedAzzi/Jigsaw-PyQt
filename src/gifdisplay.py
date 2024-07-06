from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, QMargins


class GifDisplay(QFrame):
    def __init__(self, gif_file_path, parent=None):
        super().__init__(parent)

        self.setWindowTitle("GIF Display Window")
        self.setFrameShape(QFrame.NoFrame)  # Remove frame border

        self.gif_label = QLabel(self)
        self.movie = QMovie(gif_file_path)
        self.gif_label.setMovie(self.movie)
        self.movie.start()

        # Set window size to match GIF size
        self.setFixedSize(self.movie.frameRect().size())

        # Create layout with no margins
        layout = QVBoxLayout()
        layout.setContentsMargins(QMargins(0, 0, 0, 0))  # Remove all margins
        layout.setSpacing(0)  # Remove spacing between widgets
        layout.addWidget(self.gif_label)
        self.setLayout(layout)

        # Ensure the label takes up the entire space
        self.gif_label.setScaledContents(True)

    def closeEvent(self, event):
        self.movie.stop()
        super().closeEvent(event)


if __name__ == '__main__':
    import main
    main.main()
