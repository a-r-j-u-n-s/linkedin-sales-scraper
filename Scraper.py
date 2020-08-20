from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests, time, random
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
# TODO: IMPLEMENT SALES NAV

class Scraper:
    def __init__(self, company_name: str, results: int, keywords: list, to_ignore: list):
        self.company_name = company_name
        self.results = results
        self.keywords = keywords
        self.to_ignore = to_ignore

        # Setting up browser
        self.browser = webdriver.Chrome(ChromeDriverManager().install())

    def run(self):
        # Get login page
        self.browser.get('https://www.linkedin.com/uas/login')

        # Retrieves username and password from config.txt
        config = open('config.txt')
        lines = config.readlines()
        username = lines[1].split(':')[1]
        password = lines[2].split(':')[1]
        config.close()

        # Submits username and password keys
        element = self.browser.find_element_by_id('username')  # Using username input id
        element.send_keys(username)
        element = self.browser.find_element_by_id('password')  # Using password input id
        element.send_keys(password)

        element.submit()

        self.search()

        self.browser.quit()  # Close Chrome browser

    def search(self):
        # Initial search
        search = self.browser.find_element_by_xpath("//input[@aria-label='Search']")  # Using search bar xpath
        search.send_keys(self.company_name)
        self.browser.find_element_by_css_selector(
            "button[class='search-global-typeahead__button']").click()  # Using search BUTTON (not bar itself) class name
        time.sleep(5)
        result = self.browser.find_element_by_id('ember9183')  # Finds first search result (MAKE MORE EFFECTIVE)
        link = result.get_attribute('href')
        self.browser.get(link)
