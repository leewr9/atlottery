from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException


def handle_alert(driver) -> str | None:
    try:
        alert = driver.switch_to.alert
        alert_text = alert.text
        alert.accept()
        return alert_text
    except NoAlertPresentException:
        return None


def login(window, driver) -> None:
    is_login = window.ui.pushButton_buy.isEnabled()

    if is_login:
        driver.get("https://www.dhlottery.co.kr/user.do?method=logout&returnUrl=")
        balance = 0
    else:
        driver.get("https://www.dhlottery.co.kr/user.do?method=login&returnUrl=")

        driver.find_element(By.NAME, "userId").clear()
        driver.find_element(By.NAME, "userId").send_keys(window.ui.lineEdit_id.text())
        driver.find_element(By.NAME, "password").send_keys(
            window.ui.lineEdit_password.text()
        )

        driver.execute_script("check_if_Valid3();")

        alert_text = handle_alert(driver)
        if alert_text is not None:
            from PySide6.QtWidgets import QMessageBox

            QMessageBox.warning(window, "로그인 실패", alert_text)
            return

        balance = get_balance(driver).replace(",", "")[:-1]

    window.ui.pushButton_login.setText("로그인" if is_login else "로그아웃")
    window.ui.lineEdit_id.setEnabled(is_login)
    window.ui.lineEdit_password.setEnabled(is_login)
    window.ui.spinBox_count.setEnabled(not is_login)
    window.ui.pushButton_buy.setEnabled(not is_login)
    window.ui.lcdNumber_balance.setProperty("value", int(balance))


def get_balance(driver) -> str:
    driver.get("https://www.dhlottery.co.kr/common.do?method=main")
    wait = WebDriverWait(driver, 10)

    money_element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "li.money a strong"))
    )
    return money_element.text


def buy_lotto_auto(driver, quantity: int = 5) -> None:
    driver.get("https://ol.dhlottery.co.kr/olotto/game/game645.do")

    auto_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "num2"))
    )
    driver.execute_script("arguments[0].click();", auto_button)

    select = Select(driver.find_element(By.ID, "amoundApply"))
    select.select_by_value(str(quantity))

    check_button = driver.find_element(By.ID, "btnSelectNum")
    driver.execute_script("arguments[0].click();", check_button)
