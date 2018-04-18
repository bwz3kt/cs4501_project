print("hey selenium is running")
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

    def test_user_login(self):
        username = "cyeung"
        password = "password"
        driver = self.driver
        driver.get("http://192.168.99.100:8000/")
        driver.find_element_by_id("id_username").send_keys(username)
        driver.find_element_by_id("id_username").send_keys(password)

        driver.implicitly_wait(20)
        assert "MemeMachine" in driver.page_source

    def test_home_page(self):
        driver = self.driver
        driver.get("http://192.168.99.100:8000/home/")
        assert "ApartFinder is a website to help renters find tenants easily!" in driver.page_source

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    print("main ran")
    unittest.main()