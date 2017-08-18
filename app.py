from flask import Flask, render_template, request, jsonify, redirect, session
from flask import jsonify,abort
import json
import random
from flask_cors import CORS,cross_origin
from pymongo import MongoClient


app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
CORS(app)

#make mongodb connection
connection=MongoClient("mongodb://localhost:27017/")

@app.route('/')
def main():
    return render_template('main.html')





@app.route('/addname')
def addname():
    if request.args.get('yourname'):
        session['name']=request.args.get('yourname')
        return redirect(url_for('main'))
    else:
        return render_template('addname.html',session=session)

@app.route('/clear')
def clearsession():
    session.clear()
    return redirect(url_for('main'))

@app.route("/api/v1/info")
def home_index():
    api_list=[]
    db=connection.cloud_native.apirelease

    for row in db.find():
        api_list.append(str(row))
    return jsonify({'api_version':api_list}), 200

@app.route('/adduser')
def adduser():
    return render_template('adduser.html')

@app.route('/addtweets')
def addtweetjs():
    return render_template('addtweets.html')

@app.errorhandler(404)
def resource_not_found(error):
    return make_response(jsonify({'error':'Resource not found'}),404)

@app.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error':'Bad Request'}),400)


@app.route('/api/v1/users/<int:user_id>',methods=['GET'])
def get_user(user_id):
    return list_user(user_id)



@app.route('/api/v1/users',methods=['GET'])
def get_users():
    return list_users()


@app.route('/api/v1/users',methods=['POST'])
def create_user():
    if not request.json or not 'username' in request.json or not 'email' in request.json or not 'password' in request.json:
        abort(400)
    user={
        'username':request.json['username'],
        'email': request.json['email'],
        'name':request.json.get('name',""),
        'password':request.json['password'],
        'id':random.randint(1,1000)

    }
    return jsonify({'status':add_user(user)}),201


@app.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = {}
    user['id']=user_id
    key_list = request.json.keys()
    for i in key_list:
        user[i] = request.json[i]
    return jsonify({'status': upd_user(user)}), 200


@app.route('/api/v1/users', methods=['DELETE'])
def delete_user():
    if not request.json or not 'username' in request.json:
        abort(400)
    user=request.json['username']
    return jsonify({'status': del_user(user)}), 200



#input
#process loop through mongodb to find all users
#output return all users info

def list_users():
    api_list=[]
    db=connection.cloud_native.users
    for row in db.find():
        api_list.append(str(row))
    return jsonify({'user_list':api_list}), 200


#input user_id
#process loop through mongodb to find user info
#output user info by id
def list_user(user_id):
    api_list=[]
    db=connection.cloud_native.users
    for i in db.find({'id':user_id}):
        api_list.append(str(i))

    if api_list ==[]:
        abort(404)
    return jsonify({'user_details':api_list}), 200




# Deleting User
def del_user(del_user):
    db = connection.cloud_native.users
    api_list=[]
    for i in db.find({'username':del_user}):
        api_list.append(str(i))

    if api_list == []:
        abort(404)
    else:
       db.remove({"username":del_user})
       return "Success"


#input user info
#process update user data
#output return success or failed mesg

def upd_user(user):
    api_list=[]
    print (user)
    db_user = connection.cloud_native.users
    users = db_user.find_one({"id":user['id']})
    for i in users:
        api_list.append(str(i))
    if api_list == []:
       abort(409)
    else:
        db_user.update({'id':user['id']},{'$set': user}, upsert=False )
        return "Success"

def add_user(new_user):
    api_list=[]
    print(new_user)

    db=connection.cloud_native.users
    user=db.find({'$or':[{"username":new_user['username']}, {"email":new_user['email']}]})
    for i in user:
        print(str(i))
        api_list.append(str(i))

    if api_list==[]:
        db.insert(new_user)
        return "success"
    else:
        abort(409)

    return jsonify(a_dict)




@app.route('/api/v2/tweets', methods=['GET'])
def get_tweets():
    return list_tweets()

@app.route('/api/v2/tweets/<int:id>', methods=['GET'])
def get_tweet(id):
    return list_tweet(id)



@app.route('/api/v2/tweets', methods=['POST'])
def add_tweets():

    user_tweet = {}
    if not request.json or not 'username' in request.json or not 'body' in request.json:
        abort(400)
    user_tweet['tweetedby'] = request.json['username']
    user_tweet['body'] = request.json['body']
    user_tweet['timestamp']=strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
    user_tweet['id'] = random.randint(1,1000)

    return  jsonify({'status': add_tweet(user_tweet)}), 201


def list_tweets():
    api_list=[]
    db=connection.cloud_native.tweet
    for row in db.find():
        api_list.append(str(row))
    return jsonify({'tweets_list':api_list})


# List specific tweet
def list_tweet(user_id):
    print (user_id)
    db = connection.cloud_native.tweets
    api_list=[]
    tweet = db.find({'id':user_id})
    for i in tweet:
        api_list.append(str(i))
    if api_list == []:
        abort(404)
    return jsonify({'tweet': api_list})



# Adding tweets
def add_tweet(new_tweet):
    api_list=[]
    print (new_tweet)
    db_user = connection.cloud_native.users
    db_tweet = connection.cloud_native.tweets

    user = db_user.find({"username":new_tweet['tweetedby']})
    for i in user:
        api_list.append(str(i))
    if api_list == []:
       abort(404)
    else:
        db_tweet.insert(new_tweet)
        return "Success"


if __name__=="__main__":
    app.run(host='127.0.0.1',port=5000,debug=True)
