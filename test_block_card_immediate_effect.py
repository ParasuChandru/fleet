from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time

def test_block_card_instant_effect():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    # 1. Login with MFA
    driver.get("https://your-fleet-app-url/login")
    driver.find_element(By.ID, "username").send_keys("manager_user")
    driver.find_element(By.ID, "password").send_keys("manager_password")
    driver.find_element(By.ID, "loginButton").click()

    # MFA step
    otp = get_otp_from_email_or_api()  # Implement OTP retrieval as per actual system
    driver.find_element(By.ID, "otpInput").send_keys(otp)
    driver.find_element(By.ID, "verifyButton").click()

    # 2. Start timer for block action speed requirement
    wait.until(EC.presence_of_element_located((By.ID, "nav-cards"))).click()
    driver.find_element(By.ID, "searchCardInput").send_keys("CARD1234")
    driver.find_element(By.ID, "searchCardButton").click()
    wait.until(EC.presence_of_element_located((By.XPATH, "//tr[td/text()='CARD1234']"))).click()
    start_time = time.time()

    driver.find_element(By.ID, "blockCardButton").click()
    wait.until(EC.text_to_be_present_in_element((By.ID, "toastMessage"), "Card successfully blocked"))
    end_time = time.time()
    assert end_time - start_time <= 5, f"Block took {end_time - start_time:.2f}s, should complete in ≤5s"

    # 3. Check real-time notification (simulate if possible or assert in-app message)
    notification = wait.until(EC.presence_of_element_located((By.ID, "notificationPanel"))).text
    assert "Card blocked" in notification, "Real-time notification missing"

    # 4. Confirm card status in UI is 'Blocked'
    status = driver.find_element(By.ID, "cardStatus").text
    assert status == "Blocked", "Card status not updated to Blocked"

    # 5. Attempt transaction – must fail
    resp = requests.post("https://fleet-app-backend/api/transaction", json={
        "card_id": "CARD1234",
        "amount": 10,
        "merchant": "SHELL"
    })
    assert resp.json()["status"] == "declined", "Transaction allowed for blocked card"
    assert resp.json()["reason"] == "Card is blocked"

    # 6. Confirm audit log entry exists (simulate log API call)
    log_resp = requests.get("https://fleet-app-backend/api/audit-logs?card_id=CARD1234&type=block")
    assert len(log_resp.json()["logs"]) > 0, "No audit log for block event"

    driver.quit()

def get_otp_from_email_or_api():
    # Placeholder: Replace with actual retrieval logic
    return "123456"
