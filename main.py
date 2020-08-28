from LinkedinScraper import LinkedinScraper

import pandas as pd


def main():
    scraper = LinkedinScraper('Lockheed Martin', 1, ['intern'], [], guess_email=True)
    scraper.run()

    # REDUNTANT: SCRAPE RESULTS SALESFORCE SCRIPT
    # salesforce_accounts = pd.read_csv('testing/salesforce_accounts.csv')
    # my_accounts = pd.read_csv('testing/accounts_masterlist_to_edit.csv')
    # my_accounts['Record Owner'] = 'Personetics Marketing'
    # my_accounts['Original UTM'] = 'Outbound'
    # print(my_accounts, '=' * 100, sep='\n')
    #
    # accounts = my_accounts[['First Name', 'Last Name', 'Company']]
    # salesforce = salesforce_accounts[['First Name', 'Last Name', 'Company']]
    #
    # merged = accounts.merge(salesforce, how='left', indicator=True).query('_merge == "both"').drop(['_merge'], axis=1)
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    #     print(merged)
    #     print(len(merged))
    # indices = merged.index
    # my_accounts = my_accounts.drop(index=indices)
    # print(my_accounts)
    #
    # my_accounts.to_csv('testing/accounts.csv')


if __name__ == '__main__':
    main()
