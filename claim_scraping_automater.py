from scraper_scripts import snopes_scraper as ss
from scraper_scripts import poltifact_scraper as ps
import pandas as pd

"""Main File, automated to run on linux server every hour with CRON Job
checks for politfact and snopes fact check links every hour
stores new found data, and finds related tweets to new claims"""


'''Scrape Method using scraper classes and save to csv and database'''
def scrape_and_save_politifact():
    #politifact_scraper
    politifact = ps.Politifact_Scraper()

    politifact_links = politifact.get_factcheck_data()


    #get old scraped links from csv
    try:
        previous_politifact_df = pd.read_csv('csv/old_politifact_data.csv',encoding="utf-8")
        previous_politifact_set = {tuple(previous_politifact_df['politifact_link'].values.tolist())}
    except:
        previous_politifact_df = pd.DataFrame()
        previous_politifact_set = set(previous_politifact_df.values.tolist())


    #current scrapped links from politifact class
    current_politifact_df = pd.DataFrame(politifact_links,columns=politifact.get_column_names())
    current_politifact_set = {tuple(current_politifact_df['politifact_link'].values.tolist())}

    #finding only the new links and saving them to csv
    new_politifact_set = list(current_politifact_set.difference(previous_politifact_set))

    if (len(new_politifact_set)>0):
        new_politifact_df = current_politifact_df.loc[current_politifact_df['politifact_link'].isin(new_politifact_set[0])]
        new_politifact_df.to_csv('csv/collected_politifact_data.csv', mode='a', index=False, header=False,
                                 encoding="utf-8")


    #updating the old scrapped links for the next iteration
    current_politifact_df.to_csv('csv/old_politifact_data.csv', index=False, encoding="utf-8")




def scrape_and_save_snopes():
    # politifact_scraper
    snopes = ss.Snopes_Scraper()

    snopes_links = snopes.get_snopes_claims()

    # get old scraped links from csv
    try:
        previous_snopes_df = pd.read_csv('csv/old_snopes_data.csv', index_col=0)
    except:
        previous_snopes_df = pd.DataFrame()

    previous_snopes_set = set([tuple(values) for values in previous_snopes_df.values.tolist()])

    # current scrapped links from snopes class
    current_snopes_df = pd.DataFrame(snopes_links, columns=snopes.get_column_names())
    current_snopes_set = set([tuple(values) for values in current_snopes_df.values.tolist()])

    # finding only the new links and saving them to csv
    new_snopes_set = current_snopes_set.difference(previous_snopes_set)
    new_snopes_df = pd.DataFrame(new_snopes_set, columns=snopes.get_column_names())
    new_snopes_df.to_csv('csv/collected_snopes_data.csv', mode='a', index=True, header=False)

    #saving the current links as old for next iteration
    current_snopes_df.to_csv('csv/old_snopes_data.csv', index=True)


"""Run the script on cron job for every hour"""

if __name__ == '__main__':
    scrape_and_save_politifact()
    scrape_and_save_snopes()