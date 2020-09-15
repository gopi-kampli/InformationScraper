import pandas as pd
from scraper_scripts import twitter_scraper as ts
from scraper_scripts import poltifact_scraper as ps
from scraper_scripts import snopes_scraper as ss

"""Twitter Scraping automator, to be run on CRON job every 5 hours"""

if __name__ == '__main__':

    #Load collected claims from csv
    politifact_df = pd.read_csv('csv/collected_politifact_data.csv',encoding="utf-8")
    #Loading columns names when no header
    politifact_df.columns = ps.Politifact_Scraper().get_column_names()
    #Loading only the latest 200 claims, for recent data
    politifact_df = politifact_df.tail(200)

    #Requied columns for tweet extraction
    politifact_list = politifact_df[['media_rating','claim_text','politifact_link']].values.tolist()

    #Scraping tweets and saving to database
    for p in politifact_list:
        data = ts.get_tweet_data(p[1],p[2])
        data['media_rating']= p[0]
        data['Scraper'] = 'Politifact'
        #TODO: insert into a specified database or csv file


    #Repeating same process for snopes
    snopes_df = pd.read_csv("csv/collected_snopes_data.csv",encoding="utf-8")
    snopes_df.columns = ss.Snopes_Scraper().get_column_names()
    snopes_df = snopes_df.tail(200)

    snopes_list = snopes_df[['media_rating', 'claim_text', 'politifact_link']].values.tolist()

    #Scraping tweets and saving to database
    for s in snopes_list:
        data = ts.get_tweet_data(s[1],s[2])
        data['media_rating'] = s[0]
        data['Scraper'] = 'Snopes'
        # TODO: insert into a specified database or csv file

