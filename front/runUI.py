from math import sin, cos

from PyQt5 import Qt, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QGridLayout
import sys
from exeui import ExeUI

import UIWidget
from LibEpidemic import Ui_MainWindow
from PyQt5.QtCore import *
from UIWidget import Arrow


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)

        self.model = model

        self.setupUi(self)
        self.pushButton.clicked.connect(self.handleAction)
        self.simu_days = 0

    def setModel(self, model):
        self.model = model

    def setExeUI(self, exeUI):
        self.exeUI = exeUI

    def checkStatus(self, code):
        if code != 0:
            reply = QMessageBox.question(self, 'error', 'The Programme will exit',
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                         QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                print('退出')
                sys.exit(0)
            else:
                print('不退出')

    def displayModel(self, p):
        self.name2compartments = self.model.name2compartments
        nodes = list(self.name2compartments.keys())
        self.nodeButtons = {}
        self.buttonSize = 50
        initNode = nodes[0]

        self.layout = QGridLayout()

        self.visit = []
        self.dfsShowModel(initNode, [self.graphicsView.x() + self.buttonSize,
                                     self.graphicsView.y() + self.graphicsView.height() / 3 + self.buttonSize,
                                     self.buttonSize, self.buttonSize], p)

        self.paths = self.model.name2paths
        pathSrcDst = [(k[:k.index('-')], k[k.index('>') + 1:]) for k in list(self.paths.keys())]
        for src, dst in pathSrcDst:
            self.scene.addItem(Arrow(n1=self.nodeButtons[src], n2=self.nodeButtons[dst],
                                     formula=self.paths[src + "->" + dst].expression, graphview=self.graphicsView))

        self.formulas = []
        for src, dst in pathSrcDst:
            param_str = ''
            if (src + "->" + dst) in p.keys():
                param = p[src + "->" + dst]

                for name in param:
                    param_str += name + ' : ' + str(param[name]) + '\n'

            f = UIWidget.Formula(self.centralwidget, self.nodeButtons[src], self.nodeButtons[dst],
                                 formula=self.paths[src + "->" + dst].expression + '\n' + param_str,
                                 textBox=self.label_2)
            self.formulas.append(f)
            self.layout.addWidget(f, 1, 0)

        self.setLayout(self.layout)

    def dfsShowModel(self, node, pos, p):
        if node in self.visit:
            return
        self.toButton(node, pos, p)
        self.visit.append(node)
        next = self.name2compartments[node].node.next_name_list.keys()
        if len(next) == 0:
            return
        theta = 90 / (len(next) if len(next) == 1 else len(next) - 1)
        R = 200
        for index, n in enumerate(next):
            y_ = sin(index * theta) * R
            x_ = cos(index * theta) * R
            pos[0] += x_
            pos[1] += y_
            self.dfsShowModel(n, pos, p)

    def toButton(self, name, pos, p):
        strname = name + '\nNone'
        if name in p.keys():
            strname = name + '\n' + str(int(p[name]))
        pushButton = UIWidget.DragButton(self.centralwidget, name, strname, textBox=self.label_2)
        pushButton.setContextMenuPolicy(Qt.CustomContextMenu)
        pushButton.customContextMenuRequested.connect(pushButton.createContextMenu)
        pushButton.setGeometry(QtCore.QRect(pos[0], pos[1], pos[2], pos[3]))
        pushButton.setObjectName("pushButton")
        self.layout.addWidget(pushButton, 1, 0)
        self.nodeButtons[name] = pushButton
        return pushButton

    def handleAction(self):
        if self.url.text()[0:5] == 'start':
            self.simu_days += 1
            model, p = exe.send_message(message={'handle': 'run'})
            self.model = model
            self.update(p)
            reply = QMessageBox.question(self, 'Simulator', 'Succeed simulating ' + str(
                self.simu_days) + ' day!\n\nClick Yes or Cancel to continue,\nClick No if you want to quit!',
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                         QMessageBox.Cancel)
            if reply == QMessageBox.No:
                sys.exit(0)
            else:
                pass
            return
        message = {}
        if '->' in self.label_2.text():
            text = self.label_2.text()
            src = text[:text.index("->")]
            dst = text[text.index("->") + 2:text.index(" ")]
            forstr = self.url.text()
            if forstr[:5] == 'param':
                handle, name, value = forstr.split(' ')
                message['handle'] = 'param'
                message['name'] = name
                if value[0] == '[':
                    tmp = value[1:-1].split(',')
                    v = []
                    for item in tmp:
                        v.append(float(item))
                        message['value'] = v
                else:
                    message['value'] = float(value)
                message['src'] = src
                message['dst'] = dst
            else:
                message['handle'] = 'formula'
                message['exp'] = self.url.text()
                message['src'] = src
                message['dst'] = dst
        else:
            temp = self.label_2.text().split(" ")
            origin = temp[0]
            text = " ".join(temp[1:])
            new = self.url.text()
            if text == "vertical subdivide":
                message['handle'] = 'subdivide'
                message['type'] = 'ver'
                message['origin'] = origin
                message['new'] = new.split(" ")
            elif text == "horizontal subdivide":
                message['handle'] = 'subdivide'
                message['type'] = 'hor'
                message['origin'] = origin
                message['new'] = new.split(" ")
            elif text == "add path":
                message['handle'] = 'subdivide'
                message['type'] = 'add'
                message['origin'] = origin
                message['new'] = new.replace(" ", "")
            elif text == 'set value':
                message['handle'] = 'setvalue'
                message['compartment'] = origin
                message['value'] = float(new)
            else:
                return
        code, model, p = self.exeUI.send_message(message)
        self.model = model
        self.checkStatus(code)
        self.update(p)

    def update(self, p):
        for k in self.nodeButtons:
            self.nodeButtons[k].close()
        self.graphicsView.close()
        self.displayModel(p)
        for k in self.nodeButtons:
            self.nodeButtons[k].show()
        for f in self.formulas:
            f.show()
        self.graphicsView.show()


if __name__ == '__main__':
    sir_preset = True
    app = QApplication(sys.argv)
    exe = ExeUI()
    code, model, param = exe.send_message({'handle': 'init', 'init_name': 'S'})
    if sir_preset:
        exe.send_message({'handle': 'init', 'init_name': 'S'})
        exe.send_message({'handle': 'subdivide', 'type': 'ver', 'origin': 'S', 'new': ['I', 'R']})

        exe.send_message({'handle': 'formula', 'src': 'S', 'dst': 'I', 'exp': 'beta*S*I*popu'})
        exe.send_message({'handle': 'param', 'src': 'S', 'dst': 'I', 'name': 'beta', 'value': 0.3})
        exe.send_message({'handle': 'param', 'src': 'S', 'dst': 'I', 'name': 'popu', 'value': 0.00001})

        exe.send_message({'handle': 'formula', 'src': 'I', 'dst': 'R', 'exp': 'gamma*I'})
        exe.send_message({'handle': 'param', 'src': 'I', 'dst': 'R', 'name': 'gamma', 'value': 0.1})

        exe.send_message({'handle': 'setvalue', 'compartment': 'S', 'value': 99990})
        exe.send_message({'handle': 'setvalue', 'compartment': 'I', 'value': 10})
        code, model, param = exe.send_message({'handle': 'setvalue', 'compartment': 'R', 'value': 0})
    LibEpidemicFont = MyWindow()
    LibEpidemicFont.setModel(model)
    LibEpidemicFont.setExeUI(exe)
    LibEpidemicFont.displayModel(param)
    LibEpidemicFont.show()
    sys.exit(app.exec_())
