from LinkedinScraper import LinkedinScraper
import pandas as pd


def account_updater():
    salesforce_accounts = pd.read_csv('testing/all_contacts.csv')
    my_accounts = pd.read_csv('testing/new_accounts.csv')
    print(my_accounts, '=' * 100, sep='\n')

    accounts = my_accounts[['First Name', 'Last Name', 'Company']]
    salesforce = salesforce_accounts[['First Name', 'Last Name', 'Company']]

    merged = accounts.merge(salesforce, how='left', indicator=True).query('_merge == "both"').drop(['_merge'], axis=1)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(merged)
        print(len(merged))
    indices = merged.index
    my_accounts = my_accounts.drop(index=indices)
    print(my_accounts)

    my_accounts.to_csv('testing/accounts_updated.csv')


def main():
    scraper = LinkedinScraper('Zions First National Bank', 10, ['intern'], [], guess_email=True, link_scrape=True)
    scraper.run()


if __name__ == '__main__':
    main()
