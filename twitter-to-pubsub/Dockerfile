FROM google/python

RUN pip install --upgrade pip
RUN pip install tweepy
RUN pip install --upgrade google-api-python-client
RUN pip install python-dateutil

ADD twitter-to-pubsub.py /twitter-to-pubsub.py
ADD helper.py /helper.py


CMD python twitter-to-pubsub.py
