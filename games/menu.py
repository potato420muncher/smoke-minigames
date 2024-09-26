from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame, QHBoxLayout
from PyQt6.QtCore import QTimer

from PyQt6.QtCore import Qt, QRect, QPoint
from PyQt6.QtGui import QPainter, QColor, QIcon, QPixmap


class Menu(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 600)

        self.setStyleSheet("background-color: #2e2e2e;")  # Dark grey background

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        self.layout.setSpacing(0)  # Remove spacing between widgets

        title_label = QLabel("Smoke Mini-Games")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")  # White text
        self.layout.addWidget(title_label)

        # Create a scroll area
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none;")  # Remove border around scroll area

        # Create a frame to hold the buttons 
        button_frame = QFrame()
        button_layout = QVBoxLayout(button_frame)
        button_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins from button layout
        button_layout.setSpacing(10)  # Optional: add spacing between buttons

        # Create the Colorshifter button with an image
        play_button = QPushButton()
        play_button.setStyleSheet("background-color: #444444; color: white;")  # Dark button
        play_button.setFixedHeight(50)

       # Create a horizontal layout for the button content
        button_content = QHBoxLayout()
        button_content.setContentsMargins(0, 0, 0, 0)  # Remove margins from button content
        button_layout.setSpacing(5)  # Optional: add spacing between buttons

        # Add image to the button
        image_label = QLabel()
        pixmap = QPixmap("resources/colorshifter_icon.png")  # Path to your image
        pixmap = pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio)  # Resize the image
        image_label.setPixmap(pixmap)
        button_content.addWidget(image_label)

        # Add button text next to the image
        button_text = QLabel("Colorshifter")
        button_text.setStyleSheet("color: white; font-size: 16px;")  # Text styling
        button_content.addWidget(button_text)

        play_button.setLayout(button_content)  # Set the layout for the button
        play_button.clicked.connect(self.start_colorshifter)

        button_layout.addWidget(play_button)


        # Set the frame as the scroll area's widget
        scroll_area.setWidget(button_frame)
        self.layout.addWidget(scroll_area)

        self.setLayout(self.layout)

    def start_colorshifter(self):
        from games.colorshifter.menu_cs import MenuCs  # Lazy import
        self.start_menu(MenuCs)

    def start_menu(self, menu_class):
        
        self.next = menu_class()
        self.clearFocus()
        self.next.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.next.setFocus()
        self.parent().setCentralWidget(self.next)
