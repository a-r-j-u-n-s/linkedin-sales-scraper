# Linkedin Sales Scraper
**LinkedinScraper** is a sales web scraping bot that generates relevant leads/accounts for companies of your choice based on data from [LinkedIn](https://www.linkedin.com/feed/) and saves the results to a .csv file. This bot can also guess the email addresses of leads based on data from [Rocketreach](https://rocketreach.co/)


## Dependencies
*Requires Python 3.7 or later*

[Selenium](https://pypi.org/project/selenium/), 
[BeautifulSoup](https://pypi.org/project/beautifulsoup4/),
[Pandas](https://pandas.pydata.org/)
[ChromeDriver](https://chromedriver.chromium.org/)

## Features and Options

`link_scrape`: *Scraping a list of LinkedIn Profiles*

- Default `True`
- Utilizes link scraping mode
- Open links.txt and paste desired profile links
- Run; results saved to accounts_scrape.csv

`guess_email`: *Using Rocketreach to guess leads' company emails*

- Set this option to `True` to enable email guessing
- Bot will access [Rocketreach](rocketreach.co) to generate an email guess (with a displayed accuracy) for all scrape reesults
- Results will be included in accounts_scrape.csv

`to_ignore`:

- Add keywords of job titles you would like the scraper to ignore
- E.g. `to_ignore` = ['intern', 'software', 'operations'] -> ignores profiles with given job title keywords

`headless`:

- Runs browser in "headless" mode
- Browser will run as a background process
- Note: Will not work with guess_email!

`user_agent`:

- Checks `config.txt` for alternate user agent and uses it for web driving
- Note: Only necessary for large scrapes of over 100 profiles


## Usage

Clone this repository and set your credentials and information in [main.py](main.py)

## Author

* **Arjun Srivastava** - [LinkedIn](https://www.linkedin.com/in/arjun-srivastava042701/)




