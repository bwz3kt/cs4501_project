print("Selenium script started.")
import unittest
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
import time


class SeleniumTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote(
            command_executor='http://selenium-chrome:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)

    #User should be able to log in (test)
    def test_user_login(self):
        username = "tk9at"
        password = "wldnro"
        driver = self.driver
        #my ip address
        driver.get("http://192.168.99.100:8000")
        ids = driver.find_elements_by_xpath('//*[@id]')

        for ii in ids:
            print(ii.get_attribute('id'))
        print("Printed all attributes")

        driver.find_element_by_id("id_username").send_keys(username)
        driver.find_element_by_id("id_password").send_keys(password)
        driver.find_element_by_id("login").click()
        driver.implicitly_wait(20)
        #header_text = driver.find_element_by_tag_name("h3").text
        #driver.find_element_by_id("login").click()
        #print(header_text)
        self.assertEqual("Welcome to ApartFinder", driver.title)

    #User should be able to Sign up(test)
    def test_user_signup(self):
        username = "taechristes"
        email="taechristes@virginia.edu"
        password = "mypas"
        confirmpassword = "mypas"
        driver = self.driver
        #my ip address
        driver.get("http://192.168.99.100:8000/signup/")
        driver.find_element_by_id("id_username").send_keys(username)
        driver.find_element_by_id("id_email").send_keys(email)
        driver.find_element_by_id("id_password").send_keys(password)
        driver.find_element_by_id("id_passwordConfirm").send_keys(confirmpassword)
        driver.find_element_by_id("signup").click()
        driver.implicitly_wait(20)

        self.assertEqual("Welcome to ApartFinder", driver.title)

    #User should be able to Sign out (Test)
    def test_user_logout(self):
        driver = self.driver
        #My ip address
        driver.get("http://192.168.99.100:8000")
        username = "tk9at"
        password = "wldnro"
        driver.find_element_by_id("id_username").send_keys(username)
        driver.find_element_by_id("id_password").send_keys(password)
        driver.find_element_by_id("login").click()
        driver.implicitly_wait(20)
        driver.find_element_by_id("logout").click()
        header_text = driver.find_element_by_tag_name("h3").text
        print(header_text)
        self.assertEqual("Log in", header_text)
        #assert "ApartFinder is a website to help renters find tenants easily!" in driver.page_source

    #use should be able to view user Lists (Test)
    def test_user_lists(self):
        driver = self.driver
        # My ip address
        driver.get("http://192.168.99.100:8000")
        username = "tk9at"
        password = "wldnro"
        driver.find_element_by_id("id_username").send_keys(username)
        driver.find_element_by_id("id_password").send_keys(password)
        driver.find_element_by_id("login").click()
        driver.implicitly_wait(20)
        driver.find_element_by_id("top").click()
        driver.implicitly_wait(20)
        topheader_text = driver.find_element_by_tag_name("h3").text
        print(topheader_text)
        self.assertEqual("Apartment List", topheader_text)
        driver.find_element_by_id("price").click()
        driver.implicitly_wait(20)
        priceheader_text = driver.find_element_by_tag_name("h3").text
        print(priceheader_text)
        self.assertEqual("Apartment List", priceheader_text)
        driver.find_element_by_id("all").click()
        driver.implicitly_wait(20)
        allheader_text = driver.find_element_by_tag_name("h3").text
        print(allheader_text)
        self.assertEqual("Apartment List", allheader_text)

    #User should be able to view all apartments (Test)
    def test_all_apartments(self):
        driver = self.driver
        # My ip address
        driver.get("http://192.168.99.100:8000")
        username = "tk9at"
        password = "wldnro"
        driver.find_element_by_id("id_username").send_keys(username)
        driver.find_element_by_id("id_password").send_keys(password)
        driver.find_element_by_id("login").click()
        driver.implicitly_wait(20)
        driver.find_element_by_id("all").click()
        driver.implicitly_wait(20)
        assert ("Apartment 8") in driver.page_source

    #User should be able to create apartment (Test)
    def test_create_apartments(self):
        driver = self.driver
        # My ip address
        driver.get("http://192.168.99.100:8000")
        username = "tk9at"
        password = "wldnro"
        driver.find_element_by_id("id_username").send_keys(username)
        driver.find_element_by_id("id_password").send_keys(password)
        driver.find_element_by_id("login").click()
        driver.implicitly_wait(20)
        driver.find_element_by_id("create").click()
        driver.implicitly_wait(20)
        driver.find_element_by_id("id_name").send_keys("testapt")
        driver.find_element_by_id("id_price").send_keys(1228)
        driver.find_element_by_id("createbutton").click()
        driver.implicitly_wait(20)

        assert ("testapt") in driver.page_source

    #User should be able to search apartment (Test)
    def test_search_apartments(self):
        driver = self.driver
        # My ip address
        driver.get("http://192.168.99.100:8000")
        username = "tk9at"
        password = "wldnro"
        driver.find_element_by_id("id_username").send_keys(username)
        driver.find_element_by_id("id_password").send_keys(password)
        driver.find_element_by_id("login").click()
        driver.implicitly_wait(20)
        driver.find_element_by_id("search").click()
        driver.implicitly_wait(20)
        driver.find_element_by_id("id_query").send_keys("Apartment")
        driver.find_element_by_id("searchbutton").click()
        driver.implicitly_wait(20)
        assert ("Apartment 1") in driver.page_source

    #User should be able to delete apartment (Test)
    def test_delete_apartment(self):
        driver = self.driver
        # My ip address
        driver.get("http://192.168.99.100:8000")
        username = "tk9at"
        password = "wldnro"
        driver.find_element_by_id("id_username").send_keys(username)
        driver.find_element_by_id("id_password").send_keys(password)
        driver.find_element_by_id("login").click()
        driver.implicitly_wait(20)
        driver.find_element_by_id("profile").click()
        driver.implicitly_wait(20)
        driver.find_element_by_id("delete5").click()
        driver.implicitly_wait(20)
        assert ("Apartment 5") not in driver.page_source

    #User should be able to view their profile (Test)
    def test_user_profile(self):
        driver = self.driver
        # My ip address
        driver.get("http://192.168.99.100:8000")
        username = "tk9at"
        password = "wldnro"
        driver.find_element_by_id("id_username").send_keys(username)
        driver.find_element_by_id("id_password").send_keys(password)
        driver.find_element_by_id("login").click()
        driver.implicitly_wait(20)
        driver.find_element_by_id("profile").click()
        driver.implicitly_wait(20)
        header_text = driver.find_element_by_tag_name("h4").text
        print(header_text)
        self.assertEqual("Your Apartments", header_text)


    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    print("Selenium main ran.")
    # time.sleep(15)
    # unittest.main()