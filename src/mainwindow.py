import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QIcon, QColor, QPalette
from PyQt5.QtCore import Qt, QFile, QTextStream, QDir, QStandardPaths, QSize

from setlevel import SetLevel  # Replace with actual import
from gifdisplay import GifDisplay  # Replace with actual import
from about import About  # Replace with actual import
from resources_rc import *  # Import the resources_rc module


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.bg = QLabel("", self)
        self.logo = QLabel("", self)
        self.start = None
        self.demo = None
        self.about = None
        self.exit = None

        self.setupUi()
        self.setupFiles()

    def setupUi(self):
        self.setWindowTitle("Main Window")
        self.setFixedSize(700, 560)

        homeDir = QDir.homePath()
        bestTimeDirPath = os.path.join(homeDir, "best_time")

        # Ensure the directory exists
        if not QDir(bestTimeDirPath).exists():
            if not QDir().mkpath(bestTimeDirPath):
                print("Failed to create directory:", bestTimeDirPath)

        filePath = os.path.join(bestTimeDirPath, "best_time.txt")

        # Check if the file exists; if not, create it with default values
        if not QFile.exists(filePath):
            file = QFile(filePath)
            if file.open(QFile.WriteOnly | QFile.Text):
                out = QTextStream(file)
                out << "easy:30\n"
                out << "medium:60\n"
                out << "hard:90\n"
                out << "so hard:120\n"
                file.close()
            else:
                print("Failed to open file for writing:", file.errorString())

        self.setCentralWidget(self.bg)

        bg_img = QPixmap(":/bg4.jpg")
        if not bg_img.isNull():
            self.bg.setPixmap(bg_img.scaledToWidth(
                400, Qt.SmoothTransformation))
        else:
            print("Failed to load image")

        logo_img = QPixmap(":/icon.png")
        if not logo_img.isNull():
            self.logo.setPixmap(logo_img.scaledToWidth(
                240, Qt.SmoothTransformation))
            self.logo.setGeometry(3 * self.width() // 5,
                                  50, 240, 230)  # Ensure integer values
        else:
            print("Failed to load image")

        self.start = QPushButton(self)
        self.start.setIcon(QIcon(":/start2.png"))
        self.start.setStyleSheet("border: none; background: transparent;")

        self.start.setIconSize(QSize(280, 200))
        self.start.setFixedSize(120, 60)
        self.start.setCursor(Qt.PointingHandCursor)
        self.start.move(self.width() - 220, 320 - 40)
        self.start.clicked.connect(lambda: self.on_start_clicked())

        self.demo = QPushButton(self)
        self.demo.setIcon(QIcon(":/demo.png"))
        self.demo.setStyleSheet("border: none; background: transparent;")
        self.demo.setIconSize(QSize(280, 200))
        self.demo.setFixedSize(120, 60)
        self.demo.setCursor(Qt.PointingHandCursor)
        self.demo.move(self.width() - 220, 320 - 40 + 60)
        self.demo.clicked.connect(lambda: self.on_demo_clicked())

        self.about = QPushButton(self)
        self.about.setIcon(QIcon(":/about.png"))
        self.about.setStyleSheet("border: none; background: transparent;")
        self.about.setIconSize(QSize(280, 200))
        self.about.setFixedSize(120, 60)
        self.about.setCursor(Qt.PointingHandCursor)
        self.about.move(self.width() - 220, 320 - 40 + 60 * 2)
        self.about.clicked.connect(lambda: self.on_about_clicked())

        self.exit = QPushButton(self)
        self.exit.setIcon(QIcon(":/exit.png"))
        self.exit.setStyleSheet("border: none; background: transparent;")
        self.exit.setIconSize(QSize(280, 200))
        self.exit.setFixedSize(120, 60)
        self.exit.setCursor(Qt.PointingHandCursor)
        self.exit.move(self.width() - 220, 320 - 40 + 60 * 3)
        self.exit.clicked.connect(lambda: self.close())

    def setupFiles(self):
        pass  # Optionally handle any file setup logic here

    def on_start_clicked(self):
        # pass
        self.set_level = SetLevel()
        self.set_level.show()
        self.close()

    def on_demo_clicked(self):

        self.gif_window = GifDisplay(":/demo4.gif", None)
        # self.gif_window.setAttribute(Qt.WA_DeleteOnClose)
        self.gif_window.show()

    def on_about_clicked(self):
        # pass
        self.about_window = About(None)
        self.about_window.show()

    def closeEvent(self, event):
        # Optionally handle any cleanup or confirmation logic here
        super().closeEvent(event)


if __name__ == '__main__':
    import main
    main.main()
