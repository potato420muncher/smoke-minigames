import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt6.QtCore import QTimer

from PyQt6.QtCore import Qt, QRect, QPoint
from PyQt6.QtGui import QPainter, QColor

from games.menu import Menu

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()

    menu = Menu()

    window.setBaseSize(400, 600)
    window.setMaximumSize(400, 600)
    window.setMinimumSize(400, 600)
    window.setCentralWidget(menu)
    window.setWindowTitle("Minigames")

    app.setActiveWindow(window)

    window.show()
    sys.exit(app.exec())