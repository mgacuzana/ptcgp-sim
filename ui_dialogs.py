from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel

class InputErrorDialog(QDialog):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle("Input Error")

        # Create widgets
        self.label = QLabel(message)
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)

        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.ok_button)
        self.setLayout(layout)

class OpenPackDialog(QDialog):
    def __init__(self, cards):
        super().__init__()
        self.setWindowTitle("You Opened A Pack!")
        self.setGeometry(100, 100, 800, 600)

        # Create closing button
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)

        # Create vertical stack of all card names and put the ok button at the bottom
        layout = QVBoxLayout()
        for card in cards:
            layout.addWidget(QLabel(card.__str__()))

        layout.addWidget(self.ok_button)
        self.setLayout(layout)