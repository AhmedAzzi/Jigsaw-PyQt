from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout,  QLabel, QPushButton, QStackedWidget, QWidget)
from PyQt5.QtCore import Qt


class About(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.m_stackedWidget = QStackedWidget(self)

        self.setFixedSize(500, 500)
        self.setWindowTitle("About")
        self.setupAboutPanel()
        self.setupInstructionPanel()

        self.m_stackedWidget.addWidget(self.m_aboutPanel)
        self.m_stackedWidget.addWidget(self.m_instructionPanel)

        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)
        mainLayout.addWidget(self.m_stackedWidget)
        self.setLayout(mainLayout)

        self.m_stackedWidget.setCurrentWidget(self.m_aboutPanel)
        self.setFrameStyle(QFrame.NoFrame)

    def setupAboutPanel(self):
        self.m_aboutPanel = QWidget(self)
        self.m_aboutPanel.setStyleSheet("background-color: #c5935e;")

        titleLabel = self.createStyledLabel(self.getAboutText())
        helpButton = self.createStyledButton("Help?")
        helpButton.clicked.connect(self.showInstructionPanel)

        layout = QVBoxLayout(self.m_aboutPanel)
        layout.addWidget(titleLabel, 0, Qt.AlignCenter)
        layout.addWidget(helpButton, 0, Qt.AlignCenter)
        self.m_aboutPanel.setLayout(layout)

    def setupInstructionPanel(self):
        self.m_instructionPanel = QWidget(self)
        self.m_instructionPanel.setStyleSheet("background-color: #c5935e;")

        instructionLabel = self.createStyledLabel(self.getInstructionText())
        backButton = self.createStyledButton("Back")
        backButton.clicked.connect(self.showAboutPanel)

        layout = QVBoxLayout(self.m_instructionPanel)
        layout.addWidget(instructionLabel, 0, Qt.AlignCenter)
        layout.addWidget(backButton, 0, Qt.AlignCenter)
        self.m_instructionPanel.setLayout(layout)

    def createStyledLabel(self, text):
        label = QLabel(self)
        label.setText(text)
        label.setStyleSheet(
            "font-family: Z003, sans-serif; font-size: 20px; color: black;")
        label.setAlignment(Qt.AlignCenter)
        label.setFixedSize(360, 400)
        return label

    def createStyledButton(self, text):
        button = QPushButton(text, self)
        button.setStyleSheet(
            "color: black; font-family: Z003, sans-serif; font-size: 18px;")
        button.setFixedSize(100, 30)
        return button

    def showInstructionPanel(self):
        self.m_stackedWidget.setCurrentWidget(self.m_instructionPanel)

    def showAboutPanel(self):
        self.m_stackedWidget.setCurrentWidget(self.m_aboutPanel)

    def getAboutText(self):
        return ("𝕵𝖎𝖌𝖘𝖆𝖜 𝕳𝕾𝕽\n"
                "𝖁𝖊𝖗𝖘𝖎𝖔𝖓 : 1.0\n"
                "𝕮𝖗𝖊𝖆𝖙𝖎𝖔𝖓 𝕯𝖆𝖙𝖊: May 29, 2023\n"
                "This puzzle game was created using Qt C++.\n"
                "Développeur : Ahmed Azzi\n"
                "Date de création : 5 Jul 2024\n"
                "Ce jeu de puzzle a été créé avec PyQt.\n"
                "Amusez-vous bien !")

    def getInstructionText(self):
        return ("𝕵𝖎𝖌𝖘𝖆𝖜 𝕳𝕾𝕽 - 𝕲𝖆𝖒𝖊 𝕴𝖓𝖘𝖙𝖗𝖚𝖈𝖙𝖎𝖔𝖓𝖘\n\n"
                "• Move puzzle pieces by clicking on them with the mouse.\n"
                "• The goal is to reassemble the image by swapping the pieces in the correct order.\n"
                "• Use the 'Back' button to go back to the levels interface.\n"
                "• Pause the game by clicking the pause button.\n"
                "• Use the reset button to restart the game at any time.\n"
                "• Finish the game by placing all the pieces in the correct order.\n"
                "• The game also ends if you close the game window.")


if __name__ == '__main__':
    import main
    main.main()
