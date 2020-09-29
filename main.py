from LinkedinScraper import LinkedinScraper


def main():
    username = "My LinkedIn Username"
    password = "My LinkedIn Password"
    company = "Desired Company"
    to_ignore = []

    scraper = LinkedinScraper(
        username=username,
        password=password,
        company_name=company,
        count=100,
        to_ignore=to_ignore,
        guess_email=True,
        headless=False,
        link_scrape=True,
        user_agent=False,
    )
    scraper.run()


if __name__ == "__main__":
    main()
