import sys
import numpy as np
import random
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class ModelCreationPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        QLocale.setDefault(QLocale("en_US"))
        self.parent = parent
        self.init_ui()
        self.load_styles()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 20, 0, 20)  # ปรับ margin บน-ล่าง
        self.layout.setSpacing(30)

        # Header Section
        self.header = QWidget()
        self.header.setFixedHeight(100)  # ลดความสูง header
        header_layout = QVBoxLayout(self.header)
        
        title_label = QLabel("Maze Configuration")
        title_label.setObjectName("configTitle")
        
        header_layout.addStretch()
        header_layout.addWidget(title_label, alignment=Qt.AlignCenter)
        header_layout.addStretch()

        # Form Section
        self.form_widget = QWidget()
        form_layout = QFormLayout(self.form_widget)
        form_layout.setVerticalSpacing(25)  # ระยะห่างระหว่างแถว
        form_layout.setContentsMargins(50, 25, 50, 25)  # ระยะห่างภายในฟอร์ม
        form_layout.setLabelAlignment(Qt.AlignRight)  # จัด label ชิดขวา

        # Input Fields
        self.pop_size = self.create_input_field(QSpinBox(), 10, 1000)
        self.grid_size = self.create_input_field(QSpinBox(), 11, 25)
        self.mutation_rate = self.create_input_field(QDoubleSpinBox(), 0.1, 1.0)
        self.generation_limit = self.create_input_field(QSpinBox(), 50, 1000)
        self.mutation_rate.setSingleStep(0.05)

        # เพิ่ม label style
        form_layout.addRow(QLabel("Population Size:"), self.pop_size)
        form_layout.addRow(QLabel("Grid Size:"), self.grid_size)
        form_layout.addRow(QLabel("Mutation Rate:"), self.mutation_rate)
        form_layout.addRow(QLabel("Generation Limit:"), self.generation_limit)

        # Button Section
        button_container = QWidget()
        button_layout = QVBoxLayout(button_container)
        button_layout.setSpacing(15)
        button_layout.setContentsMargins(0, 10, 0, 10)

        self.btn_start = QPushButton("Start Evolution")
        self.btn_back = QPushButton("Back to Menu")
        
        for btn in [self.btn_start, self.btn_back]:
            btn.setObjectName("formBtn")
            btn.setFixedSize(300, 50)  # ปรับขนาดปุ่มให้ใหญ่ขึ้น

        button_layout.addWidget(self.btn_start)
        button_layout.addWidget(self.btn_back)

        # Layout Organization
        self.layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.layout.addWidget(self.header, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.form_widget, alignment=Qt.AlignCenter)
        self.layout.addWidget(button_container, alignment=Qt.AlignCenter)
        self.layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(self.layout)

        # Connect Signals
        self.btn_start.clicked.connect(self.start_evolution)
        self.btn_back.clicked.connect(lambda: self.parent.stacked_widget.setCurrentIndex(0))

    def create_input_field(self, field, min_val, max_val):
        field.setRange(min_val, max_val)
        field.setAlignment(Qt.AlignCenter)
        field.setFixedSize(250, 45)
        field.setStyleSheet("font-size: 16px;")
        
        # ตั้งค่า Locale ให้กับ Widget โดยตรง
        field.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        
        # สำหรับ QDoubleSpinBox ตั้งค่าตัวเลขเป็นรูปแบบภาษาอังกฤษ
        if isinstance(field, QDoubleSpinBox):
            field.setDecimals(2)
            field.setSingleStep(0.05)
            field.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        
        return field

    def load_styles(self):
        self.setStyleSheet("""
            QLabel#configTitle {
                font-size: 32px;
                font-weight: 300;
                letter-spacing: 2px;
            }
            QPushButton#formBtn {
                background-color: #3B4252;
                color: #ECEFF4;
                border: 2px solid #4C566A;
                border-radius: 8px;
                font-size: 18px;
                min-width: 300px;
                padding: 12px 25px;
            }
            QPushButton#formBtn:hover {
                background-color: #434C5E;
                border-color: #5E81AC;
            }
            QSpinBox, QDoubleSpinBox {
                background-color: #3B4252;
                color: #ECEFF4;
                border: 1px solid #4C566A;
                padding: 8px 20px;
                font-size: 16px;
                border-radius: 6px;
            }
            QLabel {
                font-size: 16px;
                color: #D8DEE9;
                padding-right: 15px;
            }
        """)

    def start_evolution(self):
        params = {
            'pop_size': self.pop_size.value(),
            'grid_size': self.grid_size.value(),
            'mutation_rate': self.mutation_rate.value(),
            'generation_limit': self.generation_limit.value()
        }
        self.parent.stacked_widget.setCurrentIndex(2)
        self.parent.maze_page.initialize(params)
