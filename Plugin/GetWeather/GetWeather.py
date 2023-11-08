from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit
from PyQt5.QtCore import Qt
import sys
import requests
import geocoder
import os
import configparser


def get_weather(city, api_key, language, unit):
    base_url = "https://api.seniverse.com/v3/weather/daily.json"
    params = {"location": city, "key": api_key, "language": language, "unit": unit, "start": 0, "days": 3}
    response = requests.get(base_url, params=params)
    data = response.json()
    if 'results' in data:
        weather = data['results'][0]['daily']
        last_upd = data['results'][0]['last_update']
        date, time = last_upd.split("T")
        year, month, day = date.split("-")
        if "+" in time:
            time, _ = time.split("+")
        hour, minute, second = time.split(":")
        last_upd2 = year + "年" + month + "月" + day + "日-" + hour + "点" + minute + "分" + second + "秒"
        forecast_text = f"城市：{city}\n上次更新：{last_upd2}\n"
        for day_weather in weather:
            forecast_text += f"\n日期：{day_weather['date']}\n白天天气：{day_weather['text_day']}\n夜晚天气：{day_weather['text_night']}\n最高温度：{day_weather['high']}°{unit.upper()}\n最低温度：{day_weather['low']}°{unit.upper()}\n"
        return forecast_text
    else:
        return "无法获取天气数据，请检查你的城市名和API密钥是否正确。"


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.config = configparser.ConfigParser()
        self.config.read('settings/settings.ini')
        city = self.config['DEFAULT']['City']
        g = geocoder.ip('me')
        city = g.city
        self.config['DEFAULT']['City'] = city
        with open('settings/settings.ini', 'w') as configfile:
            self.config.write(configfile)
        self.city_entry = QLineEdit(self)
        self.city_entry.setText(city)
        self.language_entry = QLineEdit(self)
        self.language_entry.setText("zh-Hans")
        self.unit_entry = QLineEdit(self)
        self.unit_entry.setText("c")
        self.submit_button = QPushButton("查询", self)
        self.submit_button.clicked.connect(self.on_submit)
        self.log_text = QTextEdit(self)
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_entry)
        vbox.addWidget(self.language_entry)
        vbox.addWidget(self.unit_entry)
        vbox.addWidget(self.submit_button)
        vbox.addWidget(self.log_text)
        self.setLayout(vbox)
        self.setGeometry(300, 300, 800, 600)

        # 设置样式表
        self.setStyleSheet("""
                    QWidget {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #00716F, stop:1 #12A5A6);
                        font-family: 'Arial';
                    }
                    QLineEdit, QTextEdit {
                        background-color: #fff;
                        color: #333;
                        border: none;
                        border-radius: 5px;
                        font-size: 16px;
                    }
                    QPushButton {
                        background-color: #0082fa;
                        color: #fff;
                        border-radius: 5px;
                        padding: 5px;
                        transition-duration: 0.4s;
                        font-size: 16px;
                    }
                    QPushButton:hover {
                        background-color: #0056b3;
                        color: white;
                        border-radius: 15px;
                    }
                """)
        self.show()

    def on_submit(self):
        city = self.city_entry.text()
        language = self.language_entry.text()
        unit = self.unit_entry.text()
        api_key = os.environ.get("SENIVERSE_API_KEY") or self.config['DEFAULT']['API_KEY']
        try:
            result = get_weather(city, api_key, language, unit)
            self.log_text.append(f"{result}\n")
            QApplication.processEvents()
            sb = self.log_text.verticalScrollBar()
            sb.setValue(sb.maximum())
        except Exception as e:
            self.log_text.append(f"查询失败：{str(e)}\n")
            QApplication.processEvents()