from Scraper import Scraper


def main():
    scraper = Scraper('google', 10, [], [])
    scraper.run()


if __name__ == '__main__':
    main()
