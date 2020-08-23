from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import pandas as pd
import requests, time, lxml, csv
from bs4 import BeautifulSoup

__all__ = ['LinkedinScraper']


# TODO: IMPLEMENT SALES NAV, fix middle name

class LinkedinScraper:
    """
    Sales web scraping bot to generate relevant leads/accounts from LinkedIn
    """
    def __init__(self, company_name: str, count: int, keywords: list, to_ignore: list, guess_email=False):
        """
        Initializes Scraper
        :param company_name: Company in which to search
        :param count: max number of accounts to scrape within company
        :param keywords: key words relevant to job titles
        :param to_ignore: words to ignore in job titles
        """
        self.company_name = company_name
        self.count = count
        self.keywords = keywords
        self.to_ignore = to_ignore
        self._results = pd.DataFrame(
            columns=['First Name', 'Last Name', 'Title', 'Company', 'Location'])  # .csv file for results

        self._outfile = open("accounts_scrape.csv", "w", newline='')
        self._csv_writer = csv.writer(self._outfile)
        self._browser = webdriver.Chrome(ChromeDriverManager().install())  # Set up browser

        # If guess_email, find email format
        if guess_email:
            self._email_format = self.guess_email_format()
        else:
            self._email_format = None

    def run(self):
        """
        Runs Scraper with Chromedriver
        :return:
        """
        # Get login page
        self._browser.get('https://www.linkedin.com/uas/login')

        # Retrieves username and password from config.txt
        config = open('config.txt')
        lines = config.readlines()
        username = lines[1].split(':')[1]
        password = lines[2].split(':')[1]
        config.close()

        # Submits username and password keys
        element_id = self._browser.find_element_by_id('username')  # Using username input id
        element_id.send_keys(username)
        element_id = self._browser.find_element_by_id('password')  # Using password input id
        element_id.send_keys(password)

        # element_id.submit()  CAUSES STALE ELEMENT ERROR

        # Search and access 'People' tab for given company
        self.search()

        self._outfile.close()
        self._browser.quit()  # Close Chrome browser

    def search(self):
        """
        Access employees of chosen company
        """
        # Initial search
        search = self._browser.find_element_by_xpath("//input[@aria-label='Search']")  # Find elem w search bar xpath
        search.send_keys(self.company_name)
        self._browser.find_element_by_css_selector(
            "button[class='search-global-typeahead__button']").click()  # Using search BUTTON (not bar itself) class name

        # time.sleep(5)
        # result = self.browser.find_element_by_class_name('search-result__result-link ember-view')  # Finds first search result (MAKE MORE EFFECTIVE)
        # link = result.get_attribute('href')
        # self.browser.get(link)

        # Scrape individual profile
        self.scrape_profile('https://www.linkedin.com/in/ravina-dalamal-mirapuri-6b83a16/')

    def scrape_profile(self, link: str):
        """
        Scrapes profile and adds information to results file
        :param link: profile link
        """
        self._browser.get(link)

        height = self._browser.execute_script("return document.documentElement.scrollHeight")  # Maybe use body?

        self._browser.execute_script(
            "window.scrollTo(0, document.documentElement.scrollHeight);")  # Scrolls to bottom of page

        # Parse with BeautifulSoup and lxml
        src = self._browser.page_source
        soup = BeautifulSoup(src, 'lxml')

        # Get personal info
        personal_info_div = soup.find(name='div', attrs={'class': 'flex-1 mr5'})
        info_loc = personal_info_div.find_all(name='ul')
        names = info_loc[0].find('li').text.strip().split()  # First and last name
        job_info = personal_info_div.find('h2').text.strip().split(' at ')  # Job title and company
        location = info_loc[1].find_next('li').text.strip()  # Location

        # Create and append new data to .csv
        account_info = pd.DataFrame(data=[[names[0], names[1], job_info[0], job_info[1], location]],
                                    columns=self._results.columns)
        self._results = self._results.append(account_info, True)

        # Save profile information to .csv file
        self._results.to_csv('accounts_scrape.csv')

    def guess_email_format(self):
        """
        Guesses the email format of the given company based on Rocketreach results
        :return: email format
        """
        self._browser.get('https://www.google.com/')

        # Search for Rocketreach results on Google
        search_input = self._browser.find_element_by_name('q')
        search_input.send_keys('site:rocketreach.co/ AND ' + self.company_name + ' AND email format')
        search_input.send_keys(Keys.RETURN)

        # Go to first result
        search_results = self._browser.find_element_by_xpath('//*[@class="r"]/a[1]')
        link = search_results.get_attribute('href')
        self._browser.get(link)
        return ''



