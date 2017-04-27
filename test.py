#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, math
from PyQt5.QtWidgets import QWidget, QSlider, QApplication, QHBoxLayout, QVBoxLayout, QLCDNumber, QGraphicsScene, QGraphicsView
from PyQt5.QtCore import QObject, Qt, pyqtSignal, QRectF
from PyQt5.QtGui import QPainter, QFont, QColor, QPen


class Communicate(QObject):

    updateBW = pyqtSignal(int)


class testWidget(QWidget):

    def __init__(self):
        self.needDraw = True
        super().__init__()
        self.setMinimumSize(self.width(), self.height())


    def paintEvent(self, e):
        self.qp.begin(self)
        self.drawWidget()
        self.qp.end()


    def testDraw(self, num: int = 0):
        self.qp = QPainter()

        font = QFont('Serif', 7, QFont.Light)
        self.qp.setFont(font)

        pen = QPen(QColor(20, 20, 20), 1,
                   Qt.SolidLine)

        self.qp.setPen(pen)
        self.qp.setBrush(Qt.NoBrush)

        self.qp.begin(self)
        self.qp.drawPie(0,0, 100,100, 1, num)
        self.qp.end()


    def drawWidget(self):
        # pen2 = QPen(QColor(250, 20, 20), 1,
        #             Qt.SolidLine)
        #
        # pen3 = QPen(QColor(20, 20, 250), 2,
        #             Qt.SolidLine)
        #
        # pen4 = QPen(QColor(20, 20, 250), 1,
        #             Qt.SolidLine)

        w = self.width()
        h = self.height()

        rect = QRectF(0.0, 0.0, 120.0, 50.0)

        # qp.drawArc(rect, 2, 1000)

        # self.testDraw(1)

        # qp.drawLine(0, int(h/2), w, int(h/2)) # h
        # qp.drawLine(int(w/2), 0, int(w/2), h) # h
        # # qp.drawLine(0, 0, self.width()-1, self.width()-1)
        # qp.setPen(pen2)
        # # qp.drawLine(int(self.width()/2), self.width()-1, 0, 0)
        # 
        # accuracy = 9
        # for i in range(1, w, accuracy):
        #     for j in range(1, h, accuracy):
        #         qp.drawPoint(i, j)
        # 
        # qp.setPen(pen3)
        # 
        # for i in range(1, w, accuracy):
        #     x = i
        #     y = int(h/2 + math.sin(i * .0174533) * (h/2))
        #     qp.drawPoint(x, y)
        # 
        # qp.setPen(pen4)
        # 
        # prev = [0, h/2]
        # for i in range(1, w, accuracy):
        #     x = i
        #     y = int(h/2 + math.sin(i * .0174533) * (h/2))
        #     qp.drawLine(prev[0], prev[1], x, y)
        #     prev = [x, y]

        # self.needDraw = False


class Example(QWidget):

    def paintEvent(self, e):
        self.qp.begin(self)
        self.draw()
        self.qp.end()

    def __init__(self):
        super().__init__()

        self.elements = []
        """
        self.elements: QGraphicsObject[]
        """

        self.scene = QGraphicsScene()
        self.graphicsView = QGraphicsView(self.scene)

        hbox = QHBoxLayout()
        hbox.addWidget(self.graphicsView)
        # hbox.addWidget(self.wid)
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('My first app')

        font = QFont('Ubuntu', 20, QFont.Normal)
        self.scene.setFont(font)

        self.qp = QPainter(self.graphicsView)

        self.lcd = QLCDNumber(self.graphicsView)

        self.slider = QSlider(self.graphicsView)
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setGeometry(0, self.graphicsView.height() - 30, self.graphicsView.width(), 30)
        self.slider.valueChanged.connect(self.changer)

        self.elements.append(self.scene.addText('@!#'))

        self.show()

    def changer(self, e: int):
        self.lcd.display(e)
        # self.wid.testDraw(e)
        # self.graphicsView.
        font = QFont('Ubuntu', e * 2 + 16, QFont.Bold)
        self.elements[0].setFont(font) # dynamic change

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            exit(0)
            # print(event.key())

    def draw(self):

        self.graphicsView.setGeometry(0, 0, self.width(), self.height())

        self.lcd.move(self.graphicsView.width() - self.lcd.width() - 4, 3)

        # self.qp.qp.drawLine(0, 0, 100, 200)
        # self.qp.drawText(80, 80, "@!#")
        # self.qp.qp.drawArc(50, 50, 20, 20, 100, 4000)
        # self.qp.qp.drawPie(50, 50, 20, 20, 100, 4000)
        # self.qp.qp.drawRect(1,2, self.graphicsView.width() - 4, self.graphicsView.height() - 3)
        self.slider.setGeometry(0, self.graphicsView.height() - 30, self.graphicsView.width(), 30)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
