from LinkedinScraper import LinkedinScraper

import pandas as pd


def main():
    scraper = LinkedinScraper('Amazon', 1, [], [], guess_email=True)
    scraper.run()
    # salesforce_accounts = pd.read_csv('testing/salesforce_accounts.csv')
    # my_accounts = pd.read_csv('testing/accounts_masterlist_to_edit.csv')
    # accounts = my_accounts[['First Name', 'Last Name', 'Company']]
    # salesforce = salesforce_accounts[['First Name', 'Last Name', 'Company']]
    # print(accounts.head())
    # print('=' * 100)
    # print(salesforce.head())


if __name__ == '__main__':
    main()
