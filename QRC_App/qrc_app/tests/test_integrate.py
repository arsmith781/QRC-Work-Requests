from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By


# driver = webdriver.Firefox()
# driver.get('https://github.com')


class IntegrationTests(LiveServerTestCase):
    # first simple proof of concept test for opening the server.
    def testHomePage(self):
        driver = webdriver.Firefox()
        # for some reason this requires the server to be running in another terminal but she working so we ball
        driver.get('http://127.0.0.1:8000/')  # go to the home page of the website
        assert "QRC Work Requests" in driver.title
        driver.quit()

    # proof of concept login test with already created user
    def testLogin(self):
        driver = webdriver.Firefox()
        # for some reason this requires the server to be running in another terminal but she working so we ball
        driver.get('http://127.0.0.1:8000/login/')  # go to the home page of the website

        # assume account is already created and is the following. This is for simplicity and headaches
        # userName: staffAccount1
        # password: 123staf!

        # find user name
        name_input = driver.find_element(By.ID, 'id_username')
        name_input.send_keys('staffAccount1')

        # find password
        password_input = driver.find_element(By.ID, 'id_password')
        password_input.send_keys('123staf!')

        # Find and click the login button (I had to add html for this in login.html -> name="loginTest")
        login_button = driver.find_element(By.NAME, 'loginTest')
        login_button.click()

        # assert that after login we made it to the home page
        self.assertEqual(driver.current_url, "http://127.0.0.1:8000/")

        driver.close()
