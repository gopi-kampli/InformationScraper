from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

"""
Web Scraper for Politifact.com to track source information for Fact check
"""

'''
Politifact.com claims scraping
'''
class Politifact_Scraper():

    # extract search term articles from snopes
    def _extract_article_links(self, media_rating='false'):
        # snopes link for fact check

        req = Request('https://www.politifact.com/factchecks/list/?ruling=' + media_rating,
                      headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()

        bs = BeautifulSoup(webpage, 'html.parser')

        bs_links = bs.find_all("li", {"class": "o-listicle__item"})

        extracted_contents = []

        for li in bs_links:
            politifact_timestamp = li.find('div', {"class": "m-statement__desc"})
            politifact_timestamp = str(politifact_timestamp.text)
            politifact_timestamp.rstrip('\r\n')

            article_type = li.find('a', {"class": "m-statement__name"})
            article_type = str(article_type.text)
            article_type.rstrip('\r\n')

            claim = li.find('div', {"class": "m-statement__quote"})
            claim = str(claim.text)
            claim.rstrip('\r\n')

            politifact_link = li.find('div', {"class": "m-statement__quote"})
            politifact_link = str(politifact_link.find('a')['href'])
            politifact_link = 'https://www.politifact.com' + politifact_link
            politifact_link.rstrip('\r\n')

            politifact_author = li.find('footer', {"class": "m-statement__footer"})
            politifact_author = str(politifact_author.text)
            politifact_author.rstrip('\r\n')

            extracted_content = [media_rating, claim, article_type, politifact_timestamp, politifact_author,
                                 politifact_link]

            extracted_contents.append(extracted_content)

        return extracted_contents

    # get all truth-o-meter fact check links
    def get_factcheck_data(self):
        true = self._extract_article_links('true')
        false = self._extract_article_links('false')
        mostly_true = self._extract_article_links('mostly-true')
        mostly_false = self._extract_article_links('mostly-false')
        half_true = self._extract_article_links('half-true')
        pants_on_fire = self._extract_article_links('pants-fire')

        result = []
        result.extend(true)
        result.extend(mostly_true)
        result.extend(half_true)
        result.extend(mostly_false)
        result.extend(false)
        result.extend(pants_on_fire)

        return result

    def get_column_names(self):
        column_names = ['media_rating', 'claim_text', 'article_type', 'politifact_timestamp', 'politifact_author',
                        'politifact_link']
        return column_names
