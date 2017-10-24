FROM google/python

RUN mkdir /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install tweepy
RUN pip install --upgrade google-api-python-client
RUN pip install python-dateutil

ADD twitter-to-pubsub.py /app/twitter-to-pubsub.py
ADD helper.py /app/helper.py

ADD . /app

CMD python twitter-to-pubsub.py
