#!/bin/bash

#Build docker image for twitter_to_pubsup streaming pipleline
docker build -t gcr.io/$DEVSHELL_PROJECT_ID/tweets_to_pubsub_pipleline pubsub_dataflow_bigquery_twitter_streaming_pipleine/twitter_to_pubsub

#Save the docker image to GCR
gcloud docker push gcr.io/$DEVSHELL_PROJECT_ID/tweets_to_pubsub_pipleline

#Create a pubsup topic to collect the tweets_to_pubsub
gcloud beta pubsub topics create epl_tweets

#Create a Google Container Engine Cluster and enable it to write to Pub/Sub
gcloud container clusters create epl_tweets_analytics_cluster --num-nodes=1 --scopes=https://www.googleapis.com/auth/pubsub

#Get the credentials to access the pubsub_pipleine
gcloud container clusters get-credentials epl_tweets_analytics_cluster

#Deploy the pubsub_pipleine to the cluster
kubectl create -f pubsub_dataflow_bigquery_twitter_streaming_pipleine/twitter_to_pubsub/tweets_to_pubsub.yaml

#Create the BigQuery Dataset to save the tweets
bd mq epl_analytics

#Start the Dataflow pipeleine that will take the tweets from pubsub topic and
#do NLP processing for sentimental analysis and save the tweets to BigQUery
cd pubsub_dataflow_bigquery_twitter_streaming_pipleine/pubsub_dataflow_bq_pipeline/
mvn compile exec:java -Dexec.mainClass = com.esperti.pubsub_dataflow_bq.TweetsProcessor -Dexec.args="--streaming --stagingLocation=gs://epl_sentimental_analysis --project=$DEVSHELL_PROJECT_ID"
