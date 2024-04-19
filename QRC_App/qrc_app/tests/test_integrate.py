import time

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
        driver.get('http://127.0.0.1:8000/login/')  # go to the login

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

    # go to the model creation page witout being logged in
    def testCreatingAModel_noLogin(self):
        driver = webdriver.Firefox()
        # for some reason this requires the server to be running in another terminal but she working so we ball
        driver.get('http://127.0.0.1:8000/workrequest/create_request/')  # go to the creation page of the website

        # we should have been redirected to a login screen. I found the URL for when I do it so lets check it
        self.assertEqual(driver.current_url, "http://127.0.0.1:8000/login/?next=/workrequest/create_request/")

        driver.close()

    # try to create a model. A success if seeing the model on the list page
    def testCreatingAModel_withLogin(self):
        # ******** start code ripped from test login **********
        driver = webdriver.Firefox()
        # for some reason this requires the server to be running in another terminal but she working so we ball
        driver.get('http://127.0.0.1:8000/login/')  # go to the login

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
        # ******** end code ripped from test login **********

        # start creation test
        driver.get('http://127.0.0.1:8000/workrequest/create_request/')  # go to the creation page of the website

        name_input = driver.find_element(By.ID, 'id_submitter_name')
        name_input.send_keys('Integrate Test')

        contactInfo_input = driver.find_element(By.ID, 'id_contact_info')
        contactInfo_input.send_keys('integrateTest@123.com')

        # this is a dropdown
        location_input = driver.find_element(By.ID, 'id_location')
        location_input.send_keys('Shower Houses')

        # this is a dropdown
        sublocation_input = driver.find_element(By.ID, 'id_sub_location')
        sublocation_input.send_keys('Room 1-1')

        # this is a dropdown
        typeOfIssue_input = driver.find_element(By.ID, 'id_type_of_issue')
        typeOfIssue_input.send_keys('Furniture')

        description_input = driver.find_element(By.ID, 'id_description')
        description_input.send_keys('this is a description from a test case. No photo for simplicity')

        # now we can try to click the button
        # i dont like finding it this way but in my case theres only 1 on the form so do it.
        submit_button = driver.find_element(By.CLASS_NAME, 'btn-primary')
        submit_button.click()

        # I have a javascript popup after submit so let's deal with that
        # Switch to the alert mode for popups
        popup = driver.switch_to.alert

        # "click ok" on the popup
        popup.accept()

        # wait for the stuff to happen (database creation and page switch)
        time.sleep(2)
        page_source = driver.page_source
        # no task number since that is dynamic and no other " - Shower Houses Furniture" will exist
        assert ' - Shower Houses - Furniture' in page_source
        driver.close()




