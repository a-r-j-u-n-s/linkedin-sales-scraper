from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests, time, random
from bs4 import BeautifulSoup


def main():

    # FIX PATH: todo for chromedriver?
    browser = webdriver.Chrome(ChromeDriverManager().install())

    # Retrieves username and password
    browser.get('https://www.linkedin.com/uas/login')
    config = open('config.txt')
    lines = config.readlines()
    username = lines[1].split()[1]
    password = lines[2].split()[1]

    # Submits username and password keys
    element_id = browser.find_element_by_id('username')
    element_id.send_keys(username)
    element_id = browser.find_element_by_id('password')
    element_id.send_keys(password)
    element_id.submit()

    # Search functionality
    search = browser.find_element_by_xpath("//input[@aria-label='Search']")
    search.send_keys('apple')
    search.submit()


if __name__ == '__main__':
    main()