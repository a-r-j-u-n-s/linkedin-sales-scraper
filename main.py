from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests, time, random
from bs4 import BeautifulSoup


def main():
    # Setting up browser
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get('https://www.linkedin.com/uas/login')

    # Retrieves username and password from config.txt
    config = open('config.txt')
    lines = config.readlines()
    username = lines[1].split()[1]
    password = lines[2].split()[1]

    # Submits username and password keys
    element_id = browser.find_element_by_id('username')  # Using username input id
    element_id.send_keys(username)
    element_id = browser.find_element_by_id('password')  # Using password input id
    element_id.send_keys(password)
    element_id.submit()

    # Initial search
    search = browser.find_element_by_xpath("//input[@aria-label='Search']")  # Using search bar xpath
    search.send_keys('Gabrielle Sprunck')
    browser.find_element_by_css_selector("button[class='search-global-typeahead__button']").click()  # Using search BUTTON (not bar itself) class name
    time.sleep(10)

    # TODO: implement Scraper class, multi-query, etc.

    # Get info from given link
    link = 'https://www.linkedin.com/in/arjun-srivastava042701/'
    browser.get(link)


if __name__ == '__main__':
    main()
