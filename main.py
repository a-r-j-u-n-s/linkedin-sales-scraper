from LinkedinScraper import LinkedinScraper


def main():
    scraper = LinkedinScraper('apple', 10, [], [], guess_email=True)
    scraper.run()


if __name__ == '__main__':
    main()
