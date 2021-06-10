import os
import sys
import numpy as np
import pandas as pd
import re
from pymongo import MongoClient
from flask import Flask, request, jsonify
from flask_cors import CORS
import api_fun.myfun as myfun


# --------------------------------------------------
path_root = os.path.join(os.getcwd(), "../../")
path_key = os.path.join(path_root, './key/key.txt')
path_result = os.path.join(path_root, "./result")
json_contact = os.path.join(path_result, "./contact_all.json")

# database credential
conn_string = open(path_key, 'r').read()


# --------------------------------------------------
app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return 'Hello Cathay !'

@app.route("/rent591/cathay_search", methods=['POST'])
def cathay_search():
    post_raw = request.get_json()
    
    # mongodb
    cluster = MongoClient(conn_string)
    db = cluster['db_cathay']
    collection = db['cathay_search']
    
    # query input json
    results = collection.find({"$and": myfun.post_json(post_raw)}, {"_id":0})
    result = []
    for x in results:
        result.append(x)
    
    # query post_id
    re_post_id = []
    for x in result:
        re_post_id = re_post_id + [{'post_id':x['post_id']}]
    collection = db['meta_data']
    results = collection.find({"$or": re_post_id}, {"_id":0})
    result = []
    for x in results:
        result.append(x)
    cluster.close()
    
    return jsonify({'query': post_raw, 'query_num': len(result), 'query_results': result})


if __name__ == "__main__":
    # app.run(host = '0.0.0.0', port = 7406, debug = True)
    app.run(port = 7406, debug = True)
    
