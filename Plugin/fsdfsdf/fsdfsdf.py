from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QSpacerItem
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPainter, QPixmap, QColor
from PyQt5.QtWidgets import QApplication, QWidget



from Plugin.fsdfsdf.dasdas import Ui_text2




class b(QWidget, Ui_text2):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)