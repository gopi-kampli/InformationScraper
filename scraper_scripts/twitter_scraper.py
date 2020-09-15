import config
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json
import time

"""
Script to scrape tweets based on  article claims
"""
# loading twitter api
api = config.python_twitter_api

# Cleaning stop words using nltk
stop_words = set(stopwords.words('english'))

collection = 'twitterUsers'

logf = open("twitter_scraper_error.log", "w")


def _analyze_tweet(tweet, claim, claim_url):
    is_reply = False

    reply_to_status_id = None
    reply_to_user_id = None

    for t in tweet['statuses']:
        user = t['user']
        user_id = user['id']
        tweet_id = t['id']
        # text = t['text']

        if t['in_reply_to_status_id'] is not None:
            is_reply = True
            reply_to_status_id = t['in_reply_to_status_id']
            reply_to_user_id = t['in_reply_to_user_id']

        try:
            extended_text = t['full_text']
        except AttributeError as e:
            logf.write("Failed to download {0}: {1}\n".format(str(user), str(e)))
            extended_text = t['retweeted_status']['full_text']

        user_information = {
            'user': user_id,
            'tweet_id': tweet_id,
            'text': extended_text,
            'claim': claim,
            'is_reply': is_reply,
            'tweet': t,
            'extended_text': extended_text,
            'url': claim_url,
            'reply_to_status_id':reply_to_status_id,
            'reply_to_user_id':reply_to_user_id
        }

        return user_information


# process to get tweets from claim sentences
def get_tweet_data(claim_sentences, claim_url):
    # word pre-processing
    word_tokens = word_tokenize(claim_sentences)

    words = [word.lower() for word in word_tokens if word.isalpha()]

    filtered_sentence = [w for w in words if not w in stop_words]

    # To remove long sentences that are hard to query using twitter advanced search
    if len(filtered_sentence) > 20:
        return

    # combine filtered sentence to form a query statement
    query_sentence = "%20".join(filtered_sentence)

    try_counter = 0

    try:
        search_result = api.GetSearch(raw_query="q=" + str(query_sentence), return_json=True)

        # json_str = json.dumps(search_result)

        if (search_result['statuses'] != []):
            user_information = _analyze_tweet(search_result, claim_sentences, claim_url)
            return user_information

    except Exception as e:

        logf.write("Failed to download {0}: {1}\n".format(str(filtered_sentence), str(e)))
        return {}
