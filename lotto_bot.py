from PySide6.QtWidgets import QMessageBox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoAlertPresentException,
    NoSuchElementException,
    TimeoutException,
)


def handle_alert(driver) -> str | None:
    """
    Check for and accept JavaScript alert if present.
    Returns alert text or None if no alert.
    """
    try:
        alert = driver.switch_to.alert
        alert_text = alert.text
        alert.accept()
        return alert_text
    except NoAlertPresentException:
        return None


def get_balance(driver) -> str | None:
    """
    Retrieve the user's balance from main page.
    Returns balance string or None if element not found.
    """
    driver.get("https://www.dhlottery.co.kr/common.do?method=main")
    wait = WebDriverWait(driver, 10)
    try:
        money_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li.money a strong"))
        )
        return money_element.text
    except TimeoutException:
        return None


def buy(window, driver, quantity: int = 5) -> None:
    """
    Automate lotto purchase process.
    Shows warning dialog if purchase fails.
    """
    driver.get("https://ol.dhlottery.co.kr/olotto/game/game645.do")

    wait = WebDriverWait(driver, 10)

    try:
        auto_button = wait.until(EC.element_to_be_clickable((By.ID, "num2")))
        driver.execute_script("arguments[0].click();", auto_button)

        select = Select(driver.find_element(By.ID, "amoundApply"))
        select.select_by_value(str(quantity))

        select_button = driver.find_element(By.ID, "btnSelectNum")
        driver.execute_script("arguments[0].click();", select_button)

        buy_button = driver.find_element(By.ID, "btnBuy")
        driver.execute_script("arguments[0].click();", buy_button)

        driver.execute_script("closepopupLayerConfirm(true);")

        buy_report = driver.find_element(By.ID, "report")
        display_value = buy_report.value_of_css_property("display")

        if display_value == "none":
            recommend = driver.find_element(By.CSS_SELECTOR, "p.cont1")
            QMessageBox.warning(window, "구매 실패", recommend.text)
            return
    except (TimeoutException, NoSuchElementException) as e:
        QMessageBox.warning(window, "구매 실패", f"구매 중 오류가 발생했습니다:\n{e}")


def login(window, driver) -> None:
    """
    Handles login and logout process.
    Updates UI state accordingly.
    """
    is_logged_in = window.ui.pushButton_buy.isEnabled()

    if is_logged_in:
        try:
            driver.get("https://www.dhlottery.co.kr/user.do?method=logout&returnUrl=")
        except Exception as e:
            QMessageBox.warning(
                window, "오류", f"로그아웃 중 오류가 발생했습니다:\n{e}"
            )
        balance = 0
    else:
        driver.get("https://www.dhlottery.co.kr/user.do?method=login&returnUrl=")

        try:
            driver.find_element(By.NAME, "userId").clear()
            driver.find_element(By.NAME, "userId").send_keys(
                window.ui.lineEdit_id.text()
            )
            driver.find_element(By.NAME, "password").send_keys(
                window.ui.lineEdit_password.text()
            )

            driver.execute_script("check_if_Valid3();")

            alert_text = handle_alert(driver)
            if alert_text is not None:
                QMessageBox.warning(window, "로그인 실패", alert_text)
                return

            balance = get_balance(driver)
            if balance is None:
                QMessageBox.warning(
                    window, "로그인 실패", "예치금 정보를 가져올 수 없습니다."
                )
                return

            balance = balance.replace(",", "")[:-1]
        except (NoSuchElementException, TimeoutException) as e:
            QMessageBox.warning(
                window, "로그인 실패", f"로그인 중 오류가 발생했습니다:\n{e}"
            )
            return

    # UI 상태 업데이트
    window.ui.pushButton_login.setText("로그인" if is_logged_in else "로그아웃")
    window.ui.lineEdit_id.setEnabled(is_logged_in)
    window.ui.lineEdit_password.setEnabled(is_logged_in)
    window.ui.spinBox_count.setEnabled(not is_logged_in)
    window.ui.pushButton_buy.setEnabled(not is_logged_in)
    window.ui.lcdNumber_balance.setProperty("value", int(balance))
