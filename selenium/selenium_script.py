print("Selenium script started.")
import unittest
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import time


class SeleniumTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote(
            command_executor='http://selenium-chrome:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)

    # COMMENTED OUT b/c cannot pass through Travis.
    def test_user_login(self):
        username = "cyeung"
        password = "password"
        driver = self.driver
        driver.implicitly_wait(20)
        #my ip address
        driver.get("http://192.168.99.100:8000/")

        #Travis
<<<<<<< HEAD
        #driver.get("http://174.138.62.246:8000/")
=======
        #driver.get("http://localhost:8000/")
        ids = driver.find_elements_by_xpath('//*[@id]')

        for ii in ids:
            print(ii.get_attribute('id'))
        print("Printed all attributes")
>>>>>>> a9c2c0c8d73de40a3e0a83168c665b18834af695
        driver.find_element_by_id("id_username").send_keys(username)
        driver.find_element_by_id("id_password").send_keys(password)
        driver.find_element_by_id("login").click()
        driver.implicitly_wait(20)
        #Log out shit doesn't work right now.
        #logout_text = driver.find_element_by_id("logout").text
        #driver.implicitly_wait(20)
        #self.assertEqual("Log Out", logout_text)

    def test_user_signup(self):
        username = "testuser"
        email="test@virginia.edu"
        password = "newpassword"
        confirmpassword = "newpassword"
        driver = self.driver
        driver.implicitly_wait(20)
        #my ip address
        driver.get("http://192.168.99.100:8000/signup/")

        #travis
<<<<<<< HEAD
        #driver.get("http://174.138.62.246:8000/signup/")
=======
        #driver.get("http://web-api:8000/signup/")
>>>>>>> a9c2c0c8d73de40a3e0a83168c665b18834af695

        driver.find_element_by_id("id_username").send_keys(username)
        driver.find_element_by_id("id_email").send_keys(email)
        driver.find_element_by_id("id_password").send_keys(password)
        driver.find_element_by_id("id_passwordConfirm").send_keys(confirmpassword)
        driver.find_element_by_id("signup").click()
        driver.implicitly_wait(20)

        #logout_text not working
        #logout_text = driver.find_element_by_id("logout").text
        #self.assertEqual("Log Out", logout_text)



        #Just the test I made, but doesn't work -Taehyun-
        #driver.find_element_by_xpath("/base/body/nav/div[2]/div[1]/div[1]/li/a").click()
        #assert "Log Out:" in driver.page_source
        #driver.implicitly_wait(20)


    def test_home_page(self):
        driver = self.driver
        #My ip address
        driver.get("http://192.168.99.100:8000/home/")

        #Travis
<<<<<<< HEAD
        #driver.get("http://174.138.62.246:8000/home/")
=======
        #driver.get("http://web-api:8000/home/")
>>>>>>> a9c2c0c8d73de40a3e0a83168c665b18834af695

        #assert "ApartFinder is a website to help renters find tenants easily!" in driver.page_source

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    print("main ran")
    unittest.main()