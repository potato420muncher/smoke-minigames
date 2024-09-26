from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame, QSpacerItem, QSizePolicy
from PyQt6.QtCore import QTimer

from PyQt6.QtCore import Qt, QRect, QPoint
from PyQt6.QtGui import QPainter, QColor


class MenuCs(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 600)
        self.setStyleSheet("background-color: #2e2e2e;")  # Dark grey background

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        self.layout.setSpacing(0)  # Remove spacing between widgets

        title_label = QLabel("Colorshifter")
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


        # Spacer between Normal and Shuffled buttons
        spacer = QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        button_layout.addItem(spacer)

        # Play normal button
        play_button = QPushButton("Normal")
        play_button.setStyleSheet("background-color: #444444; color: white;")  # Dark button
        play_button.setFixedHeight(50)
        play_button.clicked.connect(self.start_normal_game)
        button_layout.addWidget(play_button)

        # Play shuffled button
        play_button_s = QPushButton("Shuffled")
        play_button_s.setStyleSheet("background-color: #444444; color: white;")  # Dark button
        play_button_s.setFixedHeight(50)
        play_button_s.clicked.connect(self.start_shuffled_game)
        button_layout.addWidget(play_button_s)

        # Add a spacer to push the return button to the bottom
        button_layout.addStretch()  # Add stretchable space to push the next item down

        # Menu button
        menu_b = QPushButton("Return to menu")
        menu_b.setStyleSheet("background-color: #444444; color: white;")  # Dark button
        menu_b.setFixedHeight(50)
        menu_b.clicked.connect(self.return_to_menu)
        button_layout.addWidget(menu_b)


        # Set the frame as the scroll area's widget
        button_frame.setLayout(button_layout)
        scroll_area.setWidget(button_frame)
        self.layout.addWidget(scroll_area)

        self.setLayout(self.layout)

    def start_normal_game(self):
        from .normal_cs import NormalCs  # Lazy import
        self.start_game(NormalCs)

    def start_shuffled_game(self):
        from .shuffled_cs import ShuffledCs  # Lazy import
        self.start_game(ShuffledCs)

    def start_game(self, game_class):
        self.game = game_class()
        self.clearFocus()
        self.game.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.game.setFocus()
        self.parent().setCentralWidget(self.game)


    def return_to_menu(self) :
        self.clearFocus()

        from games.menu import Menu # Lazy import
        self.menu = Menu()

        self.menu.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.menu.setFocus()  # Set focus to game widget
        self.parent().setCentralWidget(self.menu)  # Change central widget to game