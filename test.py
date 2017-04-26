#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, math
from PyQt5.QtWidgets import (QWidget, QSlider, QApplication, QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QFont, QColor, QPen


class Communicate(QObject):

    updateBW = pyqtSignal(int)


class testWidget(QWidget):

    def __init__(self):
        self.needDraw = True
        super().__init__()
        self.setMinimumSize(self.width(), self.height())


    def paintEvent(self, e):

        qp = QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()


    def drawWidget(self, qp):

        font = QFont('Serif', 7, QFont.Light)
        qp.setFont(font)

        pen = QPen(QColor(20, 20, 20), 1,
                   Qt.SolidLine)

        pen2 = QPen(QColor(250, 20, 20), 1,
                    Qt.SolidLine)

        pen3 = QPen(QColor(20, 20, 250), 2,
                    Qt.SolidLine)

        pen4 = QPen(QColor(20, 20, 250), 1,
                    Qt.SolidLine)

        w = self.width()
        h = self.height()

        qp.setPen(pen)
        qp.setBrush(Qt.NoBrush)
        qp.drawLine(0, int(h/2), w, int(h/2)) # h
        qp.drawLine(int(w/2), 0, int(w/2), h) # h
        # qp.drawLine(0, 0, self.width()-1, self.width()-1)
        qp.setPen(pen2)
        # qp.drawLine(int(self.width()/2), self.width()-1, 0, 0)

        accuracy = 9
        for i in range(1, w, accuracy):
            for j in range(1, h, accuracy):
                qp.drawPoint(i, j)

        qp.setPen(pen3)

        for i in range(1, w, accuracy):
            x = i
            y = int(h/2 + math.sin(i * .0174533) * (h/2))
            qp.drawPoint(x, y)

        qp.setPen(pen4)

        prev = [0, h/2]
        for i in range(1, w, accuracy):
            x = i
            y = int(h/2 + math.sin(i * .0174533) * (h/2))
            qp.drawLine(prev[0], prev[1], x, y)
            prev = [x, y]

        # self.needDraw = False


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.setMaximumSize(500, 500)
        # self.setGeometry(300, 300, 500, 900)
        self.setWindowTitle('My first app')
        font = QFont('Ubuntu', 20, QFont.Normal)
        self.setFont(font)

        # self.wid = BurningWidget()
        self.wid = testWidget()

        hbox = QHBoxLayout()
        hbox.addWidget(self.wid)
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            exit(0)
        # print(event.key())


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
