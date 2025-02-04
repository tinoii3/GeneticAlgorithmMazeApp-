import sys
import numpy as np
import random
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from guide_page import GuidePage
from homepage import HomePage
from model_create import ModelCreationPage
from maze_page import MazePage

class GeneticAlgorithmApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Genetic Path Optimizer")
        self.setGeometry(100, 100, 1200, 800)
        self.setup_ui()
        self.set_style()

    def setup_ui(self):
        # ตั้งค่าโครงสร้างหลัก
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # สร้างหน้าต่างต่างๆ
        self.home_page = HomePage(self)
        self.model_page = ModelCreationPage(self)
        self.maze_page = MazePage(self)
        self.guide_page = GuidePage(self)
        #self.progress_page = ProgressPage(self)

        # เพิ่มหน้าต่างเข้า Stack
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.model_page)
        self.stacked_widget.addWidget(self.maze_page)
        self.stacked_widget.addWidget(self.guide_page)
        #self.stacked_widget.addWidget(self.progress_page)

    def set_style(self):
        # ตั้งค่า Style Sheet สำหรับการออกแบบเชิงธุรกิจ
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2E3440;
            }
            QPushButton {
                background-color: #434C5E;
                color: #ECEFF4;
                border-radius: 5px;
                padding: 10px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #4C566A;
            }
            QLabel {
                color: #D8DEE9;
            }
            QLineEdit, QSpinBox {
                background-color: #3B4252;
                color: #ECEFF4;
                border: 1px solid #4C566A;
                padding: 5px;
            }
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GeneticAlgorithmApp()
    window.show()
    sys.exit(app.exec_())