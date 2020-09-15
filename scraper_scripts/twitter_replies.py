import time
import logging
import config
import tweepy


t = config.python_twitter_api
api = config.api

'''
Get The Entire Twitter thread of replies and conversation to a particular tweet
'''
def get_cascade(tweet_id,username):
    username = "@" + username

    replies = tweepy.Cursor(api.search, q='to:{}'.format(username),
                            since_id=tweet_id, tweet_mode='extended').items()
    while True:
        try:
            reply = replies.next()
            print(reply)
            if not hasattr(reply, 'in_reply_to_status_id_str'):
                continue
            if reply.in_reply_to_status_id == tweet_id:
                logging.info("reply of tweet:{}".format(reply.full_text))

                print(reply)

        except tweepy.RateLimitError as e:
            logging.error("Twitter api rate limit reached".format(e))
            time.sleep(60)
            continue

        except tweepy.TweepError as e:
            logging.error("Tweepy error occured:{}".format(e))
            break

        except StopIteration:
            break

        except Exception as e:
            logging.error("Failed while fetching replies {}".format(e))
            break





