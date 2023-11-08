from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QSpacerItem
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPainter, QPixmap, QColor
from PyQt5.QtWidgets import QApplication, QWidget



from Plugin.text.fdfsd import Ui_text




class c(QWidget, Ui_text):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)