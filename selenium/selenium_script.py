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

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    print("main ran")
    unittest.main()