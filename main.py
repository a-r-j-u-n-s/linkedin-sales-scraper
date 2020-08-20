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
    element_id = browser.find_element_by_id('username')
    element_id.send_keys(username)
    element_id = browser.find_element_by_id('password')
    element_id.send_keys(password)
    element_id.submit()

    # Initial search NOT WORKING RIGHT NOW
    search = browser.find_element_by_xpath("//input[@aria-label='Search']")  # Using xpath of LinkedIn search bar
    search.click()
    search.send_keys('apple')
    search.submit()
    time.sleep(5)


if __name__ == '__main__':
    main()