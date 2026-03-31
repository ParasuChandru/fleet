import unittest
from appium import webdriver

class MobileBankingAppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        desired_caps = {
            'platformName': 'Android',
            'deviceName': 'Android Emulator',
            'appPackage': 'com.example.bankingapp',
            'appActivity': '.MainActivity',
            'automationName': 'UiAutomator2'
        }
        cls.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_01_login(self):
        self.driver.find_element_by_id('username_field').send_keys('testuser')
        self.driver.find_element_by_id('password_field').send_keys('password123')
        self.driver.find_element_by_id('login_button').click()
        self.assertTrue(self.driver.find_element_by_id('dashboard_title').is_displayed())

    def test_02_dashboard_summary(self):
        saving_balance = self.driver.find_element_by_id('savings_balance').text
        current_balance = self.driver.find_element_by_id('current_balance').text
        self.assertIsNotNone(saving_balance)
        self.assertIsNotNone(current_balance)
        transaction_summary = self.driver.find_element_by_id('transactions_summary')
        self.assertTrue(transaction_summary.is_displayed())

    def test_03_transfer_money(self):
        self.driver.find_element_by_id('transfer_button').click()
        self.driver.find_element_by_id('recipient_field').send_keys('john_doe')
        self.driver.find_element_by_id('amount_field').send_keys('500')
        self.driver.find_element_by_id('send_button').click()
        alert = self.driver.find_element_by_id('transfer_success_alert')
        self.assertTrue(alert.is_displayed())
        self.driver.find_element_by_id('alert_ok_button').click()

    def test_04_pay_bills(self):
        self.driver.find_element_by_id('pay_bills_button').click()
        self.assertTrue(self.driver.find_element_by_id('bill_pay_screen').is_displayed())
        self.driver.find_element_by_id('back_button').click()

    def test_05_navigation_home(self):
        self.driver.find_element_by_id('dashboard_home_button').click()
        self.assertTrue(self.driver.find_element_by_id('dashboard_title').is_displayed())

if __name__ == '__main__':
    unittest.main()