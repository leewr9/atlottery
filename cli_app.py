import os

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.policy import SMTP

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import app.core.lottery_bot as bot

LOTTERY_USER = os.getenv("LOTTERY_USER", None)
LOTTERY_PASS = os.getenv("LOTTERY_PASS", None)
LOTTERY_COUNT = int(os.getenv("LOTTERY_COUNT", 5))

EMAIL_SENDER = os.getenv("EMAIL_SENDER", None)
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", None)


def notify_email(subject: str, html: str) -> bool:
    try:
        if EMAIL_SENDER and EMAIL_PASSWORD:
            print("Email credentials found, sending email...")
            msg = MIMEMultipart(policy=SMTP)
            msg["From"] = f"동행복권 자동구매 {EMAIL_SENDER}"
            msg["To"] = EMAIL_SENDER
            msg["Subject"] = subject
            msg.attach(MIMEText(html, "html", "utf-8"))

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                server.send_message(msg)
            print("Email sent successful")
        else:
            print("Email credentials missing, email not sent.")

        return True
    except Exception as e:
        print(f"Email sent failed: {e}")
        return False


def notify_success(message: str, numbers: list, balance: int) -> bool:
    purchase_table = "<table cellspacing='0' cellpadding='0'>\n"

    for number in numbers:
        purchase_table += "<tr>\n"
        purchase_table += f"<td style='width:37px; height:24px; text-align:center; font-weight: bold;'>{number[0]}</td>\n"
        for num in number[1:]:
            purchase_table += (
                f"<td style='width:37px; height:24px; text-align:center;'>{num}</td>\n"
            )
        purchase_table += "</tr>\n"

    purchase_table += "</table>"

    html_body = f"""
<html>
  <body>
    <img src="https://leewr9.github.io/assets/docs/atlottery/title.png">
    
    <p>이번 회차 로또 구매가 성공적으로 완료되었습니다.</p>

    <p style="font-weight: bold;">구매 번호:</p>
    <div style="border-left: 3px solid silver; padding: 10px;">
        <p>{message.replace("\n", "<br>")}</p>
        {purchase_table}
    </div>

    <p><strong>예치금 잔액:</strong> {balance}원</p>
    
    <p>--</p>

    <p style="color: gray;">
      동행복권 홈페이지: <a href="https://www.dhlottery.co.kr">https://www.dhlottery.co.kr</a><br>
      자동구매 문의: <a href="mailto:leewr9@gmail.com">leewr9@gmail.com</a>
    </p>
  </body>
</html>
"""
    return notify_email("[동행복권 자동구매] 구매 완료", html_body)


def notify_failure(message: str) -> bool:
    html_body = f"""
<html>
  <body>
    <img src="https://leewr9.github.io/assets/docs/atlottery/title.png">
    
    <p>문제가 발생하여 이번 회차 로또 구매가 완료되지 않았습니다.</p>

    <p style="font-weight: bold;">원인:</p>
    <p style="border-left: 3px solid silver; padding: 10px;">
        {message.replace("\n", "<br>")}
    </p>

    <p>예치금 확인 또는 다음 회차에 다시 시도해 주세요.</p>
    
    <p>--</p>

    <p style="color: gray;">
      동행복권 홈페이지: <a href="https://www.dhlottery.co.kr">https://www.dhlottery.co.kr</a><br>
      자동구매 문의: <a href="mailto:leewr9@gmail.com">leewr9@gmail.com</a>
    </p>
  </body>
</html>
"""
    return not notify_email("[동행복권 자동구매] 구매 실패 안내", html_body)


def main(driver: webdriver.Chrome) -> bool:
    print("Starting Auto Lottoery Purchase")

    print("Attempting login...")
    if LOTTERY_USER and LOTTERY_PASS:
        result, message = bot.login(driver, LOTTERY_USER, LOTTERY_PASS)
        if not result:
            print(f"Login failed: {message}")
            return notify_failure(message)
        print("Login successful")

        print("Checking balance...")
        balance = bot.refresh_balance(driver)
        if not balance:
            print("Cannot retrieve balance information.")
            return notify_failure("예치금 정보를 가져올 수 없습니다.")
        if balance and int(balance) <= 0:
            print(f"Insufficient balance: {balance}")
            return notify_failure("예치금이 부족합니다.")
        print(f"Balance check completed: {balance}")

        print(f"Attempting to purchase {LOTTERY_COUNT} lottery tickets...")
        result, message, numbers = bot.buy_lottery(driver, LOTTERY_COUNT)
        if result:
            print("Lotto purchase successful")
            return notify_success(message, numbers, balance)
        else:
            print(f"Lotto purchase failed: {message}")
            return notify_failure(message)
    else:
        print("Lotto account credentials missing, cannot proceed.")
        return False


if __name__ == "__main__":
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )

    try:
        if main(driver):
            print("Auto Lottoery Purchase Success")
        else:
            raise Exception("Auto Lottoery Purchase Failed")
    finally:
        driver.quit()
