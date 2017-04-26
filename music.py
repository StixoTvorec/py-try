#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys, math
from PyQt5.QtWidgets import (QWidget, QPushButton, QSlider, QApplication, QHBoxLayout, QVBoxLayout, QLabel, QGridLayout)
from PyQt5.QtCore import QObject, Qt, pyqtSignal, QRect, QPoint, QSize
# from PyQt5.QtGui import QPainter, QFont, QColor, QPen

class myMusic(QWidget):
    def __init__(self):
        super().__init__()

        # # self.setFixedSize(500, 500)
        # self.setMaximumSize(500, 500)
        self.setWindowTitle('My first app')

    def start(self):
        layout = QGridLayout()
        # inner_layout = QVBoxLayout()

        # layout.addLayout(inner_layout, 3, 1)

        layout.tr('test')

        lbl1 = QLabel('Zetcode')
        btn = QPushButton('Button1')
        btn1 = QPushButton('Button2')
        btn2 = QPushButton('Button3')
        btn3 = QPushButton('Button4')
        layout.addWidget(lbl1, 0, 1, 1, 1)
        layout.addWidget(btn, 0, 0, 1, 1)
        layout.addWidget(btn1, 1, 0, 1, 1)
        layout.addWidget(btn2, 1, 1, 1, 1)
        layout.addWidget(btn3, 1, 2, 1, 1)

        print(layout.rowCount())

        self.setLayout(layout)

        self.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            exit(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    music = myMusic()
    music.start()
    sys.exit(app.exec_())
