import sys
import numpy as np
import random
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import time

class MazePage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.figure = None
        self.canvas = None
        self.initUI()
        self.load_styles()
    
    def initUI(self):
        # ใช้ QVBoxLayout หลัก
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(20)

        # Header Section
        self.header = QWidget(self)
        header_layout = QVBoxLayout(self.header)
        title_label = QLabel("Maze Solution")
        title_label.setObjectName("mazeTitle")
        header_layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # สร้าง Container สำหรับกราฟและข้อความ
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(20)

        # Canvas Area (ด้านซ้าย)
        self.canvas_widget = QWidget()
        self.canvas_widget.setFixedSize(550, 500)
        self.canvas_layout = QVBoxLayout(self.canvas_widget)
        self.canvas_widget.setStyleSheet("""
            background-color: #3B4252;
            border: 2px solid #4C566A;
            border-radius: 15px;
        """)
        
        # Text Box (ด้านขวา)
        self.text_box = QTextEdit()
        self.text_box.setFixedWidth(400)
        self.text_box.setFixedHeight(500)
        self.text_box.setObjectName("genText")
        self.text_box.setStyleSheet("""
            QTextEdit {
                background-color: #3B4252;
                border: 2px solid #4C566A;
                border-radius: 15px;
                padding: 15px;
                color: #D8DEE9;
                font-size: 14px;
            }
        """)

        # เพิ่ม Widget ลงใน Layout แนวนอน
        content_layout.addWidget(self.canvas_widget)
        content_layout.addWidget(self.text_box)

        # Control Button (อยู่นอกกรอบกราฟ)
        self.btn_back = QPushButton("Back to Configuration")
        self.btn_back.setObjectName("mazeBtn")
        self.btn_back.clicked.connect(lambda: self.parent.stacked_widget.setCurrentIndex(1))

        # เพิ่มทั้งหมดลง Layout หลัก
        main_layout.addWidget(self.header)
        main_layout.addWidget(content_widget, stretch=1)
        main_layout.addWidget(self.btn_back, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)
        

    def load_styles(self):
        # ปรับสไตล์ของ widget ต่างๆ โดยสามารถแก้ไขค่า letter-spacing ของหัวข้อได้ที่นี่
        self.setStyleSheet("""
            QLabel#mazeTitle {
                font-size: 42px;
                font-weight: 300;
                margin-top: 40px;
            }
            QPushButton#mazeBtn {
                background-color: #3B4252;
                color: #ECEFF4;
                border: 2px solid #4C566A;
                border-radius: 10px;
                padding: 15px;
                min-width: 250px;
                font-size: 18px;
                margin-bottom: 60px;
            }
            QPushButton#mazeBtn:hover {
                background-color: #434C5E;
                border-color: #5E81AC;
            }
        """)
    
    def initialize(self, params):
        """
        รับพารามิเตอร์การทำงานจาก ModelCreationPage และดำเนินการหาเส้นทางที่ดีที่สุดด้วย Genetic Algorithm
        แล้วแสดงผลกราฟภายในหน้า MazePage
        """
        self.text_box.clear()  # ล้างข้อมูลเก่า
        self.text_box.insertHtml("<h3 style='color:#88C0D0;'>🚀 Starting Genetic </h3> <p></p>")

        score = []
        pop_num = []
        
        start_time = time.time()
        pop_size = params['pop_size']
        grid_size = params['grid_size']
        mutation_rate = params['mutation_rate']
        generation_limit = params['generation_limit']

        # สร้าง Grid และกำหนดค่า Weight
        weights = np.random.randint(1, 11, size=(grid_size, grid_size))

        # --- ฟังก์ชันในส่วนของ Genetic Algorithm ---
        def create_individual():
            individual = ['R'] * (grid_size - 1) + ['D'] * (grid_size - 1)
            random.shuffle(individual)
            return individual

        def calculate_fitness(individual):
            x, y = 0, 0

            score.clear()
            pop_num.clear()
            
            total = weights[y][x]
            score.append(weights[y][x])

            for move in individual:
                if move == 'R' and x < grid_size - 1:
                    x += 1
                elif move == 'D' and y < grid_size - 1:
                    y += 1

                score.append(weights[y][x])
                total += weights[y][x]

            score_values = list(map(int, score))
            pop_num.append(score_values)

            return total

        def repair_path(child):
            r_count = child.count('R')
            d_count = child.count('D')
            
            while r_count > grid_size - 1:
                idx = random.choice([i for i, g in enumerate(child) if g == 'R'])
                child[idx] = 'D'
                r_count -= 1
                d_count += 1
            
            while d_count > grid_size - 1:
                idx = random.choice([i for i, g in enumerate(child) if g == 'D'])
                child[idx] = 'R'
                d_count -= 1
                r_count += 1
            
            return child

        def crossover(parent1, parent2):
            size = len(parent1)
            start, end = sorted(random.sample(range(size), 2))
            child = [None] * size
            child[start:end] = parent1[start:end]
            
            remaining = []
            for gene in parent2:
                if child[start:end].count(gene) < parent2.count(gene):
                    remaining.append(gene)
            ptr = 0
            for i in range(size):
                if child[i] is None:
                    child[i] = remaining[ptr]
                    ptr += 1
            return repair_path(child)

        def mutate(individual, mutation_rate=0.1):
            if random.random() < mutation_rate:
                idx1, idx2 = random.sample(range(len(individual)), 2)
                individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
            return repair_path(individual)

        def plot_path(path, title_str, path_str):
            # คำนวณตำแหน่งจุดที่เดินทาง
            x, y = 0, 0
            path_x = [x]
            path_y = [y]
            for move in path:
                if move == 'R':
                    x += 1
                elif move == 'D':
                    y += 1
                
                path_x.append(x)
                path_y.append(y)
            
            # หากมี Canvas อยู่แล้ว ให้เคลียร์ออกจาก layout ก่อน
            if self.canvas is not None:
                for i in reversed(range(self.canvas_layout.count())):
                    widget_to_remove = self.canvas_layout.itemAt(i).widget()
                    if widget_to_remove is not None:
                        widget_to_remove.setParent(None)
            
            # สร้าง Figure และ Canvas ใหม่
            self.figure = Figure(figsize=(12, 12))
            self.figure.subplots_adjust(top=0.80)
            self.figure.set_facecolor('#3B4252')
            self.canvas = FigureCanvas(self.figure)
            self.canvas.setStyleSheet("""
                border: 2px solid #444;
                border-radius: 15px;
            """)
            self.canvas_layout.addWidget(self.canvas)
            ax = self.figure.add_subplot(111)
            
            im = ax.imshow(weights, cmap='viridis', origin='upper')
            # เปลี่ยนสีของตัวอักษรใน colorbar เป็นสีขาว
            cbar = self.figure.colorbar(im, ax=ax)
            cbar.ax.tick_params(labelcolor='white')  # เปลี่ยนสีของตัวเลขใน colorbar เป็นสีขาว

            ax.plot(path_x, path_y, 'r-', linewidth=2)
            ax.scatter(path_x, path_y, c='red', s=50)
            
            ax.set_title(title_str, fontsize=16, pad=35, color='white')
            ax.text(0.5, 1.02, path_str, transform=ax.transAxes,
                    ha='center', fontsize=8, color='white')
            
            ax.tick_params(axis='x', labelcolor='white')  # เปลี่ยนสีตัวเลขที่แสดงบนแกน X
            ax.tick_params(axis='y', labelcolor='white')

            self.canvas.draw()

        # --- เริ่มต้น Population ---
        population = [create_individual() for _ in range(pop_size)]
        best_individual = None
        best_fitness = float('inf')

        for generation in range(generation_limit):
            population = sorted(population, key=calculate_fitness)
            current_best = population[0]
            current_best_fitness = calculate_fitness(current_best)

            # แสดงข้อมูลใน Text Box
            gen_info = f"""
            <div style='margin-bottom: 15px;'>
                <span style='color:#88C0D0; font-weight:bold;'>Generation {generation+1}</span>
                <br>
                ▸ Population: <span style='color:#A3BE8C;'>{pop_num}</span>
                <br>
                ▸ Best Fitness: <span style='color:#EBCB8B;'>{current_best_fitness}</span>
                <br>
                <br>
            </div>
            """
            self.text_box.insertHtml(gen_info)
            
            # เลื่อน Scroll ไปด้านล่างอัตโนมัติ
            self.text_box.verticalScrollBar().setValue(
                self.text_box.verticalScrollBar().maximum()
            )
            QApplication.processEvents()

            if current_best_fitness < best_fitness:
                best_fitness = current_best_fitness
                best_individual = current_best

            new_population = [current_best]
            while len(new_population) < pop_size:
                parents = random.sample(population[:max(2, pop_size // 2)], 2)
                child = crossover(parents[0], parents[1])
                child = mutate(child, mutation_rate)
                new_population.append(child)
            population = new_population

        # (Your genetic algorithm code here)
        end_time = time.time()
        execution_time = end_time - start_time

        # หลังจากลูป Generation หมดแล้ว
        summary_html = f"""
        <div style='margin-top: 20px; padding: 15px; background-color: #434C5E; border-radius: 10px;'>
            <h4 style='color:#A3BE8C; margin:0;'>✅ Completed</h4>
            <p style='margin:5px 0;'>
                ▸ Total Generations: {generation_limit}<br>
                ▸ Final Best Fitness: <strong>{best_fitness}</strong><br>
                ▸ Execution Time: {execution_time:.2f} seconds
            </p>
        </div>
        """
        self.text_box.insertHtml(summary_html)

        # (ถ้าต้องการแบ่งบรรทัดของ best_individual ในบางกรณี)
        # if len(best_individual) > 16:
        #     best_individual = "".join(best_individual[:16]) + "\n" + "".join(best_individual[16:])
        
        best_individual = "".join(best_individual) + "\n"
        
        title_plot = f"Best Maze Path - Fitness: {best_fitness}"
        path_plot = f"Best Path: {''.join(best_individual)}"
        plot_path(best_individual, title_plot, path_plot)