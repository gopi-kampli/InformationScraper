from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.common.exceptions import TimeoutException
from urllib.request import Request, urlopen

"""
Web Scraper for snopes.com to track for fact check
"""


class Snopes_Scraper():
    '''
       Snopes.com claims scraping
    '''

    driver = None

    def __init__(self):
        # selenium driver to access sites rendered with javascript
        # self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver = None

    # extract search term articles from snopes
    def _extract_article_links(self):

        # snopes link for fact check
        snopes_fact_check_url = 'https://www.snopes.com/fact-check/'

        req = Request(snopes_fact_check_url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        bs = BeautifulSoup(webpage, 'html.parser')

        urls = []
        url_text = []
        bs_links = bs.find_all("div", {"class": "media-list"})

        for div in bs_links:
            links = div.findAll('a')
            for a in links:
                url_text.append(a.text)
                urls.append(a['href'])

        return urls

    def _extract_article_information(self, url):
        # terms initialization
        title_text = "Not Found"
        subtitle_text = "Not Found"
        snopes_author_text = "Not Found"
        claim_text = "Not Found"
        media_rating = "Not Found"

        # original sources
        source_type = "source not found"
        tweet_links = []
        article_links = []
        tweet_source = "Not Found"
        origin_source = "Not Found"

        # beautiful soup html extraction
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        bs = BeautifulSoup(webpage, 'html.parser')

        # get title of snopes article
        try:
            title_attribute = bs.find(class_="title")
            title_text = title_attribute.text
        except AttributeError as e:
            print("title" + str(e))

        # get subtext of snopes article
        try:
            subtitle_attribute = bs.find(class_="subtitle")
            subtitle_text = subtitle_attribute.text
        except AttributeError as e:
            print("subtitle " + str(e))

        # snopes_author
        try:
            snopes_author_attribute = bs.find(class_="author")
            snopes_author_text = snopes_author_attribute.text
        except AttributeError as e:
            print("author " + str(e))

        # claim
        try:
            claim_attribute = bs.find(class_="claim")
            # claim_attribute = claim_attribute.findAll('p')
            claim_text = claim_attribute.text
        except AttributeError as e:
            print("claim " + str(e))

        # rating
        try:
            if bs.find(class_="rating-label-false") != None:
                media_rating = "False"
            elif bs.find(class_="rating-label-true") != None:
                media_rating = "True"
            elif bs.find(class_="rating-label-mixture") != None:
                media_rating = "Mixture"
            elif bs.find(class_="rating-label-mostly-false") != None:
                media_rating = "Mostly False"
            elif bs.find(class_="rating-label-mostly-true") != None:
                media_rating = "Mostly True"
            else:
                media_rating = "Not Found/Other Category"
        except AttributeError as e:
            print("rating " + str(e))

        try:
            content_attribute = bs.find(class_="content")

            tweet_attribute = bs.find(class_="twitter-tweet")
            tweet_links_all = tweet_attribute.findAll('a')

            article_links = content_attribute.findAll('a')

            for t in tweet_links_all:
                tweet_links.append(t['href'])
                if 'status' in str(t['href']).lower():
                    tweet_source = t['href']

            for s in article_links:
                print(s.text)
                if 'origin' in str(s.text).lower():
                    origin_source = s['href']

        except AttributeError as e:
            print("Source Attribute  " + str(e))

        snopes_array = [title_text, subtitle_text, snopes_author_text, claim_text, media_rating]
        original_article_array = [tweet_links, tweet_source, article_links, origin_source]

        return snopes_array, original_article_array

    def get_snopes_claims(self):

        results = []
        search_terms_news_contents = []

        try:
            news_contents = self._extract_article_links()
            search_terms_news_contents.append([news_contents])

        except TimeoutError:
            time.sleep(300)
            news_contents = self._extract_article_links()
            search_terms_news_contents.append([news_contents])

        exception_counter = 0
        counter = 1

        for content in search_terms_news_contents:

            news = content[0]
            for url in news:
                try:
                    snopes_array, original_article_array = self._extract_article_information(url)
                    result = []
                    result.extend(snopes_array)
                    result.extend([original_article_array[1], original_article_array[3]])
                    result.extend([url])
                    results.append(result)
                    counter += 1

                    if (counter % 250 == 0):
                        time.sleep(30)

                except TimeoutException as ex:
                    time.sleep(300)
                    continue

                except:
                    if exception_counter > 5:
                        exception_counter += 1
                        time.sleep(1000)
                        continue
                    else:
                        break

        return results

    def get_column_names(self):

        column_names = ['title_text', 'subtitle_text', 'snopes_author', 'claim_text', 'media_rating',
                        'tweet_source', 'origin_source', 'snopes_link']
        return column_names
