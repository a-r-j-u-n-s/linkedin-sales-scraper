from LinkedinScraper import LinkedinScraper


def main():
    scraper = LinkedinScraper('Amazon', 1, [], [], guess_email=True, headless=False)
    scraper.run()


if __name__ == '__main__':
    main()
