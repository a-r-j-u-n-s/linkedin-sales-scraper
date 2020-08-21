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
        username = lines[3].split(':')[1]
        password = lines[4].split(':')[1]
        config.close()

        # Submits username and password keys
        element_id = self.browser.find_element_by_id('username')  # Using username input id
        element_id.send_keys(username)
        element_id = self.browser.find_element_by_id('password')  # Using password input id
        element_id.send_keys(password)

        # element_id.submit()  CAUSING STALE ELEMENT ERROR

        # Search and access 'People' tab for given company
        self.search()

        self.browser.quit()  # Close Chrome browser

    def search(self):
        # Initial search
        search = self.browser.find_element_by_xpath("//input[@aria-label='Search']")  # Using search bar xpath
        search.send_keys(self.company_name)
        self.browser.find_element_by_css_selector(
            "button[class='search-global-typeahead__button']").click()  # Using search BUTTON (not bar itself) class name
        time.sleep(5)
        result = self.browser.find_element_by_class_name('search-result__result-link ember-view')  # Finds first search result (MAKE MORE EFFECTIVE)
        link = result.get_attribute('href')
        self.browser.get(link)
