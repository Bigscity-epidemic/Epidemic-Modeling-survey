from PyQt5 import Qt
from PyQt5.QtCore import QPoint, QLineF, QPointF
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QPushButton, QGraphicsLineItem, QGraphicsPolygonItem, QGraphicsView, QGraphicsScene, \
    QTextEdit, QWidget, QMenu, QLabel


class DragButton(QPushButton):
    def __init__(self, parent=None, text=None,strname=None, textBox=None):
        super().__init__(parent)
        self.text = text
        self.setText(strname)
        self.iniDragCor = [0, 0]
        self.textBox = textBox

    def mousePressEvent(self, e):
        self.iniDragCor[0] = e.x()
        self.iniDragCor[1] = e.y()

    def mouseMoveEvent(self, e):
        x = e.x() - self.iniDragCor[0]
        y = e.y() - self.iniDragCor[1]

        cor = QPoint(x, y)
        self.move(self.mapToParent(cor))

    def createContextMenu(self):
        self.contextMenu = QMenu(self)

        self.actionA = self.contextMenu.addAction('vertical subdivide')
        self.actionB = self.contextMenu.addAction('horizontal subdivide')
        self.actionC = self.contextMenu.addAction('add path')
        self.actionD = self.contextMenu.addAction('set value')

        self.actionA.triggered.connect(self.verSubDivideHandler)
        self.actionB.triggered.connect(self.horSubDivideHandler)
        self.actionC.triggered.connect(self.addPathHandler)
        self.actionD.triggered.connect(self.setvalueHandler)

        self.contextMenu.exec_(QCursor.pos())

    def verSubDivideHandler(self):
        self.textBox.setText(self.text + " vertical subdivide")

    def horSubDivideHandler(self):
        self.textBox.setText(self.text + " horizontal subdivide")

    def addPathHandler(self):
        self.textBox.setText(self.text + " add path")

    def setvalueHandler(self):
        self.textBox.setText(self.text + " set value")


class Formula(QTextEdit):
    def __init__(self, parent=None, n1=None, n2=None, formula=None, textBox=None):
        super().__init__(parent)
        x1 = n1.geometry().x() + 50
        y1 = n1.geometry().y() + 50
        x2 = n2.geometry().x()
        y2 = n2.geometry().y()

        x = (x1 + x2) / 2 - 60
        y = (y1 + y2) / 2 - 60
        if formula == '\n':
            formula = "f(" + n1.text + "," + n2.text + ")"
        self.src = n1.text
        self.dst = n2.text
        self.setGeometry(x, y, 120, 45)
        self.setText(formula)
        self.textBox = textBox

    def mousePressEvent(self, e):
        self.textBox.setText(self.src + "->" + self.dst + " input formula")


class Arrow(QGraphicsLineItem):
    def __init__(self, parent=None, formula=None, n1=None, n2=None, graphview=None):
        super().__init__(parent)

        self.lefttopx = graphview.x()
        self.lefttopy = graphview.y()
        self.width = graphview.width()
        self.height = graphview.height()
        self.formula = formula
        x1 = n1.geometry().x() - self.width / 2 - self.lefttopx + 25
        y1 = n1.geometry().y() - self.height / 2 - self.lefttopy + 25
        x2 = n2.geometry().x() - self.width / 2 - self.lefttopx
        y2 = n2.geometry().y() - self.height / 2 - self.lefttopy + 25
        # print(n1.geometry().x()-self.width/2, n1.geometry().y()-self.height/2)
        # print(n2.geometry().x()-self.width/2, n2.geometry().y()-self.height/2)
        self.startI = QPointF(x1, y1)
        self.endI = QPointF(x2, y2)
        self.line = QLineF(self.startI, self.endI)
        self.line.setLength(self.line.length() - 20)

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget_widget=None):
        # setPen
        pen = QPen(Qt.black, 1, Qt.SolidLine)
        pen.setJoinStyle(Qt.MiterJoin)
        QPainter.setPen(pen)

        # setBrush
        brush = QBrush()
        brush.setColor(Qt.black)
        brush.setStyle(Qt.SolidPattern)
        QPainter.setBrush(brush)

        v = self.line.unitVector()
        v.setLength(20)
        v.translate(QPointF(self.line.dx(), self.line.dy()))

        n = v.normalVector()
        n.setLength(n.length() * 0.5)
        n2 = n.normalVector().normalVector()

        p1 = v.p2()
        p2 = n.p2()
        p3 = n2.p2()

        QPainter.drawLine(self.line)
        QPainter.drawPolygon(p1, p2, p3)
