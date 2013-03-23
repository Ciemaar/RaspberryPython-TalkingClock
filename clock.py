from ConfigParser import SafeConfigParser
from datetime import datetime
from time import sleep
import random

from espeak import espeak
import twitter

# api = twitter.Api(consumer_key='xx',
#                              consumer_secret='xx',
#                              access_token_key='xx',
#                              access_token_secret='xx')

config = SafeConfigParser()
config.read(["clock.cfg"])

api = twitter.Api(consumer_key=config.get("twitter", "consumer_key"),
                  consumer_secret=config.get("twitter", "consumer_secret"),
                  access_token_key=config.get("twitter", "access_token_key"),
                  access_token_secret=config.get("twitter", "access_token_secret"))
statuses = api.GetFriendsTimeline(retweets=True)

espeak.synth("The time is now " + datetime.now().time().strftime("%I:%M"))
sleep(5)

status_to_tweet = random.choice(statuses)
text = status_to_tweet.text

#note occasionally unicode errors will end program at this point
twitterSpeak = "{friend} says {text}".format(friend=status_to_tweet.user.name, text=text)

print twitterSpeak
espeak.synth(twitterSpeak)
sleep(30)

