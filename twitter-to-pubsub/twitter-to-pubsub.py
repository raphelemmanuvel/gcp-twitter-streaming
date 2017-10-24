#!/usr/bin/env python
# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This script uses the Twitter Streaming API, via the tweepy library,
to pull in tweets and publish them to a PubSub topic.
"""

import base64
import time
import datetime
import os

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

import helper

#Get twitter application credentials from env
consumer_key = os.environ['CONSUMERKEY']
consumer_secret = os.environ['CONSUMERSECRET']
access_token = os.environ['ACCESSTOKEN']
access_token_secret = os.environ['ACCESSTOKENSEC']

#Get pubsub_topic from env file
PUBSUB_TOPIC = os.environ['PUBSUB_TOPIC']
MAX_RETRIES = 3


#Catch the real-time tweets using StreamListener and then push the tweets to the pubsub topic
class TweetsListener(Stream):

    tweets = []  #To collect the tweets as a batch
    batch_size = 20 #To specify the batch_size so as to push the tweets to pubsub as batch
    pubsub_client = helper.create_pubsub_client(helper.get_credentials)

    def push_to_pubsub(self,data):
        publish(self.pubsub_client, PUBSUB_TOPIC,data)

    # on_data() is a method of StreamListener class that handles events,replies,deletes,direct_messages etc
    def on_data(self, data):
        #Collect the tweets in a list and push it as a batch to pub_sub
        self.tweets.append(data)
        #push the tweets to pub_sub when the batch is filled
        if len(self.tweets)>self.batch_size:
            #push to pubsub
            self.push_to_pubsub(self.tweets)
            #clear the list after pushing to pubsub
            self.tweets = []

    # on_error() is a method of StreamListener class that handles the error
     def on_error(self, status):
        print status

#Publish the tweets into pubsub once the batch_size is filled
def publish(client, pub_sub_topic, tweets):
    data = []
    for tweet in tweets:
        pub =base64.url_safe_b64encode(tweet)
        data.append({'message':pub})
    body = {'messages':data}
    response = client.projects().topics().publish(topic=pubsub_topic, body = body).execute(num_retries=MAX_RETRIES)
    return response



if __name__ == '__main__':
    tweets_listener = TweetsListener(StreamLisetner)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, tweets_listener)
    stream.filter(['epl', 'englishpremiereleague', 'arsenal', 'manu','reddevils','gunners'])
