import copy
import json
import sys
import os
import zipfile

import darkdetect
import minecraft_launcher_lib
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from darkdetect import theme as currentTheme

from PyQt5.QtCore import Qt, QEventLoop, QTimer, QSize, QEasingCurve, QSettings, QEvent
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QIcon, QPainter, QPixmap, QColor, QActionEvent
from PyQt5.QtWidgets import QApplication, QWidget, QAction, QSpacerItem, QSizePolicy
from minecraft_launcher_lib import *
from minecraft_launcher_lib.utils import get_installed_versions

from qfluentwidgets import SplitFluentWindow, FluentIcon, qconfig, RoundMenu, FluentWindow, FlowLayout, InfoBar, \
    InfoBarPosition, ToolTipFilter, ToolTipPosition, StyleSheetBase

from qfluentwidgets import SplashScreen
from qframelesswindow import FramelessWindow, StandardTitleBar, AcrylicWindow, TitleBar
from page_form import Form, Form2, Plugin, Form5, Form6, Pluginwidget, Mccard, Selectlist, Xz

from qfluentwidgets import (NavigationInterface, NavigationItemPosition, NavigationWidget, MessageBox,
                            isDarkTheme, setTheme, Theme, setThemeColor)
from pathlib import Path
from enum import Enum
from PyQt5.QtCore import QThread
from subprocess import run
import icons_rc

import winreg


class ColorThread(QThread):

    def __init__(self) -> None:
        QThread.__init__(self)


    def run(self) -> None:
        # 定义个性化颜色的注册表路径
        color_key_path = r"Software\Microsoft\Windows\DWM"

        # 获取个性化颜色函数
        def get_system_color():
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, color_key_path)
                value, _ = winreg.QueryValueEx(key, "ColorizationColor")
                alpha = (value >> 24) & 0xFF
                red = (value >> 16) & 0xFF
                green = (value >> 8) & 0xFF
                blue = value & 0xFF
                return (red, green, blue, alpha)
            except Exception as e:
                # print("获取个性化颜色失败:", repr(e))
                return None

        # 获取个性化颜色
        system_color = get_system_color()
        r = system_color[0]
        g = system_color[1]
        b = system_color[2]
        a = system_color[3]
        if system_color:
            setThemeColor(color=QColor(r, g, b, a))


            # print("个性化颜色（RGBA）：", system_color)


class StartmcThread(QThread):

    def __init__(self) -> None:
        QThread.__init__(self)

    def set_data(self, version: str, username, options, dir) -> None:
        self._version = version
        self._username = username
        self._options = options
        self._dir = dir

    def run(self) -> None:
        options = minecraft_launcher_lib.utils.generate_test_options()
        options['username'] = self._username
        minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(self._version, self._dir,
                                                                                 self._options)
        # print(minecraft_command)
        # print(options)

        run(minecraft_command, shell=True)


class parameter():
    def __init__(self):
        self.mcdir = ".minecraft"
        self.startmc = ""
        self.theme = 'AUTO'


