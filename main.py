from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

def login(driver, user_id: str, password: str) -> None:
    driver.get("https://www.dhlottery.co.kr/user.do?method=login&returnUrl=")
    driver.find_element(By.NAME, "userId").send_keys(user_id)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.execute_script("check_if_Valid3();")

def get_balance(driver) -> str:
    driver.get("https://www.dhlottery.co.kr/common.do?method=main")
    wait = WebDriverWait(driver, 10)
    money_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.money a strong")))
    return money_element.text

def buy_lotto_auto(driver, quantity: int = 5) -> None:
    driver.get("https://ol.dhlottery.co.kr/olotto/game/game645.do")

    auto_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "num2")))
    driver.execute_script("arguments[0].click();", auto_button)

    select = Select(driver.find_element(By.ID, "amoundApply"))
    select.select_by_value(str(quantity))

    check_button = driver.find_element(By.ID, "btnSelectNum")
    driver.execute_script("arguments[0].click();", check_button)

def main():
    driver = webdriver.Chrome()
    try:
        login(driver, user_id="user_id", password="password")

        balance = get_balance(driver)
        print("예치금:", balance)

        buy_lotto_auto(driver, quantity=5)

        time.sleep(10)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
