import sys
import random
import os
from PyQt5.QtCore import Qt, QTimer, QPoint, QUrl, QSize, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import QIcon, QPixmap, QMovie
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QRadioButton, QVBoxLayout, QGridLayout, QMessageBox
from PyQt5.QtMultimedia import QSoundEffect
from functools import partial


class PuzzlePanel(QWidget):
    def __init__(self, dim, name, seconds, parent=None):
        super().__init__(parent)
        self.firstClick = False
        self.lastClicked = None
        self.name = name
        self.remainingTime = seconds
        self.startingTime = seconds
        self.dim = dim
        self.beep = QSoundEffect(self)
        self.winner = QSoundEffect(self)
        self.buttons = []
        self.solution = []

        self.setFixedSize(QApplication.primaryScreen().geometry(
        ).width(), QApplication.primaryScreen().geometry().height())

        image = QPixmap(name)
        self.img_preview = QLabel(self)
        self.img_preview.setGeometry(
            QApplication.primaryScreen().geometry().width() - 310, 60, 280, 180)
        self.img_preview.setPixmap(image.scaled(
            280, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.back = QPushButton(self)
        self.back.setIcon(QIcon(":/back.png"))
        self.back.setStyleSheet("border: none; background: transparent;")
        self.back.setIconSize(QSize(250, 180))
        self.back.setFixedSize(100, 60)
        self.back.setCursor(Qt.PointingHandCursor)
        self.back.move(0, 0)
        self.back.clicked.connect(self.go_back)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

        self.timerLabel = QLabel(self.format_time(seconds), self)
        self.timerLabel.setStyleSheet(
            "font-size: 30px; font-family: Z003; color: black; background: transparent;")
        self.timerLabel.setGeometry(self.width() // 3 - 200, 0, 400, 50)
        self.timerLabel.setAlignment(Qt.AlignCenter)

        difficulty_map = {
            3: "easy",
            4: "medium",
            5: "hard",
            6: "so hard"
        }

        home_dir = os.path.expanduser("~")
        file_path = os.path.join(home_dir, "best_time/best_time.txt")

        number = 0
        try:
            with open(file_path, "r") as file:
                for line in file:
                    parts = line.strip().split(":")
                    if len(parts) == 2 and parts[0].strip() == difficulty_map.get(dim):
                        number = int(parts[1].strip())
                        break
        except FileNotFoundError:
            print("Failed to open file")

        self.lastTime = QLabel(f"Less Elapsed Time: {number}", self)
        self.lastTime.setStyleSheet(
            "font-size: 30px; font-family: Z003; color: black; background: transparent;")
        self.lastTime.setGeometry(2 * self.width() // 3 - 200, 0, 400, 50)
        self.lastTime.setAlignment(Qt.AlignCenter)

        self.setStyleSheet("""
            QRadioButton::indicator {
                width: 60px;
                height: 60px;
            }
            QRadioButton::indicator::unchecked {
                image: url(:/pause.png);
            }
            QRadioButton::indicator::checked {
                image: url(:/play.png);
            }
            * {
                background-color: #d3c3b6;
            }
        """)

        self.pause = QRadioButton("", self)
        self.pause.setGeometry(self.width() - self.pause.width(), 5, 40, 40)
        self.pause.setCursor(Qt.PointingHandCursor)
        self.pause.setStyleSheet("border: none; margin-left: -10px;")
        self.pause.toggled.connect(self.toggle_pause)

        self.reset = QPushButton(self)
        self.reset.setIcon(QIcon(":/reset.png"))
        self.reset.setStyleSheet("border: none;")
        self.reset.setIconSize(QSize(60, 60))
        self.reset.setGeometry(
            int(self.width() - self.reset.width() * 1.5), 5, 40, 40)
        self.reset.setCursor(Qt.PointingHandCursor)
        self.reset.clicked.connect(self.reset_game)

        self.one = QLabel("", self)
        self.one.setGeometry(QApplication.primaryScreen(
        ).geometry().width() - 250, 260, 280, 200)
        one_img = QPixmap(":/01.png")
        self.one.setAttribute(Qt.WA_TranslucentBackground)
        self.one.setPixmap(one_img.scaled(
            280, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.two = QLabel("", self)
        self.two.setGeometry(QApplication.primaryScreen(
        ).geometry().width() - 320, 470, 280, 200)
        two_img = QPixmap(":/02.png")
        self.two.setAttribute(Qt.WA_TranslucentBackground)
        self.two.setPixmap(two_img.scaled(
            280, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.three = QLabel("", self)
        self.three.setGeometry(QApplication.primaryScreen(
        ).geometry().width() - 160, 470, 280, 200)
        three_img = QPixmap(":/03.png")
        self.three.setAttribute(Qt.WA_TranslucentBackground)
        self.three.setPixmap(three_img.scaled(
            280, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.source = QPixmap(name)
        self.resized = self.source.scaled(
            860, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.layout = QGridLayout()

        for i in range(dim * dim):
            w = i // dim
            col = i % dim
            self.solution.append(QPoint(w, col))

        piece_width = self.resized.width() // dim
        piece_height = self.resized.height() // dim

        for i in range(dim * dim):
            x = i % dim
            y = i // dim
            image = self.resized.copy(
                x * piece_width, y * piece_height, piece_width, piece_height)

            button = QPushButton(self)
            button.setIcon(QIcon(image))
            button.setIconSize(QSize(piece_width, piece_height))
            button.setFixedSize(piece_width, piece_height)
            button.setStyleSheet("QPushButton { border: none; padding: 0px; }")
            button.setProperty("position", QPoint(y, x))
            button.setCursor(Qt.PointingHandCursor)
            button.clicked.connect(self.handle_click)
            self.buttons.append(button)

        random.shuffle(self.buttons)

        for r in range(dim):
            for c in range(dim):
                index = r * dim + c
                if index < len(self.buttons):
                    self.layout.addWidget(self.buttons[index], r, c)

        self.container = QWidget(self)
        self.container.setLayout(self.layout)
        self.container.setStyleSheet("background: transparent;")
        self.container.setContentsMargins(0, 0, 0, 0)
        self.container.setFixedSize(int(dim * 1.2 * piece_width),
                                    int(dim * piece_height * 1.2))
        self.container.move(QApplication.primaryScreen().geometry().width(
        ) // 100, QApplication.primaryScreen().geometry().height() // 10)

    def go_back(self):
        from setlevel import SetLevel
        self.set_level = SetLevel()
        self.set_level.show()
        self.close()

    def toggle_pause(self, checked):
        if checked:
            self.timer.stop()
            for btn in self.buttons:
                btn.setEnabled(False)
        else:
            self.timer.start(1000)
            for btn in self.buttons:
                btn.setEnabled(True)

    def reset_game(self):
        self.remainingTime = self.startingTime
        self.timerLabel.setText(self.format_time(self.remainingTime))
        self.timer.start(1000)
        for btn in self.buttons:
            btn.setEnabled(True)

        random.shuffle(self.buttons)

        for r in range(self.dim):
            for c in range(self.dim):
                index = r * self.dim + c
                if index < len(self.buttons):
                    self.layout.addWidget(self.buttons[index], r, c)

    def handle_click(self):
        button = self.sender()
        button_index = self.buttons.index(button)

        self.beep.setSource(QUrl.fromLocalFile(":/beep2.wav"))
        self.beep.play()

        if self.firstClick:
            self.buttons[button_index], self.buttons[self.lastClicked] = self.buttons[self.lastClicked], self.buttons[button_index]
            self.layout.removeWidget(self.buttons[button_index])
            self.layout.removeWidget(self.buttons[self.lastClicked])
            for btn in self.buttons:
                btn.setEnabled(False)
            for r in range(self.dim):
                for c in range(self.dim):
                    index = r * self.dim + c
                    if index < len(self.buttons):
                        self.layout.addWidget(self.buttons[index], r, c)
                        self.buttons[index].setEnabled(True)

            self.firstClick = False
        else:
            self.firstClick = True
            self.lastClicked = button_index

        if self.is_solved():
            self.winner.setSource(QUrl.fromLocalFile(":/winner.wav"))
            self.winner.play()
            self.winner.setLoopCount(3)

            self.timer.stop()

            self.reset.setEnabled(False)
            self.pause.setEnabled(False)

            difficulty_map = {3: "easy", 4: "medium", 5: "hard", 6: "so hard"}
            new_value = self.startingTime - self.remainingTime
            target_difficulty = difficulty_map.get(self.dim, "unknown")

            file_path = os.path.expanduser("~/best_time/best_time.txt")

            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Read existing file or create empty list
            try:
                with open(file_path, 'r') as file:
                    lines = file.readlines()
            except FileNotFoundError:
                lines = []

            # Update or add new best time
            updated = False
            for i, line in enumerate(lines):
                if line.startswith(f"{target_difficulty}:"):
                    current_value = int(line.split(':')[1].strip())
                    if new_value < current_value:
                        lines[i] = f"{target_difficulty}:{new_value}\n"
                    updated = True
                    break

            if not updated:
                lines.append(f"{target_difficulty}:{new_value}\n")

            # Write updated lines back to file
            with open(file_path, 'w') as file:
                file.writelines(lines)

            # self.container.hide()
            container = QWidget(self)
            container.setFixedSize(self.container.size())
            container.setGeometry(self.container.geometry())

            imageLabel = QLabel(container)
            imageLabel.setPixmap(QPixmap(self.name).scaled(
                950, 580, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            imageLabel.setAlignment(Qt.AlignCenter)
            imageLabel.setFixedSize(950, 580)
            imageLabel.setStyleSheet("background: transparent")
            imageLabel.setGeometry(40, 0, 950, 580)

            gifLabel = QLabel(container)
            gifMovie = QMovie("://bg.gif")
            gifLabel.setMovie(gifMovie)
            gifLabel.setAlignment(Qt.AlignCenter)
            gifLabel.setStyleSheet("background: transparent")
            gifLabel.setGeometry(40, 20, 950, 520)
            gifMovie.start()

            container.show()

            if ((self.dim == 3 and self.remainingTime >= 20) or
                    (self.dim == 4 and self.remainingTime >= 40) or
                    (self.dim == 5 and self.remainingTime >= 60) or
                    (self.dim == 6 and self.remainingTime >= 80)):

                self.moveAndScaleImage(self.one, QApplication.primaryScreen(
                ).geometry().width() - 250, 260, 400, 280, 1.75, 5000)

            elif ((self.dim == 3 and self.remainingTime >= 10) or
                  (self.dim == 4 and self.remainingTime >= 20) or
                  (self.dim == 5 and self.remainingTime >= 30) or
                    (self.dim == 6 and self.remainingTime >= 40)):
                self.moveAndScaleImage(self.two, QApplication.primaryScreen(
                ).geometry().width() - 320, 470, 400, 280, 1.75, 5000)

            elif ((self.dim == 3 and self.remainingTime >= 0) or
                  (self.dim == 4 and self.remainingTime >= 0) or
                  (self.dim == 5 and self.remainingTime >= 0) or
                    (self.dim == 6 and self.remainingTime >= 0)):
                self.moveAndScaleImage(
                    self.three, QApplication.primaryScreen().geometry().width() - 160, 470, 400, 280, 1.75, 5000)

            QTimer.singleShot(7000, partial(
                self.show_message_box, str(self.startingTime - self.remainingTime)))

    def show_message_box(self, number):
        msg_box = QMessageBox(self)
        msg_box.setText("You finished in " + number +
                        " secondes, Do you want to go next level?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.Yes)
        ret = msg_box.exec_()

        # Handle user's response
        if ret == QMessageBox.Yes:
            self.close()
            if self.dim < 6:
                self.reset.click()
                self.puzzle_panel = PuzzlePanel(
                    self.dim + 1, self.name, self.startingTime + 30)
                self.puzzle_panel.show()
                self.close()
        elif ret == QMessageBox.No:
            print("User clicked No")

    def moveAndScaleImage(self, icon, startX, startY, endX, endY, scaleFactor, duration):
        frames = duration // 10  # Number of frames based on the duration
        startWidth = icon.width()
        startHeight = icon.height()
        originalImage = icon.pixmap().toImage()
        icon.raise_()
        currentFrame = 0

        def updateFrame():
            nonlocal currentFrame
            if currentFrame <= frames:
                scale = 1.0 + (scaleFactor - 1.0) * currentFrame / frames
                width = int(startWidth * scale)
                height = int(startHeight * scale)
                scaledImage = originalImage.scaled(
                    width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                pixmap = QPixmap.fromImage(scaledImage)
                icon.setPixmap(pixmap)
                icon.resize(width, height)

                x = startX + (endX - startX) * currentFrame // frames
                y = startY + (endY - startY) * currentFrame // frames
                icon.move(x, y)

                currentFrame += 1
            else:
                timer.stop()

        timer = QTimer(self)
        timer.timeout.connect(updateFrame)
        timer.start(10)  # Adjust the interval to control the animation speed

    def is_solved(self):
        for button in self.buttons:
            position = button.property("position")
            index = self.buttons.index(button)
            correct_position = QPoint(index // self.dim, index % self.dim)
            if position != correct_position:
                return False
        return True

    def update_timer(self):
        self.remainingTime -= 1
        if self.remainingTime >= 0:
            self.timerLabel.setText(self.format_time(self.remainingTime))
        else:
            self.timer.stop()
            QMessageBox.information(
                self, "Time's Up", "You've run out of time!")

    def format_time(self, total_seconds):
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02}:{seconds:02}"


if __name__ == '__main__':
    import main
    main.main()
