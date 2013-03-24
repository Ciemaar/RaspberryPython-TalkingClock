#Copyright 2013 Andy Fundinger
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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

