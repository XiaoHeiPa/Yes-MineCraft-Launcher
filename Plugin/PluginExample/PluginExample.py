from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QSpacerItem
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPainter, QPixmap, QColor
from PyQt5.QtWidgets import QApplication, QWidget



from Plugin.PluginExample.untitled import Ui_Form




class c(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)