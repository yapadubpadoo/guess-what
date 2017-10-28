from flask import Flask, redirect, url_for, session, request, jsonify
from flask_cors import CORS, cross_origin
import pprint
import json
import sys
import os 
import requests
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import arrow
import configparser
import redis
import subprocess

#### to subscribe app for apge
# curl -i -X POST \
#  -d "access_token=EAATy1TA0IBQBADnhDMVmvI1REwwtZCPCrhYmEwHbH59EVj8Fx5gdgN751z2Dqqq7VwTOt0MPOzCS0a5sqLmBrOMsS4KlHUs5xHeLDiYvOKszxPaGJAAWrpUSmOICiDTzL2g4iZBqGt7XQMMTczc4lahGiNDFuCdU0CZCGZADRvjMNf05ofeSBCHx9EGUSqdajnUf0opixgZDZD" \
#  "https://graph.facebook.com/v2.10/527202220962403/subscribed_apps"

config = configparser.ConfigParser()
config.read('config/production.ini')
mongo_client = MongoClient(config['mongodb']['uri'], connect=False)
tickets_collection = mongo_client.guess_what_facebook.tickets
ticket_parent_collection = mongo_client.guess_what_facebook.ticket_parent
ticket_children_collection = mongo_client.guess_what_facebook.ticket_children

app = Flask(__name__)
app.debug = True
app.secret_key = "my-secret"
CORS(app)
redis_client = redis.Redis(
    host=config['redis']['host'],
    port=config['redis']['port'], 
    password=config['redis']['password'])

def format_data(data):
    return {
        '_id': data['value']['comment_id'] \
            if 'comment_id' in data['value'] else data['value']['post_id'],
        'created_time': arrow.get(data['value']['created_time']).datetime,
        'message': data['value']['message'],
        'sender_name': data['value']['sender_name'],
        'parent_id': data['value']['parent_id'] \
            if 'parent_id' in data['value'] else None,
        'post_id': data['value']['post_id'],
        'sender_profile_picture': 'https://graph.facebook.com/' + data['value']['sender_id'] + '/picture?height=32',
    }

def tokenize(text):
    r = requests.post('http://35.163.91.157:3031/tokenize-text', data = {'text':text})
    return r.json()['data']

def text_classification(label, fasttext_test_data):
    messages = subprocess.Popen(('echo', '"' + fasttext_test_data + '"'), stdout=subprocess.PIPE)
    predicted_results = subprocess.check_output(
        ('fasttext', 'predict', label +'.bin', '-'),
        stdin=messages.stdout
        )
    result = predicted_results.decode('utf-8').replace('__label__', '').strip()
    return result

def handle_data(data):
    if data['field'] == 'feed' \
        and data['value']['item'] == 'comment'\
        and data['value']['verb'] == 'add':
        # it's a comment level, ticket one
        if data['value']['parent_id'] == data['value']['post_id']:
            ticket = format_data(data)
            tokenized_text = tokenize(ticket['message'])

            if text_classification('complain', tokenized_text) == 'complain':
                tag = 'complain'
                tag_priority = 100
            elif text_classification('question', tokenized_text) == 'question':
                tag = 'question'
                tag_priority = 50
            else:
                tag = 'other'
                tag_priority = 1
            ticket['tag'] = tag
            ticket['tag_priority'] = tag_priority

            if text_classification('negative', tokenized_text) == 'negative':
                sentiment = 'negative'
                sentiment_priority = 100
            elif text_classification('positive', tokenized_text) == 'positive':
                sentiment = 'positive'
                sentiment_priority = 50
            else:
                sentiment = 'neutral'
                sentiment_priority = 1
            ticket['sentiment'] = sentiment
            ticket['sentiment_priority'] = sentiment_priority

            try:
                inserted_id = tickets_collection.insert_one(ticket).inserted_id 
                pprint.pprint("[++] Ticket ID = {} has been created".format(inserted_id))
                ticket['created_time'] = arrow.get(ticket['created_time']).to('Asia/Bangkok').format('YYYY-MM-DD HH:mm:ss')
                redis_client.publish('new-case', json.dumps({'data': ticket}))
            except DuplicateKeyError:
                pprint.pprint("[--] Ignore duplicated ticket ID = {}".format(ticket['_id']))
                pass
        # it's reply comment level
        else:
            ticke_child = format_data(data)
            try:
                inserted_id = ticket_children_collection.insert_one(ticke_child).inserted_id 
                pprint.pprint("[+++] Ticket child ID = {} has been created".format(inserted_id))
            except DuplicateKeyError:
                pprint.pprint("[---] Ignore duplicated ticket child ID = {}".format(ticke_child['_id']))
                pass
    elif data['field'] == 'feed' \
        and data['value']['item'] == 'status'\
        and data['value']['verb'] == 'add':
        ticket_parent = format_data(data)
        try:
            inserted_id = ticket_parent_collection.insert_one(ticket_parent).inserted_id 
            pprint.pprint("[+] Parent post ID = {} has been added".format(inserted_id))
        except DuplicateKeyError:
            pprint.pprint("[-] Ignore duplicated post ID = {}".format(ticket_parent['_id']))
            pass
    
@app.route('/fb/get-updates', methods=['GET','POST'])
def fb_realtime_updates():
    if request.args.get('hub.verify_token', '') == 'guesswhat':
        return request.args.get('hub.challenge')
    else:
        updates = json.loads(request.data.decode('utf-8'))
        pprint.pprint(updates)
        
        for changes in updates['entry']:
            for data in changes['changes']:
                handle_data(data)
    return "OK"

@app.route('/tickets', methods=['GET'])
def get_tickets():
    tickets = tickets_collection.find(
        {"sender_name":{"$ne":"Guesswhattelecom"}}
    ).sort(
        [
            ('tag_priority', -1), 
            ('sentiment_priority', -1), 
            ('created_time', 1)
        ]
    )
    result = []
    for ticket in tickets:
        ticket['created_time'] = arrow.get(ticket['created_time']).to('Asia/Bangkok').format('YYYY-MM-DD HH:mm:ss')
        result.append(ticket)
    return jsonify({"data": result})

@app.route('/ticket/<_id>', methods=['GET'])
def get_ticket(_id):
    thread = []
    ticket = tickets_collection.find_one({"_id":_id})
    parent = ticket_parent_collection.find_one({"_id": ticket['parent_id']})
    parent['type'] = 'post'
    parent['created_time'] = arrow.get(parent['created_time']).to('Asia/Bangkok').format('YYYY-MM-DD HH:mm:ss')
    ticket['type'] = 'comment'
    ticket['created_time'] = arrow.get(ticket['created_time']).to('Asia/Bangkok').format('YYYY-MM-DD HH:mm:ss')
    thread.append(parent)
    thread.append(ticket)
    children = ticket_children_collection.find({"parent_id": ticket['_id']})
    for child in children:
        child['type'] = 'reply-comment'
        child['created_time'] = arrow.get(child['created_time']).to('Asia/Bangkok').format('YYYY-MM-DD HH:mm:ss')
        thread.append(child)
    return jsonify({"data": thread})

@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({"hello": "world"})
