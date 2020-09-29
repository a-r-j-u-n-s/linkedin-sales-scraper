from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import csv
import re
from bs4 import BeautifulSoup
from utils import NonEmployeeException, Employee, EmailError
from selenium.webdriver.chrome.options import Options

__all__ = ["LinkedinScraper"]


class LinkedinScraper:
    """
    Data mining/web scraping bot to generate relevant leads/accounts from LinkedIn
    """

    def __init__(
            self,
            username: str,
            password: str,
            company_name: str,
            count: int,
            to_ignore: list,
            guess_email=False,
            headless=False,
            link_scrape=True,
            user_agent=False
    ):
        """
        Initializes Scraper
        :param company_name: company in which to search
        :param count: max number of accounts to scrape within company
        :param to_ignore: words to ignore in job titles
        :param guess_email: if True, include email guesses for accounts
        :param headless: if True, will run a headless instance of Chrome
        :param link_scrape: if True, will manually scrape list of profile links from 'links.txt'
        """
        self.company_name = company_name
        self.count = count
        self.to_ignore = [word.lower() for word in to_ignore]
        self.link_scrape = link_scrape
        self.user_agent = user_agent
        self._results = pd.DataFrame(
            columns=["First Name", "Last Name", "Title", "Company", "Location", "Email"]
        )  # .csv file for results

        self._outfile = open("accounts_scrape.csv", "w", newline="")
        self._csv_writer = csv.writer(self._outfile)  # .csv writer to generate accounts
        self._scraped = set()  # List of saved account urls
        self.username = username
        self.password = password

        options = Options()
        if user_agent: # Sets user agent to user agent defined in config
            config = open("config.txt")
            lines = config.readlines()
            user_agent = lines[0].split()[1]
            options.add_argument(
                'user-agent=' + user_agent)  # NOTE: New user agent does not work with Google Search Results
            config.close()

        # Headless option NOTE: Will not work with Rocketreach!
        if headless:
            options.add_argument("--headless")
        self._browser = webdriver.Chrome(
            ChromeDriverManager().install(), options=options
        )  # Set up browser (installs chromedriver)

        # If guess_email, finds email format
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
        self._browser.get("https://www.linkedin.com/uas/login")

        # Submits username and password keys
        element_id = self._browser.find_element_by_id(
            "username"
        )  # Using username input id
        element_id.send_keys(self.username)
        element_id = self._browser.find_element_by_id(
            "password"
        )  # Using password input id
        element_id.send_keys(self.password)

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
        time.sleep(3)
        search = self._browser.find_element_by_xpath(
            "//input[@aria-label='Search']"
        )  # Find elem w search bar xpath
        search.send_keys(self.company_name)
        self._browser.find_element_by_css_selector(
            "button[class='search-global-typeahead__button']"
        ).click()  # Using search BUTTON (not bar itself) class name

        # Manual link scraping option
        if self.link_scrape:
            with open("links.txt") as link_file:
                for link in link_file.readlines():
                    if link not in self._scraped and link:
                        self.scrape_profile(link)
        else:
            while len(self._results) < self.count:
                link = "https://www.linkedin.com/in/maya-weber-9757a4152/"
                if link not in self._scraped:
                    self.scrape_profile(link)

    def scrape_profile(self, link: str):
        """
        Scrapes individual profile and adds information to results file
        :param link: profile link
        """
        self._browser.get(link)
        self._scraped.add(link)

        height = self._browser.execute_script(
            "return document.documentElement.scrollHeight"
        )  # Maybe use body?

        self._browser.execute_script(
            "window.scrollTo(0, document.documentElement.scrollHeight);"
        )  # Scrolls to bottom of page

        # Parse with BeautifulSoup and lxml
        src = self._browser.page_source
        soup = BeautifulSoup(src, "lxml")

        # Get personal info

        full_info_div = soup.find(name="div", attrs={"class": "display-flex mt2"})
        personal_info_div = soup.find(name="div", attrs={"class": "flex-1 mr5"})
        info_loc = personal_info_div.find_all(name="ul")
        names = info_loc[0].find("li").text.strip().split()  # First and last name
        job_info = (
            personal_info_div.find("h2").text.strip().split(" at ")
        )  # Job title and company
        location = info_loc[1].find_next("li").text.strip()
        job_title = job_info[0].split()

        # Get company name
        company_ul = full_info_div.find("ul", {"class": "pv-top-card--experience-list"})
        company_name = company_ul.find(
            "span",
            {
                "class": "text-align-left ml2 t-14 t-black t-bold full-width lt-line-clamp lt-line-clamp--multi-line ember-view"
            },
        ).text.strip()

        # NOTE: Company name stored in two places: job_info[1] and company_name

        # Create new employee
        employee = Employee(
            first_name=names[0],
            last_name=names[len(names) - 1],
            job_title=job_info[0],
            company=company_name,
            location=location,
        )

        # If email format exists
        employee_email = "Did not guess email"
        if self._email_format is not None:
            employee_email = self._generate_email(employee)

        # Create and append new data to .csv
        job_title_lower = [word.lower() for word in job_title]
        good_title = all(keyword not in job_title_lower for keyword in self.to_ignore)

        if good_title:
            account_info = pd.DataFrame(
                data=[
                    [
                        employee.first_name,
                        employee.last_name,
                        employee.job_title,
                        employee.company,
                        employee.location,
                        employee_email,
                    ]
                ],
                columns=self._results.columns,
            )  # FIX THIS
            self._results = self._results.append(account_info, True)

        # Save profile information to .csv file
        self._results.to_csv("results/accounts_scrape.csv")

    def guess_email_format(self):
        """
        Guesses the email format of the given company based on Rocketreach results
        :return: email format str
        """
        self._browser.get("https://www.google.com/")

        # Search for Rocketreach results on Google
        search_input = self._browser.find_element_by_name("q")
        search_input.send_keys(
            "site:rocketreach.co/ AND " + self.company_name + " AND email format"
        )
        search_input.send_keys(Keys.RETURN)

        # Go to first result
        search_results = self._browser.find_element_by_xpath('//*[@class="r"]/a[1]')
        link = search_results.get_attribute("href")
        self._browser.get(link)

        # Find email format w highest percentage
        time.sleep(6)
        src = self._browser.page_source
        soup = BeautifulSoup(src, "lxml")

        try:
            info_div = soup.find("table", {"class": "table table-bordered"})
            formats = info_div.find_all("tr")
            format_str = formats[1].find_all("td")[0].text.strip()  # Name format
            company_email = formats[1].find_all("td")[1].text.strip()  # Email format
            percentage = formats[1].find_all("td")[2].text.strip()
            self._results = self._results.rename(
                columns={"Email": "Email (accuracy: " + percentage + ")"}
            )

            # Interpret email format
            return self._interpret_format(format_str, company_email)
        except Exception:
            print("Could not guess company email")
            raise EmailError

    def _generate_email(self, employee: Employee):
        """
        Generates email for an individual employee
        :param employee: Employee
        :return: email str
        """
        split_format = self._email_format.split()
        email_format = ""
        regex = re.compile("[^A-Za-z0-9]")
        for term in split_format:
            if term in employee.email_formatting.keys():
                email_format += employee.email_formatting[term]
            elif term.startswith("@"):
                email_format += term
            else:
                if not regex.match(term[0]):
                    email_format += term[1]
        return email_format

    @staticmethod
    def _interpret_format(format_str: str, company_email: str):
        """
        Interprets given email format
        :param format_str: str of email format
        :param company_email: email address of company
        :return: email format
        """
        # format should be 'first_inital last' for example
        company = company_email.find("@")
        company_email = company_email[company: len(company_email)]
        email_format = format_str + " " + company_email
        return email_format

    @staticmethod
    def account_updater(my_accounts: pd.DataFrame, database_accounts: pd.DataFrame):
        """
        For use with SalesForce or any other database platform
        Updates scraped DataFrame by removing rows that already exist in large database
        :param my_accounts: DataFrame of scraped accounts
        :param database_accounts: DataFrame of database accounts
        :return: Downloads updated .csv to project directory
        """
        accounts = my_accounts[["First Name", "Last Name", "Company"]]
        database = database_accounts[["First Name", "Last Name", "Company"]]

        merged = (
            accounts.merge(database, how="left", indicator=True)
                .query('_merge == "both"')
                .drop(["_merge"], axis=1)
        )
        with pd.option_context(
                "display.max_rows", None, "display.max_columns", None
        ):  # more options can be specified also
            print(merged)
            print(len(merged))
        indices = merged.index
        my_accounts = my_accounts.drop(index=indices)
        print(my_accounts)

        my_accounts.to_csv("results/accounts_updated.csv")
