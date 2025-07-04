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


class MainWindow(QMainWindow):
    def __init__(self, driver):
        super().__init__()
        self.setWindowTitle("자동구매 | 동행복권")
        self.setWindowIcon(QIcon(os.path.join("resources", "favicon.ico")))

        self.ui = Ui_atlottery()
        self.ui.setupUi(self)

        self.ui.pushButton_login.clicked.connect(partial(bot.login, self, driver))
        self.ui.pushButton_buy.clicked.connect(partial(bot.buy, self, driver))

        action_site = QAction("동행복권 바로가기", self)
        action_site.triggered.connect(self.open_url)

        self.menuBar().clear()
        self.menuBar().addAction(action_site)

    def open_url(self):
        webbrowser.open("https://www.dhlottery.co.kr/")


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
