import os.path
import platform

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon, QCursor, QDesktopServices
# from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSignal, QUrl

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QIcon, QPainter, QImage, QBrush, QColor, QFont
from PyQt5.QtWidgets import QApplication, QFrame, QStackedWidget, QHBoxLayout, QLabel


from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import *
from configparser import ConfigParser
import shutil

import sys
from UI import Ui_MainWindow
from qfluentwidgets import (NavigationInterface,NavigationItemPosition, NavigationWidget, MessageBox,
                            isDarkTheme, setTheme, Theme)
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import FramelessWindow, StandardTitleBar, AcrylicWindow, TitleBar
from qfluentwidgets import Theme, setTheme, setThemeColor
from PyQt5 import QtCore, QtGui, QtWidgets

class window(AcrylicWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 使用Mica
        self.windowEffect.setMicaEffect(self.winId())
        self.setQss()
        # cfg.themeChanged.connect(self.setQss)






        # 主题色
        # setTheme(Theme.DARK)
        # s =platform.version()
        setThemeColor("#0078D4")
        s = platform.platform ()
        print(s)

        # 初始化
        if os.path.exists("yes"):
            try:

                f = open("yes/yml.ini", 'r')
                f.close()

            except IOError:
                cf = ConfigParser()

                cf.add_section('main')
                cf.set('main', 'yn', 'n')
                # cf.set('login', 'password', '123456')

                cf.write(open("yes/yml.ini", 'w'))
            cf1 = ConfigParser()

            cf1.read('yes/yml.ini', encoding='utf-8')
            # print(cf1.get('main', 'yn'))
            yn = cf1.get('main', 'yn')

            if yn == "n":
                self.stackedWidget.setCurrentIndex(0)
            if yn == "y":
                self.stackedWidget.setCurrentIndex(6)
        if not os.path.exists("yes"):
            os.mkdir("yes")
            cf = ConfigParser()

            cf.add_section('main')
            cf.set('main', 'yn', 'n')
            # cf.set('login', 'password', '123456')

            cf.write(open("yes/yml.ini", 'w'))
            self.stackedWidget.setCurrentIndex(0)

        try:

           f = open("yes/yml.ini", 'r')
           f.close()

        except IOError:

           f = open("yes/yml.ini", 'w')




        self.stackedWidget_2.setCurrentIndex(1)
        self.comboBox.setCurrentIndex(1)
        self.lineEdit.setPlaceholderText("Name:")


        # 标题栏
        self.setTitleBar(StandardTitleBar(self))
        self.titleBar.maxBtn.hide()

        self.titleBar.raise_()

        self.setWindowIcon(QIcon("bitbug_favicon2.ico"))
        self.setWindowTitle("Yes MineCraft Launcher")

        self.resize(1250, 720)

        # 居中
        rect = QApplication.desktop().availableGeometry(
        )
        w, h = rect.width(), rect.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        # 按钮事件绑定
        self.pushButton.clicked.connect(self.page1)
        self.pushButton_5.clicked.connect(self.page1)
        self.pushButton_2.clicked.connect(self.page2)
        self.pushButton_13.clicked.connect(self.page2)
        self.pushButton_4.clicked.connect(self.page3)
        self.pushButton_15.clicked.connect(self.page3)
        self.pushButton_11.clicked.connect(self.page4)
        self.pushButton_6.clicked.connect(self.page_start)
        self.pushButton_16.clicked.connect(self.pagemain)
        self.pushButton_17.clicked.connect(self.pagemain_1)
        self.pushButton_12.setUrl("https://www.minecraft.net/")



        x = self.label.pos().x()
        y = self.label.pos().y()
        self.anim = QPropertyAnimation(self.label, b"geometry")
        self.anim.setDuration(300)
        self.anim.setStartValue(QRect(x, y+600, 821, 101))
        self.anim.setEndValue(QRect(x, y, 821, 101))
        self.anim.start()

    def setQss(self):
        theme = 'dark' if isDarkTheme() else 'light'
        with open(f'resource/qss/{theme}/demo.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    # 按钮事件
    def page1(self):
        x = self.label_3.pos().x()
        y = self.label_3.pos().y()
        self.anim = QPropertyAnimation(self.label_3, b"geometry")
        self.anim.setDuration(300)
        self.anim.setStartValue(QRect(x, y + 600, 161, 161))
        self.anim.setEndValue(QRect(x, y, 161, 161))
        self.anim.start()
        x1 = self.label_4.pos().x()
        y1 = self.label_4.pos().y()
        self.anim1 = QPropertyAnimation(self.label_4, b"geometry")
        self.anim1.setDuration(300)
        self.anim1.setStartValue(QRect(x1+100, y1, 221, 71))
        self.anim1.setEndValue(QRect(x1, y1, 221, 71))
        self.anim1.start()
        self.stackedWidget.setCurrentIndex(1)

    def page2(self):
        x = self.label_13.pos().x()
        y = self.label_13.pos().y()
        self.anim = QPropertyAnimation(self.label_13, b"geometry")
        self.anim.setDuration(300)
        self.anim.setStartValue(QRect(x, y + 600, 291, 111))
        self.anim.setEndValue(QRect(x, y, 291, 111))
        self.anim.start()
        x1 = self.label_14.pos().x()
        y1 = self.label_14.pos().y()
        self.anim1 = QPropertyAnimation(self.label_14, b"geometry")
        self.anim1.setDuration(300)
        self.anim1.setStartValue(QRect(x1 + 100, y1, 541, 281))
        self.anim1.setEndValue(QRect(x1, y1, 541, 281))
        self.anim1.start()
        self.stackedWidget.setCurrentIndex(2)

    def page3(self):
        x = self.label_15.pos().x()
        y = self.label_15.pos().y()
        self.anim = QPropertyAnimation(self.label_15, b"geometry")
        self.anim.setDuration(300)
        self.anim.setStartValue(QRect(x + 600, y, 431, 381))
        self.anim.setEndValue(QRect(x, y, 431, 381))
        self.anim.start()
        x1 = self.label_17.pos().x()
        y1 = self.label_17.pos().y()
        self.anim1 = QPropertyAnimation(self.label_17, b"geometry")
        self.anim1.setDuration(300)
        self.anim1.setStartValue(QRect(x1, y1 + 600, 121, 31))
        self.anim1.setEndValue(QRect(x1, y1, 121, 31))
        self.anim1.start()
        self.stackedWidget.setCurrentIndex(3)

    def page4(self):
        x = self.label_21.pos().x()
        y = self.label_21.pos().y()
        self.anim = QPropertyAnimation(self.label_21, b"geometry")
        self.anim.setDuration(300)
        self.anim.setStartValue(QRect(x + 600, y, 201, 31))
        self.anim.setEndValue(QRect(x, y, 201, 31))
        self.anim.start()
        x1 = self.pushButton_15.pos().x()
        y1 = self.pushButton_15.pos().y()
        self.anim1 = QPropertyAnimation(self.pushButton_15, b"geometry")
        self.anim1.setDuration(300)
        self.anim1.setStartValue(QRect(x1, y1 + 600, 111, 51))
        self.anim1.setEndValue(QRect(x1, y1, 111, 51))
        self.anim1.start()
        self.stackedWidget.setCurrentIndex(4)
        self.lineEdit.clear()

    def page_start(self):
        x = self.label_22.pos().x()
        y = self.label_22.pos().y()
        self.anim = QPropertyAnimation(self.label_22, b"geometry")
        self.anim.setDuration(300)
        self.anim.setStartValue(QRect(x + 600, y, 161, 161))
        self.anim.setEndValue(QRect(x, y, 161, 161))
        self.anim.start()
        x1 = self.label_23.pos().x()
        y1 = self.label_23.pos().y()
        self.anim1 = QPropertyAnimation(self.label_23, b"geometry")
        self.anim1.setDuration(300)
        self.anim1.setStartValue(QRect(x1, y1 + 600, 221, 71))
        self.anim1.setEndValue(QRect(x1, y1, 221, 71))
        self.anim1.start()
        x2 = self.label_24.pos().x()
        y2 = self.label_24.pos().y()
        self.anim2 = QPropertyAnimation(self.label_24, b"geometry")
        self.anim2.setDuration(300)
        self.anim2.setStartValue(QRect(x2 + 600, y2, 481, 131))
        self.anim2.setEndValue(QRect(x2, y2, 481, 131))
        self.anim2.start()
        x3 = self.label_25.pos().x()
        y3 = self.label_25.pos().y()
        self.anim3 = QPropertyAnimation(self.label_25, b"geometry")
        self.anim3.setDuration(300)
        self.anim3.setStartValue(QRect(x3, y3 + 600, 541, 331))
        self.anim3.setEndValue(QRect(x3, y3, 541, 331))
        self.anim3.start()
        x4 = self.pushButton_16.pos().x()
        y4 = self.pushButton_16.pos().y()
        self.anim4 = QPropertyAnimation(self.pushButton_16, b"geometry")
        self.anim4.setDuration(300)
        self.anim4.setStartValue(QRect(x4 + 600, y4, 111, 61))
        self.anim4.setEndValue(QRect(x4, y4, 111, 61))
        self.anim4.start()
        self.stackedWidget.setCurrentIndex(5)

    def pagemain_home(self):
        x = self.label_15.pos().x()
        y = self.label_15.pos().y()
        self.anim = QPropertyAnimation(self.label_15, b"geometry")
        self.anim.setDuration(300)
        self.anim.setStartValue(QRect(x + 600, y, 431, 381))
        self.anim.setEndValue(QRect(x, y, 431, 381))
        self.anim.start()
        x1 = self.label_17.pos().x()
        y1 = self.label_17.pos().y()
        self.anim1 = QPropertyAnimation(self.label_17, b"geometry")
        self.anim1.setDuration(300)
        self.anim1.setStartValue(QRect(x1, y1 + 600, 121, 31))
        self.anim1.setEndValue(QRect(x1, y1, 121, 31))
        self.anim1.start()
        self.stackedWidget_2.setCurrentIndex(0)

    def pagemain_1(self):
        x = self.pushButton_18.pos().x()
        y = self.pushButton_18.pos().y()
        self.anim = QPropertyAnimation(self.pushButton_18, b"geometry")
        self.anim.setDuration(300)
        self.anim.setStartValue(QRect(x + 600, y, 211, 211))
        self.anim.setEndValue(QRect(x, y, 211, 211))
        self.anim.start()
        x1 = self.pushButton_24.pos().x()
        y1 = self.pushButton_24.pos().y()
        self.anim1 = QPropertyAnimation(self.pushButton_24, b"geometry")
        self.anim1.setDuration(300)
        self.anim1.setStartValue(QRect(x1 +600, y1, 151, 311))
        self.anim1.setEndValue(QRect(x1, y1, 151, 311))
        self.anim1.start()
        x3 = self.stackedWidget_2.pos().x()
        y3 = self.stackedWidget_2.pos().y()
        self.anim2 = QPropertyAnimation(self.stackedWidget_2, b"geometry")
        self.anim2.setDuration(300)
        self.anim2.setStartValue(QRect(x, y + 600, 1191, 651))
        self.anim2.setEndValue(QRect(x, y, 1191, 651))
        self.anim2.start()
        self.stackedWidget_2.setCurrentIndex(2)

    def setAcrylicEffectEnabled(self, enable: bool):

        self.setStyleSheet(f"background:{'transparent' if enable else '#F2F2F2'}")
        if enable:
            self.windowEffect.setAcrylicEffect(self.winId(), "F2F2F299")
            if QOperatingSystemVersion.current() != QOperatingSystemVersion.Windows10:
                self.windowEffect.addShadowEffect(self.winId())

            else:
                self.windowEffect.addShadowEffect(self.winId())
                self.windowEffect.removeBackgroundEffect(self.winId())

    def pagemain(self):
        cf = ConfigParser()
        cf.read('yes/yml.ini')
        res = cf.sections()  # ['section1', 'section2']
        # print(res)

        cf.set(res[0], 'yn', 'y')
        # cf.set('login', 'password', '123456')

        cf.write(open("yes/yml.ini", 'w'))
        self.stackedWidget.setCurrentIndex(6)

    def openurl(self):
        QDesktopServices.openurl(QUrl("https://www.minecraft.net/"))








if __name__ == '__main__':
    app = QApplication(sys.argv)
    windows = window()

    windows.show()
    app.exec_()
