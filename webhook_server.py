#!/usr/bin/env python3

# MIT License

# Copyright (c) 2022 catt0

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from bottle import Bottle, run, request
import threading
import json
from datetime import datetime
from pprint import pprint
import math
from sys import stdout

game_to_pic_key = {
    'Beat Saber': {'key': 'beatsaber', 'text': 'Beat Saber'},
}
default_pic_key = {'key': 'unknowngame', 'text': 'Unknown Game'},

got_data = threading.Event()
info_object = [{
    'application_id': 975147671247548416,
    'state': None,
    'details': 'Live at https://osp.home.catt0.de', # same here 
    'large_image': {'key': 'header', 'text': 'Beat Saber'},
    'small_image': None,
    'start_timestamp': None,
    'end_timestamp': None,
    'buttons': [{'label': 'Watch now',
                'url': 'https://osp.home.catt0.de/'
                    }],
}]

info_object_nothing = [{
'application_id': 975454847807680525,
    'state': 'Streaming nothing :(',
    'details': 'Old streams at https://osp.home.catt0.de',
    'large_image': None,
    'small_image': None,
    'start_timestamp': math.floor(datetime.timestamp(datetime.now())),
    'end_timestamp': None,
    'buttons': [{'label': 'Watch archive',
                'url': 'https://osp.home.catt0.de/'
                    }],
}]

info_json = None

app = Bottle()
@app.route('/hello')
def hello():
    got_data.set()
    return "Hello World!"

@app.route('/stream_start', method='POST')
@app.route('/name_change', method='POST')
def name_change():
    global info_json
    pickey = default_pic_key
    name = request.json['stream_name']
    url = request.json['stream_url']
    for k, v in game_to_pic_key.items():
        if k.lower() in name.lower():
            pickey = v
            break
    info_object[0]['large_image'] = pickey
    # I don't even know why there is a list around this
    # for now, just strip it
    try:
        info_object[0]['large_image'] = info_object[0]['large_image'][0]
    except:
        pass
    info_object[0]['state'] = name
    info_object[0]['buttons'][0]['url'] = url
    info_object[0]['start_timestamp'] = math.floor(datetime.timestamp(datetime.now()))
    info_json = json.dumps(info_object)
    got_data.set()
    return "Success"

@app.route('/stream_stop', method='POST')
def stream_stop():
    global info_json
    info_object_nothing[0]['start_timestamp'] = math.floor(datetime.timestamp(datetime.now()))
    info_json = json.dumps(info_object_nothing)
    got_data.set()
    return "Success"

def threadentry():
    run(app, host='0.0.0.0', port=8888, quiet=True)

bottle_thread = threading.Thread(target=threadentry)
bottle_thread.start()
print(json.dumps(info_object_nothing))
stdout.flush()
while True:
    if not got_data.wait():
        exit(0)
    got_data.clear()
    print(info_json)
    stdout.flush()
