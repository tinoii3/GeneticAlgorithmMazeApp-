# styles.py
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel

class AppStyles:
    @staticmethod
    def apply_dark_theme(app):
        palette = app.palette()
        palette.setColor(QPalette.Window, QColor(46, 52, 64))
        palette.setColor(QPalette.WindowText, QColor(216, 222, 233))
        palette.setColor(QPalette.Base, QColor(59, 66, 82))
        palette.setColor(QPalette.AlternateBase, QColor(67, 76, 94))
        palette.setColor(QPalette.Button, QColor(67, 76, 94))
        palette.setColor(QPalette.ButtonText, QColor(216, 222, 233))
        palette.setColor(QPalette.Highlight, QColor(136, 192, 208))
        palette.setColor(QPalette.HighlightedText, QColor(46, 52, 64))
        app.setPalette(palette)

        app.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QPushButton {
                border: 2px solid #4C566A;
                border-radius: 5px;
                padding: 10px 20px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #5E81AC;
            }
            QLabel#title {
                font-size: 32px;
                font-weight: 600;
                color: #88C0D0;
            }
            QSpinBox, QDoubleSpinBox, QLineEdit {
                background-color: #3B4252;
                color: #ECEFF4;
                border: 1px solid #4C566A;
                padding: 5px;
                min-width: 200px;
            }
        """)