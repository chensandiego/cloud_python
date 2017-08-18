from flask import Flask, render_template, request, jsonify, redirect, session
from flask import jsonify,abort
import json

from flask_cors import CORS,cross_origin
from pymongo import MongoClient

app = Flask(__name__)

#make mongodb connection and create db, collections and documents
connection=MongoClient("mongodb://localhost:27017/")
def create_mongodatabase():
    try:
        dbnames=connection.database_names()
        if 'cloud_native' not in dbnames:
            db = connection.cloud_native.users
            db_tweets = connection.cloud_native.tweets
            db_api = connection.cloud_native.apirelease

            db.insert({
                "email":"eric.strom@gmail.com",
                "id":33,
                "name":"Eric Stromberg",
                "password":"eric@123",
                "username":"eric.strom"
            })

            db_tweets.insert({
                "body":"new blog post,launch your app with the aws startup kit! #AWS",
                "id":18,
                "timestamp":"2017-03-11T06:39:40Z",
                "tweetedby":"eric.strom"
            })

            db_api.insert({
                "buildtime":"2017-01-01 10:00:00",
                "links":"/api/v1/users",
                "methods":"get,post,put,delete",
                "version":"v1"
            })

            db_api.insert({
                "buildtime":"2017-02-11 10:00:00",
                "links":"/api/v2/tweets",
                "methods":"get,post",
                "version":"v1"
            })
            print ("db initialize completed")
        else:
            print("db already initialized")
    except:
        print("db creation failed")

if __name__=="__main__":
    create_mongodatabase()
    app.run(host='127.0.0.1',port=5000,debug=True)
