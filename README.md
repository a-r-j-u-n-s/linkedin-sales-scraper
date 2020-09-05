# Linkedin Sales Scraper
**LinkedinScraper** is a sales web scraping bot that generates relevant leads/accounts for companies of your choice based on data from [LinkedIn](https://www.linkedin.com/feed/) and saves the results to a .csv file. This bot can also guess the email addresses of leads based on data from [Rocketreach](https://rocketreach.co/)


## Dependencies
*Requires Python 3.7 or later*

[Selenium](https://pypi.org/project/selenium/), 
[BeautifulSoup](https://pypi.org/project/beautifulsoup4/),
[Requests](https://pypi.org/project/requests/) (not currently in use),
[Pandas](https://pandas.pydata.org/)

## Features

`link_scrape`: *Scraping a list of LinkedIn Profiles*

- Set this option to `True` to utilize link scraping mode
- Open links.txt and paste desired profile
- Run; results saved to accounts_scrape.csv

`guess_email`: *Using Rocketreach to guess leads' company emails*

- Set this option to `True` to enable email guessing
- Bot will access [Rocketreac](rocketreach.co) to generate an email guess (with a displayed accuracy) for all scrape reesults

## Usage

Still in testing


## Author

* **Arjun Srivastava** - [LinkedIn](https://www.linkedin.com/in/arjun-srivastava042701/)




