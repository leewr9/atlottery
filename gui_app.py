import os
import sys
import webbrowser
from functools import partial

from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtGui import QIcon, QAction

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

import app.core.lottery_bot as bot
from app.ui.main_window import Ui_atlottery


def resource_path(relative_path: str) -> str:
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

        # Connect buttons
        self.ui.pushButton_login.clicked.connect(self.handle_login_logout)
        self.ui.pushButton_buy.clicked.connect(self.handle_buy)

        # Setup menu actions
        action_site = QAction("홈페이지", self)
        action_site.triggered.connect(
            partial(self.open_url, "https://www.dhlottery.co.kr/")
        )
        action_payment = QAction("충전", self)
        action_payment.triggered.connect(
            partial(
                self.open_url, "https://www.dhlottery.co.kr/payment.do?method=payment"
            )
        )
        action_purchase = QAction("구매내역", self)
        action_purchase.triggered.connect(
            partial(
                self.open_url,
                "https://www.dhlottery.co.kr/myPage.do?method=lottoBuyListView",
            )
        )
        self.action_refresh = QAction("새로고침", self)
        self.action_refresh.triggered.connect(self.refresh_ui)
        self.action_refresh.setEnabled(False)

        self.menuBar().clear()
        self.menuBar().addAction(action_site)
        self.menuBar().addAction(action_payment)
        self.menuBar().addAction(action_purchase)
        self.menuBar().addAction(self.action_refresh)

        self.driver = driver
        self.is_login = False

    def handle_login_logout(self) -> None:
        if not self.is_login:
            result, message = bot.login(
                self.driver,
                self.ui.lineEdit_id.text(),
                self.ui.lineEdit_password.text(),
            )
            if result:
                self.refresh_ui()
                self.is_login = True

                if not self.ui.pushButton_buy.isEnabled():
                    QMessageBox.information(
                        self,
                        "예치금",
                        "예치금이 부족하여 구매할 수 없습니다.\n상단 메뉴에서 충전 후 시도해 주세요.",
                    )
            else:
                QMessageBox.warning(
                    self, "로그인 실패", f"로그인 중 오류가 발생했습니다.\n\n{message}"
                )
        else:
            result, message = bot.logout(self.driver)
            if result:
                self.ui.lcdNumber_balance.setProperty("value", 0)
                self.ui.pushButton_buy.setEnabled(False)
                self.is_login = False
            else:
                QMessageBox.warning(
                    self,
                    "로그아웃 실패",
                    f"로그아웃 중 오류가 발생했습니다.\n\n{message}",
                )

        self.ui.pushButton_login.setText("로그아웃" if self.is_login else "로그인")
        self.ui.lineEdit_id.setEnabled(not self.is_login)
        self.ui.lineEdit_password.setEnabled(not self.is_login)
        self.ui.spinBox_count.setEnabled(self.is_login)
        self.action_refresh.setEnabled(self.is_login)

    def handle_buy(self) -> None:
        result, message, numbers = bot.buy_lottery(
            self.driver, self.ui.spinBox_count.text()
        )
        if result:
            for number in numbers:
                line = "   ".join(f"{num:>3}" for num in number[1:])
                message += f"{number[0]}      {line}      \n"
            QMessageBox.information(
                self, "구매 성공", f"구매하신 번호는 다음과 같습니다.\n\n{message}"
            )
            self.refresh_ui()
        else:
            QMessageBox.warning(
                self, "구매 실패", f"구매 중 오류가 발생했습니다.\n\n{message}"
            )

    def refresh_ui(self) -> None:
        balance = bot.refresh_balance(self.driver)

        if balance is not None:
            self.ui.lcdNumber_balance.setProperty("value", int(balance))
            self.ui.pushButton_buy.setEnabled(int(balance) > 0)
        else:
            QMessageBox.warning(self, "예치금", "예치금 정보를 가져올 수 없습니다.")

    def open_url(self, url: str) -> None:
        webbrowser.open(url)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    window = MainWindow(driver)
    window.show()

    exit_code = app.exec()

    driver.quit()
    sys.exit(exit_code)
