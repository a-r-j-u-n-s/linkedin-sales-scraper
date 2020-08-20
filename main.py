from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests, time, random
from bs4 import BeautifulSoup


def main():

    # FIX PATH
    browser = webdriver.Chrome(ChromeDriverManager().install())

    browser.get('https://www.linkedin.com/uas/login')
    config = open('config.txt')
    lines = config.readlines()
    username = lines[0].split()[1]
    password = lines[1].split()[1]

    element_id = browser.find_element_by_id('username')
    element_id.send_keys(username)

    element_id = browser.find_element_by_id('password')
    element_id.send_keys(password)

    element_id.submit()


if __name__ == '__main__':
    main()