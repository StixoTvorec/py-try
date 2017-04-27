#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# NOT WORKED

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys, time, math

class Test(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.pts = [[80, 300],
                    [180, 300],
                    [280, 300],
                    [430, 300],
                    [580, 300],
                    [680, 300],
                    [780, 300]]
        self.time = 0
        self.time_step = 0.002
        self.timer_id = self.startTimer(1)

    def poly(self, pts):
        return QPolygonF(map(lambda p: QPointF(*p), pts))

    def timerEvent(self, event):
        if self.timer_id == event.timerId():
            self.update_wave()
            self.time += self.time_step
            self.update()

    def update_wave(self):
        k = 0
        phi = 0.7
        for p in self.pts:
            p[1] =300 + 100*math.sin(self.time+phi*k)
            k += 1

    def paintEvent(self, event):
        painter = QPainter(self)
        pts = self.pts
        painter.setPen(QPen(QColor(Qt.darkGreen), 3))
        painter.drawPolyline(self.poly(pts))
        painter.setBrush(QBrush(QColor(255, 0, 0)))
        painter.setPen(QPen(QColor(Qt.black), 1))
        for x, y in pts:
            painter.drawEllipse(QRectF(x - 4, y - 4, 8, 8))

if __name__ == '__main__':
    example = QApplication(sys.argv)
    test2 = Test()
    test2.resize(800, 600)
    test2.show()
    sys.exit(example.exec_())