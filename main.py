import os
import sys
import webbrowser
from functools import partial

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QIcon, QAction

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import lotto_bot as bot
from main_ui import Ui_atlottery


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class MainWindow(QMainWindow):
    def __init__(self, driver):
        super().__init__()
        self.setWindowTitle("자동구매 | 동행복권")
        self.setWindowIcon(QIcon(resource_path("resources/favicon.ico")))

        self.ui = Ui_atlottery()
        self.ui.setupUi(self)

        self.ui.pushButton_login.clicked.connect(partial(bot.login, self, driver))
        self.ui.pushButton_buy.clicked.connect(partial(bot.buy, self, driver))

        self.action_site = QAction("홈페이지", self)
        self.action_site.triggered.connect(partial(self.open_url, "https://www.dhlottery.co.kr/"))
        self.action_payment = QAction("충전", self)
        self.action_payment.triggered.connect(partial(self.open_url, "https://www.dhlottery.co.kr/payment.do?method=payment"))
        self.action_refresh = QAction("새로고침", self)
        self.action_refresh.triggered.connect(partial(bot.refresh, self, driver))
        self.action_refresh.setEnabled(False)

        self.menuBar().clear()
        self.menuBar().addAction(self.action_site)
        self.menuBar().addAction(self.action_payment)
        self.menuBar().addAction(self.action_refresh)

    def open_url(self, url):
        webbrowser.open(url)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)

    window = MainWindow(driver)
    window.show()

    exit_code = app.exec()

    driver.quit()

    sys.exit(exit_code)
