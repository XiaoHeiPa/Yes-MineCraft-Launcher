from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QSpacerItem
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPainter, QPixmap, QColor
from PyQt5.QtWidgets import QApplication, QWidget



from Plugin.somePluginExample.untitled import Ui_Form
from Plugin.somePluginExample.untitleda import Ui_Form1
from Plugin.somePluginExample.untitledb import Ui_Form2




class d(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)


class a(QWidget, Ui_Form1):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)


class b(QWidget, Ui_Form2):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)