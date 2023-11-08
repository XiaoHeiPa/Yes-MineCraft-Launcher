from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QSpacerItem
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPainter, QPixmap, QColor
from PyQt5.QtWidgets import QApplication, QWidget


# from page2 import Ui_part2
from lib.QTGUI.untitled import Ui_Form as Ui_part2
from qfluentwidgets import *
from lib.QTGUI.mccard import Ui_mccard
from lib.QTGUI.page5 import Ui_page5
from lib.QTGUI.page6 import Ui_page6
from lib.QTGUI.page1 import Ui_part1
from lib.QTGUI.pluginwidget import Ui_pluginwidget
from lib.QTGUI.plugin import Ui_plugin
from lib.QTGUI.selectlist import Ui_selectlist
from  lib.QTGUI.xz import Ui_xz




class Form(QWidget, Ui_part1):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)


class Plugin(QWidget, Ui_plugin):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)


class Form5(QWidget, Ui_page5):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)


class Form6(QWidget, Ui_page6):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)


class Pluginwidget(QWidget, Ui_pluginwidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class Selectlist(QWidget, Ui_selectlist):
    def __init__(self):
        super().__init__()

        self.setupUi(self)


class Xz(QWidget, Ui_xz):
    def __init__(self):
        super().__init__()

        self.setupUi(self)


class Mccard(QWidget, Ui_mccard):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class Form2(QWidget, Ui_part2):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.spacerItem1 = QSpacerItem(358, 308, QSizePolicy.Minimum, QSizePolicy.Expanding)