class window(FluentWindow, parameter):
    def __init__(self):
        super().__init__()

        self._runmc_thread = StartmcThread()
        self._color_thread = ColorThread()
        # self._on_theme_change = on_theme_change()

        self.parameters = parameter()

        self.pulgs = []
        self.pulgs2 = []

        self.resize(1000, 700)
        # 居中
        rect = QApplication.desktop().availableGeometry(
        )
        w, h = rect.width(), rect.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)




        # setTheme(Theme.AUTO)

        self.widgettheme(self.parameters.theme)
        # setThemeColor("#0078D4")

        # self._on_theme_change.start()



        # print(setTheme)
        self.setWindowTitle("Yes-MineCraft-Launcher")
        self.setWindowIcon(QIcon("res\icon\YML3.png"))
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(128, 128))

        self.show()

        self.createSubInterface()

        # close splash screen
        self.splashScreen.finish()

        # 添加子界面
        self.form = Form(self)
        self.form2 = Form2(self)
        self.plugin = Plugin(self)
        self.form5 = Form5(self)
        self.form6 = Form6(self)

        # 初始化
        self.初始化()
        self._color_thread.start()


    def createSubInterface(self):
        loop = QEventLoop(self)
        QTimer.singleShot(3000, loop.quit)
        loop.exec()

    def 初始化(self):
        # color = 'dark' if isDarkTheme() else 'light'
        # with open(f"resource/{color}/demo.qss",encoding="utf-8")as f:
        #     self.setStyleSheet(f.read())

        self.plugin.SegmentedWidget.addItem(routeKey="1", text="单页插件",
                                            onClick=lambda: self.plugin.stackedWidget.setCurrentIndex(0))
        self.plugin.SegmentedWidget.addItem(routeKey="2", text="多页插件",
                                            onClick=lambda: self.plugin.stackedWidget.setCurrentIndex(1))
        self.plugin.SegmentedWidget.addItem(routeKey="3", text="嵌入式插件",
                                            onClick=lambda: self.plugin.stackedWidget.setCurrentIndex(2))

        self.addSubInterface(self.form, FluentIcon.HOME, '开始')
        self.addSubInterface(self.form2, FluentIcon.ALIGNMENT, '核心')
        self.addSubInterface(self.plugin, FluentIcon.MORE, '插件')

        self.navigationInterface.addSeparator()
        pos1 = NavigationItemPosition.BOTTOM

        self.addSubInterface(self.form5, FluentIcon.INFO, '关于', pos1)
        self.addSubInterface(self.form6, FluentIcon.SETTING, '设置', pos1)

        self.plugin.SmoothScrollArea.setStyleSheet("background-color: rgb(48, 48, 48, 0);")
        self.plugin.scrollAreaWidgetContents.setStyleSheet("background-color: rgb(48, 48, 48, 0);")
        self.plugin.SmoothScrollArea_2.setStyleSheet("background-color: rgb(48, 48, 48, 0);")
        self.plugin.scrollAreaWidgetContents_2.setStyleSheet("background-color: rgb(48, 48, 48, 0);")
        self.plugin.SmoothScrollArea_3.setStyleSheet("background-color: rgb(48, 48, 48, 0);")
        self.plugin.scrollAreaWidgetContents_3.setStyleSheet("background-color: rgb(48, 48, 48, 0);")
        self.form2.serversSmoothScrollArea.setStyleSheet("background-color: rgb(48, 48, 48, 0);")
        self.form6.settingsScrollAreaWidgetContents.setStyleSheet("background-color: rgb(48, 48, 48, 0);")
        self.form6.settingsSmoothScrollArea.setStyleSheet("background-color: rgb(48, 48, 48, 0);")
        self.form6.selectThemeColorBtn.setText("")
        self.form6.startOnStartup.setEnabled(False)
        self.form6.checkUpdateOnStartSwitchBtn.setEnabled(False)
        self.form6.checkUpdateBtn.setEnabled(False)
        self.form6.quickMenuSwitchBtn.setEnabled(False)
        self.form6.quickMenuSwitchBtn_2.setEnabled(False)
        self.form6.quickMenuSwitchBtn_3.setEnabled(False)

        # self.form6.CardWidget_2.close()
        # self.form6.saveSettingsBtnWidget.close()

        self.form.ComboBox.addItem("user")
        self.form6.currentVerLabel.setText("3.0.0.2984=公测一版=beta1")

        self.form.PushButton.clicked.connect(lambda: self.select())
        self.form2.PushButton_2.clicked.connect(lambda: self.xz())
        self.form.PrimaryPushButton.clicked.connect(
            lambda: self.runmc(version=self.parameters.startmc, username=self.form.ComboBox.currentText()))

        self._runmc_thread.finished.connect(self._runmc_thread_finished)

        # 插件系统
        self.Plugin()
        self.somePlugin()

        # mc检测
        self.Gamecard()


        # self._theme_thread.start()



    def _runmc_thread_finished(self) -> None:
        # This function is called after the Multi Thread Installation has been finished

        self.form.PrimaryPushButton.setEnabled(True)

    def runmc(self, version, username):
        try:

            options = minecraft_launcher_lib.utils.generate_test_options()
            options['username'] = username
            minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, self.parameters.mcdir,
                                                                                     options)
            self._runmc_thread.set_data(version=version, username=username, options=options, dir=self.parameters.mcdir)
            self._runmc_thread.start()
            self.form.PrimaryPushButton.setEnabled(False)



        except:
            ...

    def select(self):
        selectlist = Selectlist()

        mclist = []

        mclist = minecraft_launcher_lib.utils.get_installed_versions(self.parameters.mcdir)

        for i in range(len(mclist)):
            selectlist.ListWidget.setIconSize(QtCore.QSize(24, 24))

            items = QtWidgets.QListWidgetItem()
            icon = QtGui.QIcon()

            if mclist[i]['type'] == "release":
                icon.addPixmap(QtGui.QPixmap(":/built-InIcons/Grass.png"), QtGui.QIcon.Normal,
                               QtGui.QIcon.Off)

            if mclist[i]['type'] == "snapshot":
                icon.addPixmap(QtGui.QPixmap(":/built-InIcons/CommandBlock.png"), QtGui.QIcon.Normal,
                               QtGui.QIcon.Off)

            if mclist[i]['type'] == "old_alpha":
                icon.addPixmap(QtGui.QPixmap(":/built-InIcons/CobbleStone.png"), QtGui.QIcon.Normal,
                               QtGui.QIcon.Off)

            if mclist[i]['type'] == "old_beta":
                icon.addPixmap(QtGui.QPixmap(":/built-InIcons/GrassPath.png"), QtGui.QIcon.Normal,
                               QtGui.QIcon.Off)

            items.setIcon(icon)
            selectlist.ListWidget.addItem(items)

            __sortingEnabled = selectlist.ListWidget.isSortingEnabled()
            selectlist.ListWidget.setSortingEnabled(False)

            item = selectlist.ListWidget.item(i)
            item.setText(mclist[i]['id'])

            selectlist.ListWidget.setSortingEnabled(__sortingEnabled)

        title = '选择Minecraft'
        content = ""
        # w = MessageDialog(title, content, self)   # Win10 style message box
        w = MessageBox(title, content, self)
        w.textLayout.addWidget(selectlist)

        if w.exec():
            try:
                self.parameters.startmc = f"{selectlist.ListWidget.currentItem().text()}"
                self.form.PrimaryPushButton.setText("启动你的MineCraft吧\n" + self.parameters.startmc)

            except:
                ...

    def xz(self):
        xz = Xz()

        title = '下载Minecraft'
        content = ""
        # w = MessageDialog(title, content, self)   # Win10 style message box
        w = MessageBox(title, content, self)
        w.textLayout.addWidget(xz)

        if w.exec():
            try:
                # print("开始下载")
                ...

            except:
                ...

    def Gamecard(self):

        mclist = []

        mclist = minecraft_launcher_lib.utils.get_installed_versions(self.parameters.mcdir)

        for i in range(len(mclist)):
            try:
                self.form2.verticalLayout_2.removeItem(self.spacerItem1)
            except:
                pass
            try:
                for i in reversed(range(self.verticalLayout_2.count())):
                    self.form2.verticalLayout_2.itemAt(i).widget().deleteLater()
            except AttributeError:
                pass
            self.mccard = Mccard()

            self.mccard.setObjectName(f"mccard{i}")
            self.mccard.TransparentToolButton.close()
            self.mccard.TransparentToolButton_2.setIcon(FluentIcon.DELETE)
            self.mccard.TransparentToolButton_3.setIcon(FluentIcon.DICTIONARY_ADD)
            self.mccard.TransparentToolButton_4.close()
            self.mccard.TransparentToolButton_5.setIcon(FluentIcon.PLAY)
            self.mccard.StrongBodyLabel.setText(mclist[i]['id'])
            self.mccard.CaptionLabel.setText(f"{mclist[i]['type']}")
            self.mccard.CaptionLabel_2.setText(f"合规级别:{mclist[i]['complianceLevel']}")

            if mclist[i]['type'] == "release":
                self.mccard.PixmapLabel.setStyleSheet("border-image: url(:/built-InIcons/Grass.png);")

            if mclist[i]['type'] == "snapshot":
                self.mccard.PixmapLabel.setStyleSheet("border-image: url(:/built-InIcons/CommandBlock.png);")

            if mclist[i]['type'] == "old_alpha":
                self.mccard.PixmapLabel.setStyleSheet("border-image: url(:/built-InIcons/CobbleStone.png);")

            if mclist[i]['type'] == "old_beta":
                self.mccard.PixmapLabel.setStyleSheet("border-image: url(:/built-InIcons/GrassPath.png);")

            self.mccard.TransparentToolButton_5.clicked.connect(
                lambda *args, t=self.mccard: self.runmc(version=t.StrongBodyLabel.text(),
                                                        username=self.form.ComboBox.currentText()))
            self.mccard.TransparentToolButton_2.clicked.connect(
                lambda *args, t=self.mccard: self.createErrorInfoBar(title="系统消息",
                                                                     content=f"核心{t.StrongBodyLabel.text()}删除失败，请重试"))
            self.mccard.TransparentToolButton_3.clicked.connect(
                lambda *args, t=self.mccard: self.createErrorInfoBar(title="系统消息",
                                                                     content=f"{t.StrongBodyLabel.text()}.bat生成失败，该功能未开发"))

            # mccard.StrongBodyLabel.setText(f"mccard{i}")
            # mccard.TransparentToolButton_5.clicked.connect(lambda *args, t=mccard: print(t.StrongBodyLabel.text()))
            self.form2.verticalLayout_2.addWidget(self.mccard)
        self.form2.verticalLayout_2.addItem(self.form2.spacerItem1)

    def Plugin(self):

        self.pos2 = NavigationItemPosition.SCROLL

        # 压缩文件所在的目录

        self.layout = FlowLayout(needAni=True)
        self.plugin.gridLayout_2.addLayout(self.layout, 0, 0, 1, 1)

        # customize animation
        self.layout.setAnimation(250, QEasingCurve.OutQuad)

        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setVerticalSpacing(20)
        self.layout.setHorizontalSpacing(10)

        folder_path = ".\Plugin"

        # 遍历目录下的所有zip文件
        index = 0
        for file_name in os.listdir(folder_path):
            self.pluginwidget = Pluginwidget()

            # 判断文件是否为yml3文件
            if file_name.endswith(".yml3"):

                # 拼接文件的完整路径

                files_name = os.path.splitext(file_name)
                file_path = os.path.join(folder_path, files_name[0])
                import json

                # 判断是否已经解压
                if Path(file_path).is_dir():
                    with open(f'{file_path}\\pulgin.json', 'r', encoding="UTF-8") as f:
                        data_str = f.read()
                    pluginjson = json.loads(data_str)
                    self.pulgs.append((files_name, pluginjson[0]))
                    self.pluginwidget.setObjectName(f"widget{file_path}")
                    self.pluginwidget.PushButton_2.clicked.connect(
                        self.runPlugin(index, jsons=pluginjson, file_path=file_path))
                    self.pluginwidget.PushButton_3.clicked.connect(
                        self.closeplugin(index, jsons=pluginjson, file_path=file_path))

                    self.pluginwidget.StrongBodyLabel.setText(pluginjson[0]["plugin name"])
                    self.pluginwidget.BodyLabel.setText("作者：" + pluginjson[0]["plugin author"])
                    self.pluginwidget.BodyLabel_2.setText("版本：" + pluginjson[0]["version"])
                    self.pluginwidget.StrongBodyLabel.setToolTip(pluginjson[0]["plugin name"])
                    self.pluginwidget.StrongBodyLabel.setToolTipDuration(1000)
                    # self.button2.setToolTipDuration(-1)  # won't disappear

                    self.pluginwidget.StrongBodyLabel.installEventFilter(
                        ToolTipFilter(self.pluginwidget.StrongBodyLabel, 0, ToolTipPosition.BOTTOM_RIGHT))

                    try:
                        icon = pluginjson[0]["icon"]
                        self.pluginwidget.PixmapLabel.setStyleSheet(f"border-image: url({icon});")

                    except:
                        self.pluginwidget.PixmapLabel.setStyleSheet("border-image: url(:/built-InIcons/YML3logo.png);")

                    self.layout.addWidget(self.pluginwidget)

                    index += 1

                    if pluginjson[0]["state"] == "on":
                        Plugginname2 = f'Plugin.{files_name[0]}.{files_name[0]}'
                        module2 = __import__(Plugginname2)
                        win = eval(f"module2.{files_name[0]}.{files_name[0]}.{pluginjson[0]['from name']}")()
                        try:
                            self.addSubInterface(win,
                                                 eval(f"FluentIcon.{pluginjson[0]['interface icon']}"),
                                                 pluginjson[0]['interface name'],
                                                 self.pos2
                                                 )
                        except:
                            self.addSubInterface(win,
                                                 FluentIcon.MORE,
                                                 pluginjson[0]['interface name'],
                                                 self.pos2
                                                 )








                else:

                    file_path2 = os.path.join(file_path + ".yml3")
                    # 打开yml3文件
                    with zipfile.ZipFile(file_path2, "r") as zip_ref:
                        for info in zip_ref.infolist():
                            filename = info.filename.encode('cp437').decode('gbk')
                            zip_ref.extract(info, folder_path)

                    if Path(file_path).is_dir():
                        with open(f'{file_path}\\pulgin.json', 'r', encoding="UTF-8") as f:
                            data_str = f.read()
                        pluginjson = json.loads(data_str)
                        self.pulgs.append((files_name, pluginjson[0]))
                        self.pluginwidget.setObjectName(f"widget{file_path}")
                        self.pluginwidget.PushButton_2.clicked.connect(
                            self.runPlugin(index, jsons=pluginjson, file_path=file_path))
                        self.pluginwidget.PushButton_3.clicked.connect(
                            self.closeplugin(index, jsons=pluginjson, file_path=file_path))

                        self.pluginwidget.StrongBodyLabel.setText(pluginjson[0]["plugin name"])
                        self.pluginwidget.BodyLabel.setText("作者：" + pluginjson[0]["plugin author"])
                        self.pluginwidget.BodyLabel_2.setText("版本：" + pluginjson[0]["version"])
                        self.pluginwidget.StrongBodyLabel.setToolTip(pluginjson[0]["plugin name"])
                        self.pluginwidget.StrongBodyLabel.setToolTipDuration(1000)
                        # self.button2.setToolTipDuration(-1)  # won't disappear

                        self.pluginwidget.StrongBodyLabel.installEventFilter(
                            ToolTipFilter(self.pluginwidget.StrongBodyLabel, 0, ToolTipPosition.BOTTOM_RIGHT))

                        try:
                            icon = pluginjson[0]["icon"]
                            self.pluginwidget.PixmapLabel.setStyleSheet(f"border-image: url({icon});")

                        except:
                            self.pluginwidget.PixmapLabel.setStyleSheet(
                                "border-image: url(:/built-InIcons/YML3logo.png);")

                        self.layout.addWidget(self.pluginwidget)

                        index += 1

                        if pluginjson[0]["state"] == "on":
                            Plugginname2 = f'Plugin.{files_name[0]}.{files_name[0]}'
                            module2 = __import__(Plugginname2)
                            win = eval(f"module2.{files_name[0]}.{files_name[0]}.{pluginjson[0]['from name']}")()
                            try:
                                self.addSubInterface(win,
                                                     eval(f"FluentIcon.{pluginjson[0]['interface icon']}"),
                                                     pluginjson[0]['interface name'],
                                                     self.pos2
                                                     )
                            except:
                                self.addSubInterface(win,
                                                     FluentIcon.MORE,
                                                     pluginjson[0]['interface name'],
                                                     self.pos2
                                                     )

    def somePlugin(self):

        self.pos2 = NavigationItemPosition.SCROLL

        # 压缩文件所在的目录

        self.layout2 = FlowLayout(needAni=True)
        self.plugin.gridLayout_5.addLayout(self.layout2, 0, 0, 1, 1)

        # customize animation
        self.layout2.setAnimation(250, QEasingCurve.OutQuad)

        self.layout2.setContentsMargins(30, 30, 30, 30)
        self.layout2.setVerticalSpacing(20)
        self.layout2.setHorizontalSpacing(10)

        folder_path = ".\Plugin"

        # 遍历目录下的所有zip文件
        index2 = 0
        for file_name in os.listdir(folder_path):
            self.pluginwidget = Pluginwidget()

            # 判断文件是否为yml3文件
            if file_name.endswith(".YML3"):

                # 拼接文件的完整路径

                files_name = os.path.splitext(file_name)
                file_path = os.path.join(folder_path, files_name[0])
                import json

                # 判断是否已经解压
                if Path(file_path).is_dir():
                    with open(f'{file_path}\\pulgin.json', 'r', encoding="UTF-8") as f:
                        data_str = f.read()
                    pluginjson = json.loads(data_str)

                    self.pulgs2.append((files_name, pluginjson[0]))
                    self.pluginwidget.setObjectName(f"widget{file_path}")
                    self.pluginwidget.PushButton_2.clicked.connect(
                        self.runsomePlugin(index2, jsons=pluginjson, file_path=file_path))
                    self.pluginwidget.PushButton_3.clicked.connect(
                        self.closesomeplugin(index2, jsons=pluginjson, file_path=file_path))

                    self.pluginwidget.StrongBodyLabel.setText(pluginjson[0]["plugin name"])
                    self.pluginwidget.BodyLabel.setText("作者：" + pluginjson[0]["plugin author"])
                    self.pluginwidget.BodyLabel_2.setText("版本：" + pluginjson[0]["version"])
                    self.pluginwidget.StrongBodyLabel.setToolTip(pluginjson[0]["plugin name"])
                    self.pluginwidget.StrongBodyLabel.setToolTipDuration(1000)
                    # self.button2.setToolTipDuration(-1)  # won't disappear

                    self.pluginwidget.StrongBodyLabel.installEventFilter(
                        ToolTipFilter(self.pluginwidget.StrongBodyLabel, 0, ToolTipPosition.BOTTOM_RIGHT))

                    try:
                        icon = pluginjson[0]["icon"]
                        self.pluginwidget.PixmapLabel.setStyleSheet(f"border-image: url({icon});")

                    except:
                        self.pluginwidget.PixmapLabel.setStyleSheet("border-image: url(:/built-InIcons/YML3logo.png);")

                    self.layout2.addWidget(self.pluginwidget)

                    if pluginjson[0]["state"] == "on":
                        filename, pluginjsons = self.pulgs2[index2]
                        Plugginname = f'Plugin.{filename[0]}.{filename[0]}'
                        module = __import__(Plugginname)
                        winApp = eval(f"module.{filename[0]}.{filename[0]}.{pluginjsons['from name']}")()
                        try:
                            self.addSubInterface(winApp,
                                                 eval(f"FluentIcon.{pluginjsons['interface icon']}"),
                                                 pluginjsons['interface name'],
                                                 self.pos2
                                                 )
                            for i in range(int(pluginjsons['several'])):
                                self.addSubInterface(
                                    eval(f"module.{filename[0]}.{filename[0]}.{pluginjsons[f'from name{i}']}")(),
                                    eval(f"FluentIcon.{pluginjsons[f'interface icon{i}']}"),
                                    pluginjsons[f'interface name{i}'],
                                    parent=winApp)



                        except:
                            self.addSubInterface(winApp,
                                                 FluentIcon.MORE,
                                                 pluginjson['interface name'],
                                                 self.pos2
                                                 )

                            for i in range(int(pluginjsons['several'])):
                                self.addSubInterface(
                                    eval(f"module.{filename[0]}.{filename[0]}.{pluginjsons[f'from name{i}']}")(),
                                    FluentIcon.MORE,
                                    pluginjsons[f'interface name{i}'],
                                    parent=winApp)

                    index2 += 1









                else:

                    file_path2 = os.path.join(file_path + ".YML3")
                    # 打开yml3文件
                    with zipfile.ZipFile(file_path2, "r") as zip_ref:
                        for info in zip_ref.infolist():
                            filename = info.filename.encode('cp437').decode('gbk')
                            zip_ref.extract(info, folder_path)

                    if Path(file_path).is_dir():
                        with open(f'{file_path}\\pulgin.json', 'r', encoding="UTF-8") as f:
                            data_str = f.read()
                        pluginjson = json.loads(data_str)
                        self.pulgs2.append((files_name, pluginjson[0]))
                        self.pluginwidget.setObjectName(f"widget{file_path}")
                        self.pluginwidget.PushButton_2.clicked.connect(
                            self.runsomePlugin(index2, jsons=pluginjson, file_path=file_path))
                        self.pluginwidget.PushButton_3.clicked.connect(
                            self.closesomeplugin(index2, jsons=pluginjson, file_path=file_path))

                        self.pluginwidget.StrongBodyLabel.setText(pluginjson[0]["plugin name"])
                        self.pluginwidget.BodyLabel.setText("作者：" + pluginjson[0]["plugin author"])
                        self.pluginwidget.BodyLabel_2.setText("版本：" + pluginjson[0]["version"])
                        self.pluginwidget.StrongBodyLabel.setToolTip(pluginjson[0]["plugin name"])
                        self.pluginwidget.StrongBodyLabel.setToolTipDuration(1000)
                        # self.button2.setToolTipDuration(-1)  # won't disappear

                        self.pluginwidget.StrongBodyLabel.installEventFilter(
                            ToolTipFilter(self.pluginwidget.StrongBodyLabel, 0, ToolTipPosition.BOTTOM_RIGHT))

                        try:
                            icon = pluginjson[0]["icon"]
                            self.pluginwidget.PixmapLabel.setStyleSheet(f"border-image: url({icon});")

                        except:
                            self.pluginwidget.PixmapLabel.setStyleSheet(
                                "border-image: url(:/built-InIcons/YML3logo.png);")

                        self.layout2.addWidget(self.pluginwidget)

                        if pluginjson[0]["state"] == "on":
                            filename, pluginjsons = self.pulgs2[index2]
                            Plugginname = f'Plugin.{filename[0]}.{filename[0]}'
                            module = __import__(Plugginname)
                            winApp = eval(f"module.{filename[0]}.{filename[0]}.{pluginjsons['from name']}")()
                            try:
                                self.addSubInterface(winApp,
                                                     eval(f"FluentIcon.{pluginjsons['interface icon']}"),
                                                     pluginjsons['interface name'],
                                                     self.pos2
                                                     )
                                for i in range(int(pluginjsons['several'])):
                                    self.addSubInterface(
                                        eval(f"module.{filename[0]}.{filename[0]}.{pluginjsons[f'from name{i}']}")(),
                                        eval(f"FluentIcon.{pluginjsons[f'interface icon{i}']}"),
                                        pluginjsons[f'interface name{i}'],
                                        parent=winApp)



                            except:
                                self.addSubInterface(winApp,
                                                     FluentIcon.MORE,
                                                     pluginjson['interface name'],
                                                     self.pos2
                                                     )

                                for i in range(int(pluginjsons['several'])):
                                    self.addSubInterface(
                                        eval(f"module.{filename[0]}.{filename[0]}.{pluginjsons[f'from name{i}']}")(),
                                        FluentIcon.MORE,
                                        pluginjsons[f'interface name{i}'],
                                        parent=winApp)

                        index2 += 1

    def runsomePlugin(self, index, jsons, file_path):

        # 闭包装饰器，
        def startPulg():
            filename, pluginjson = self.pulgs2[index]

            Plugginname = f'Plugin.{filename[0]}.{filename[0]}'
            module = __import__(Plugginname)
            winApp = eval(f"module.{filename[0]}.{filename[0]}.{pluginjson['from name']}")()
            try:
                self.addSubInterface(winApp,
                                     eval(f"FluentIcon.{pluginjson['interface icon']}"),
                                     pluginjson['interface name'],
                                     self.pos2
                                     )
                for i in range(int(pluginjson['several'])):
                    self.addSubInterface(eval(f"module.{filename[0]}.{filename[0]}.{pluginjson[f'from name{i}']}")(),
                                         eval(f"FluentIcon.{pluginjson[f'interface icon{i}']}"),
                                         pluginjson[f'interface name{i}'],
                                         parent=winApp)



            except:
                self.addSubInterface(winApp,
                                     FluentIcon.MORE,
                                     pluginjson['interface name'],
                                     self.pos2
                                     )

                for i in range(int(pluginjson['several'])):
                    self.addSubInterface(eval(f"module.{filename[0]}.{filename[0]}.{pluginjson[f'from name{i}']}")(),
                                         FluentIcon.MORE,
                                         pluginjson[f'interface name{i}'],
                                         parent=winApp)
            self.createSuccessInfoBar(title="多页插件消息", content=f"插件{pluginjson['plugin name']}启动成功")

            jsons[0]["state"] = "on"
            with open(f'{file_path}\\pulgin.json', 'w', encoding="UTF-8") as f:
                json.dump(jsons, f)

        return startPulg

    def closesomeplugin(self, index2, jsons, file_path):

        # 闭包装饰器，
        def startPulg():
            filename, pluginjson = self.pulgs2[index2]

            self.createErrorInfoBar(title="多页插件消息",
                                    content=f"插件{pluginjson['plugin name']}禁用成功,重启软件后生效")

            jsons[0]["state"] = "off"
            with open(f'{file_path}\\pulgin.json', 'w', encoding="UTF-8") as f:
                json.dump(jsons, f)
            # print(jsons)

        return startPulg

    def runPlugin(self, index, jsons, file_path):

        # 闭包装饰器，
        def startPulg():
            filename, pluginjson = self.pulgs[index]
            Plugginname = f'Plugin.{filename[0]}.{filename[0]}'
            module = __import__(Plugginname)
            winApp = eval(f"module.{filename[0]}.{filename[0]}.{pluginjson['from name']}")()
            try:
                self.addSubInterface(winApp,
                                     eval(f"FluentIcon.{pluginjson['interface icon']}"),
                                     pluginjson['interface name'],
                                     self.pos2
                                     )
            except:
                self.addSubInterface(winApp,
                                     FluentIcon.MORE,
                                     pluginjson['interface name'],
                                     self.pos2
                                     )
            self.createSuccessInfoBar(title="单页插件消息", content=f"插件{pluginjson['plugin name']}启动成功")

            jsons[0]["state"] = "on"
            with open(f'{file_path}\\pulgin.json', 'w', encoding="UTF-8") as f:
                json.dump(jsons, f)
            # print(jsons)

        return startPulg

    def closeplugin(self, index, jsons, file_path):

        # 闭包装饰器，
        def startPulg():
            filename, pluginjson = self.pulgs[index]

            self.createErrorInfoBar(title="单页插件消息",
                                    content=f"插件{pluginjson['plugin name']}禁用成功,重启软件后生效")

            jsons[0]["state"] = "off"
            with open(f'{file_path}\\pulgin.json', 'w', encoding="UTF-8") as f:
                json.dump(jsons, f)
            # print(jsons)

        return startPulg

    def createSuccessInfoBar(self, content, title):
        # convenient class mothod
        InfoBar.success(
            title=title,
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_LEFT,
            # position='Custom',   # NOTE: use custom info bar manager
            duration=2000,
            parent=self
        )

    def createErrorInfoBar(self, content, title):
        InfoBar.error(
            title=title,
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_LEFT,
            duration=-1,  # won't disappear automatically
            parent=self
        )

    def widgettheme(self, tag):
        i = tag
        if i == "AUTO":
            setTheme(Theme.DARK if darkdetect.isDark() else Theme.LIGHT)

            self.windowEffect.setMicaEffect(self.winId(), isDarkMode=True if darkdetect.isDark() else False, isAlt=True)
            # self.windowEffect.setAcrylicEffect(self.winId(), gradientColor="99")

        if i == "LIGHT":
            self.light()
        if i == "DARK":
            self.dark()

    def light(self):
        setTheme(Theme.LIGHT)
        self.windowEffect.setMicaEffect(self.winId(), isDarkMode=False, isAlt=True)

    def dark(self):
        setTheme(Theme.DARK)
        self.windowEffect.setMicaEffect(self.winId(), isDarkMode=True, isAlt=True)

        # self.windowEffect.setAcrylicEffect(self.winId(),gradientColor="F2F2F20")


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = window()
    w.show()
    app.exec_()
