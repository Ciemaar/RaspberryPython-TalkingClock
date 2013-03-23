from datetime import datetime
from time import sleep
import re
import random
import pickle
from ConfigParser import SafeConfigParser

from espeak import espeak
import twitter


config = SafeConfigParser()
config.read(["clock.cfg"])

api = twitter.Api(consumer_key=config.get("twitter", "consumer_key"),
                  consumer_secret=config.get("twitter", "consumer_secret"),
                  access_token_key=config.get("twitter", "access_token_key"),
                  access_token_secret=config.get("twitter", "access_token_secret"))
statuses = api.GetFriendsTimeline(retweets=True)

pickle.dump(statuses, open("statuses.pkl", "wb"), pickle.HIGHEST_PROTOCOL)

espeak.synth("The time is now " + datetime.now().time().strftime("%I:%M"))
sleep(5)


#config.set('session-cache', 'key', client.key)
#save_current_config()


def tweet_status(status_to_tweet):
    text = status_to_tweet.text
    text = re.sub(r"@(\w+)", r"at \1", text)
    text = re.sub(r"#(\w+)", r"hashtag \1", text)
    text = re.sub(r"(http[^ ]+)", r"Link", text)
    text = re.sub(r"RT\W", r"", text)
    try:
        twitterSpeak = "{friend} says {text}".format(friend=status_to_tweet.user.name, text=text)
    except UnicodeEncodeError:
        print u"Unable to speak this status {friend} says {text}".format(friend=status_to_tweet.user.name, text=text)
        return
    print twitterSpeak
    espeak.synth(twitterSpeak)
    sleep(30)


tweet_status(random.choice(statuses))
