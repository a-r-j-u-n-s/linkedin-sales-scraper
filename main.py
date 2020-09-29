from LinkedinScraper import LinkedinScraper


def main():
    scraper = LinkedinScraper(
        "Zions First National Bank",
        10,
        ["intern"],
        [],
        guess_email=False,
        link_scrape=True,
    )
    scraper.run()


if __name__ == "__main__":
    main()
