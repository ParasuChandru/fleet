from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

def test_block_card_immediate_effect():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    # 1. Login as fleet manager
    driver.get("https://your-fleet-app-url/login")
    driver.find_element(By.ID, "username").send_keys("manager_user")
    driver.find_element(By.ID, "password").send_keys("manager_password")
    driver.find_element(By.ID, "loginButton").click()

    # 2. Navigate to card management
    wait.until(EC.presence_of_element_located((By.ID, "nav-cards"))).click()

    # 3. Search and select the card to block
    driver.find_element(By.ID, "searchCardInput").send_keys("CARD1234")
    driver.find_element(By.ID, "searchCardButton").click()
    wait.until(EC.presence_of_element_located((By.XPATH, "//tr[td/text()='CARD1234']"))).click()

    # 4. Initiate block on the card
    driver.find_element(By.ID, "blockCardButton").click()
    wait.until(EC.text_to_be_present_in_element((By.ID, "toastMessage"), "Card successfully blocked"))

    # 5. Confirm card is marked as blocked in UI
    status = driver.find_element(By.ID, "cardStatus").text
    assert status == "Blocked", "Card status not updated to Blocked"
    
    # 6. Simulate driver transaction attempt
    resp = requests.post("https://fleet-app-backend/api/transaction", json={
        "card_id": "CARD1234",
        "amount": 10,
        "merchant": "SHELL"
    })
    assert resp.json()["status"] == "declined", "Transaction should have been declined for blocked card"
    assert resp.json()["reason"] == "Card is blocked"

    driver.quit()
