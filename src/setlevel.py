import os
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QRadioButton, QMessageBox, QFileDialog, QMainWindow
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QDir, QFileInfo, QCoreApplication, QSize


class SetLevel(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.dim = 3
        self.second = 30
        primary_screen_size = QApplication.primaryScreen().geometry().size()
        self.setFixedSize(primary_screen_size)
        self.intro = QLabel("Choose another Image Here", self)
        self.intro.setStyleSheet(
            "font-size: 30px; font-family: Z003; color: black;")
        self.intro.setGeometry(self.width() // 2 - 200,
                               20, 400, 50)  # Absolute positioning
        self.intro.setAlignment(Qt.AlignCenter)

        fileChooserButton = QPushButton(self)
        fileChooserButton.setIcon(QIcon(":/choose.png"))
        fileChooserButton.setStyleSheet(
            "border: none; background: transparent;")
        fileChooserButton.setIconSize(QSize(60, 60))
        fileChooserButton.setGeometry(
            self.width() // 2 + 150, 10, 100, 60)  # Absolute positioning
        fileChooserButton.setCursor(Qt.PointingHandCursor)
        fileChooserButton.clicked.connect(self.on_file_choose)

        self.imageLabel = QLabel(self)
        # Relative to imagePanel
        self.imageLabel.setGeometry(self.width() // 2 - 340, 60, 680, 480)
        self.imageLabel.setAlignment(Qt.AlignCenter)

        self.prevButton = QPushButton(self)
        self.prevButton.setIcon(QIcon(":/prev.png"))
        self.prevButton.setStyleSheet("border: none; background: transparent;")
        self.prevButton.setIconSize(QSize(80, 100))
        self.prevButton.setFixedSize(100, 100)
        self.prevButton.setCursor(Qt.PointingHandCursor)
        self.prevButton.move(self.width() // 2 - 500,
                             280)  # Absolute positioning
        self.prevButton.clicked.connect(self.on_prev_clicked)

        self.nextButton = QPushButton(self)
        self.nextButton.setIcon(QIcon(":/next.png"))
        self.nextButton.setStyleSheet("border: none; background: transparent;")
        self.nextButton.setIconSize(QSize(80, 100))
        self.nextButton.setFixedSize(100, 100)
        self.nextButton.setCursor(Qt.PointingHandCursor)
        self.nextButton.move(self.width() // 2 + 400,
                             280)  # Absolute positioning
        self.nextButton.clicked.connect(self.on_next_clicked)

        self.setStyleSheet(
            "QRadioButton {"
            "    font-size: 20px; font-family: Z003; color: black;"
            "    padding-left: 40px;"
            "}"
            "QRadioButton::indicator {"
            "    width: 30px;"
            "    height: 30px;"
            "}"
            "QRadioButton::indicator::unchecked {"
            "    image: url(:/r1_c.png);"
            "}"
            "QRadioButton::indicator::checked {"
            "    image: url(:/r1_o.png);"
            "}"
        )

        self.easy = QRadioButton("Easy\n3x3", self)
        self.easy.setChecked(True)
        self.easy.move(self.width() // 2 - 500, 550)  # Absolute positioning
        self.easy.setFixedSize(150, 60)
        self.easy.clicked.connect(self.on_easy_clicked)

        self.medium = QRadioButton("Medium\n4x4", self)
        self.medium.setStyleSheet(
            "font-size: 20px; font-family: Z003; color:black")
        self.medium.setFixedSize(150, 60)
        self.medium.move(self.width() // 2 - 200, 550)  # Absolute positioning
        self.medium.clicked.connect(self.on_medium_clicked)

        self.hard = QRadioButton("Hard\n5x5", self)
        self.hard.setStyleSheet(
            "font-size: 20px; font-family: Z003; color:black")
        self.hard.move(self.width() // 2 + 100, 550)  # Absolute positioning
        self.hard.setFixedSize(150, 60)
        self.hard.clicked.connect(self.on_hard_clicked)

        self.so_hard = QRadioButton("So Hard\n6x6", self)
        self.so_hard.setStyleSheet(
            "font-size: 20px; font-family: Z003; color:black")
        self.so_hard.move(self.width() // 2 + 400, 550)  # Absolute positioning
        self.so_hard.setFixedSize(150, 60)

        self.so_hard.clicked.connect(self.on_so_hard_clicked)

        self.play = QPushButton(self)
        self.play.setIcon(QIcon(":/play1.png"))
        self.play.setStyleSheet("border: none; background: transparent;")
        self.play.setIconSize(QSize(250, 180))
        self.play.setFixedSize(250, 60)
        self.play.setCursor(Qt.PointingHandCursor)
        self.play.move(3 * self.width() // 4 - 160,
                       620)  # Absolute positioning
        self.play.clicked.connect(self.on_play_clicked)

        self.back = QPushButton(self)
        self.back.setIcon(QIcon(":/back.png"))
        self.back.setStyleSheet("border: none; background: transparent;")
        self.back.setIconSize(QSize(250, 180))
        self.back.setFixedSize(250, 60)
        self.back.setCursor(Qt.PointingHandCursor)
        self.back.move(self.width() // 4 - 100, 620)  # Absolute positioning
        self.back.clicked.connect(self.on_back_clicked)

        self.imageFiles = [
            ":/cow.jpg",
            ":/dolphin.jpg",
            ":/Nasa.jpg"
        ]

        self.currentImage = 0
        self.load_image()

    def on_file_choose(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open Image", QDir.currentPath(), "Image Files (*.jpg *.jpeg *.png *.gif)")

        if fileName:
            if QFileInfo(fileName).size() < 1000000:
                self.imageFiles.append(fileName)
                self.currentImage = len(self.imageFiles) - 1
                pixmap = QPixmap(fileName)
                self.imageLabel.setPixmap(pixmap.scaled(
                    680, 480, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                QMessageBox.warning(self, "Image too Large",
                                    "Choose another one")

    def on_prev_clicked(self):
        self.currentImage -= 1
        if self.currentImage < 0:
            self.currentImage = len(self.imageFiles) - 1

        pixmap = QPixmap(self.imageFiles[self.currentImage])
        self.imageLabel.setPixmap(pixmap.scaled(
            680, 480, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def on_next_clicked(self):
        self.currentImage += 1
        if self.currentImage >= len(self.imageFiles):
            self.currentImage = 0

        pixmap = QPixmap(self.imageFiles[self.currentImage])
        self.imageLabel.setPixmap(pixmap.scaled(
            680, 480, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def on_easy_clicked(self):
        self.dim = 3
        self.second = 30

    def on_medium_clicked(self):
        self.dim = 4
        self.second = 60

    def on_hard_clicked(self):
        self.dim = 5
        self.second = 90

    def on_so_hard_clicked(self):
        self.dim = 6
        self.second = 120

    def on_play_clicked(self):
        from puzzlepanel import PuzzlePanel
        self.puzzle_panel = PuzzlePanel(
            self.dim, self.imageFiles[self.currentImage], self.second)
        self.puzzle_panel.show()
        self.close()

    def on_back_clicked(self):
        from mainwindow import MainWindow
        main_window = MainWindow()
        main_window.show()
        self.close()

    def load_image(self):
        pixmap = QPixmap(self.imageFiles[self.currentImage])
        self.imageLabel.setPixmap(pixmap.scaled(
            680, 480, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def closeEvent(self, event):
        super().closeEvent(event)


if __name__ == '__main__':
    import main
    main.main()
