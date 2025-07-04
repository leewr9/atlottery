import os
import sys
from functools import partial

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QIcon
from selenium import webdriver

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


if __name__ == "__main__":
    app = QApplication(sys.argv)

    driver = webdriver.Chrome()

    window = MainWindow(driver)
    window.show()

    exit_code = app.exec()

    driver.quit()

    sys.exit(exit_code)
