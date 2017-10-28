from flask import Flask, redirect, url_for, session, request, jsonify
import pprint
import json
import sys
import os 
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import arrow
import configparser

#### to subscribe app for apge
# curl -i -X POST \
#  -d "access_token=EAATy1TA0IBQBADnhDMVmvI1REwwtZCPCrhYmEwHbH59EVj8Fx5gdgN751z2Dqqq7VwTOt0MPOzCS0a5sqLmBrOMsS4KlHUs5xHeLDiYvOKszxPaGJAAWrpUSmOICiDTzL2g4iZBqGt7XQMMTczc4lahGiNDFuCdU0CZCGZADRvjMNf05ofeSBCHx9EGUSqdajnUf0opixgZDZD" \
#  "https://graph.facebook.com/v2.10/527202220962403/subscribed_apps"

config = configparser.ConfigParser()
config.read('config/production.ini')
mongo_client = MongoClient(config['mongodb']['uri'])
tickets_collection = mongo_client.guess_what_facebook.tickets
ticket_parent_collection = mongo_client.guess_what_facebook.ticket_parent
ticket_children_collection = mongo_client.guess_what_facebook.ticket_children

app = Flask(__name__)
app.debug = True
app.secret_key = "my-secret"

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
    }

def handle_data(data):
    if data['field'] == 'feed' \
        and data['value']['item'] == 'comment'\
        and data['value']['verb'] == 'add':
        # it's a comment level, ticket one
        if data['value']['parent_id'] == data['value']['post_id']:
            ticket = format_data(data)
            try:
                inserted_id = tickets_collection.insert_one(ticket).inserted_id 
                print("[++] Ticket ID = {} has been created".format(inserted_id))
            except DuplicateKeyError:
                print("[--] Ignore duplicated ticket ID = {}".format(ticket['_id']))
                pass
        # it's reply comment level
        else:
            ticke_child = format_data(data)
            try:
                inserted_id = ticket_children_collection.insert_one(ticke_child).inserted_id 
                print("[+++] Ticket child ID = {} has been created".format(inserted_id))
            except DuplicateKeyError:
                print("[---] Ignore duplicated ticket child ID = {}".format(ticke_child['_id']))
                pass
    elif data['field'] == 'feed' \
        and data['value']['item'] == 'status'\
        and data['value']['verb'] == 'add':
        ticket_parent = format_data(data)
        try:
            inserted_id = ticket_parent_collection.insert_one(ticket_parent).inserted_id 
            print("[+] Parent post ID = {} has been added".format(inserted_id))
        except DuplicateKeyError:
            print("[-] Ignore duplicated post ID = {}".format(ticket_parent['_id']))
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

# if __name__ == '__main__':
#     app.run()
