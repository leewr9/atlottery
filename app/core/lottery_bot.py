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
    Handle a browser alert if present and return its text.

    Args:
        driver: Selenium WebDriver instance.

    Returns:
        Alert text if present, otherwise None.
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
    Retrieve the account balance from the lottery website.

    Args:
        driver: Selenium WebDriver instance.

    Returns:
        Balance as a string, or None if retrieval fails.
    """
    driver.get("https://www.dhlottery.co.kr/common.do?method=main")
    wait = WebDriverWait(driver, 10)
    try:
        balance_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li.money a strong"))
        )
        return balance_element.text
    except TimeoutException:
        return None


def get_history(driver) -> str | None:
    """
    Fetch the purchase history of lottery tickets.

    Args:
        driver: Selenium WebDriver instance.

    Returns:
        Purchase history as a formatted string, or None if retrieval fails.
    """
    try:
        history_message = f"로또 6/45 - {driver.find_element(
            By.CSS_SELECTOR, "div.date-info h3 strong"
        ).text}\n"
        history_message += "\n"

        for history_item in driver.find_elements(
            By.CSS_SELECTOR, "div.date-info ul li"
        ):
            history_message += history_item.text + "\n"

        history_message += "\n"
        purchased_numbers = driver.find_elements(
            By.CSS_SELECTOR, "div.selected ul li .nums"
        )

        history_numbers = []
        for i, number_group in enumerate(purchased_numbers):
            numbers = [chr(65 + i)]
            for span in number_group.find_elements(By.TAG_NAME, "span"):
                num = int(span.text)
                if num not in numbers:
                    numbers.append(num)
            history_numbers.append(numbers)

        return history_message, history_numbers
    except TimeoutException:
        return None


def refresh_balance(driver) -> str | None:
    """
    Refresh and return the current account balance.

    Args:
        driver: Selenium WebDriver instance.

    Returns:
        Updated balance as a string, or None if refresh fails.
    """
    try:
        balance_text = get_balance(driver)
        if balance_text is None:
            raise Exception(
                "Balance retrieval failed: None returned from get_balance()."
            )
        cleaned_balance = balance_text.replace(",", "")[:-1]
        return cleaned_balance
    except Exception:
        return None


def buy_lottery(driver, ticket_count: int) -> tuple[bool, str, list]:
    """
    Purchase a specified number of lottery tickets.

    Args:
        driver: Selenium WebDriver instance.
        ticket_count: Number of tickets to purchase.

    Returns:
        Tuple of (success flag, message or error).
    """
    driver.get("https://ol.dhlottery.co.kr/olotto/game/game645.do")

    try:
        wait = WebDriverWait(driver, 10)
        auto_button = wait.until(EC.element_to_be_clickable((By.ID, "num2")))
        driver.execute_script("arguments[0].click();", auto_button)

        ticket_selector = Select(driver.find_element(By.ID, "amoundApply"))
        ticket_selector.select_by_value(str(ticket_count))

        select_button = driver.find_element(By.ID, "btnSelectNum")
        driver.execute_script("arguments[0].click();", select_button)

        buy_button = driver.find_element(By.ID, "btnBuy")
        driver.execute_script("arguments[0].click();", buy_button)

        driver.execute_script("closepopupLayerConfirm(true);")

        purchase_report = driver.find_element(By.ID, "report")
        display_value = purchase_report.value_of_css_property("display")

        if display_value == "none":
            error_element = driver.find_element(
                By.CSS_SELECTOR, "#recommend720Plus > div > div.status > p.cont1"
            )
            if not error_element.text:
                error_element = driver.find_element(
                    By.CSS_SELECTOR, "#popupLayerAlert > div > div.noti > span"
                )
            return False, error_element.text, []
        else:
            message, numbers = get_history(driver)
            if message is None:
                return False, "구매 내역을 가져올 수 없습니다.", []

            return True, message, numbers
    except (TimeoutException, NoSuchElementException) as e:
        return False, str(e), []


def logout(driver) -> tuple[bool, str]:
    """
    Log out from the lottery website.

    Args:
        driver: Selenium WebDriver instance.

    Returns:
        Tuple of (success flag, message).
    """
    try:
        driver.get("https://www.dhlottery.co.kr/user.do?method=logout&returnUrl=")
    except Exception as e:
        return False, str(e)

    return True, "Logout successful"


def login(driver, user_id: str, password: str) -> tuple[bool, str]:
    """
    Log in to the lottery website using provided credentials.

    Args:
        driver: Selenium WebDriver instance.
        user_id: User ID.
        password: User password.

    Returns:
        Tuple of (success flag, message or error).
    """
    try:
        driver.get("https://www.dhlottery.co.kr/user.do?method=login&returnUrl=")

        driver.find_element(By.NAME, "userId").clear()
        driver.find_element(By.NAME, "userId").send_keys(user_id)
        driver.find_element(By.NAME, "password").send_keys(password)

        driver.execute_script("check_if_Valid3();")

        import time

        time.sleep(1)

        alert_text = handle_alert(driver)
        if alert_text is not None:
            return False, alert_text

        return True, "Login successful"
    except (NoSuchElementException, TimeoutException) as e:
        return False, str(e)
