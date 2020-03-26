import flask
from flask import request
from flask import make_response

import random
import string

import boto3
from botocore.exceptions import NoCredentialsError

import subprocess

app = flask.Flask(__name__)
app.config["DEBUG"] = True

filepath = "D:/nms210/Projects/adv-powerbi-js"

class Record:
    def __init__(self, string, result):
        self.string = string
        self.result = result

numRecords =  5
lastCalls = []

def upload_to_aws(local_file, bucket, s3_file):
    session = boto3.Session()
    s3 = session.client('s3')

    try:
        s3.upload_file(local_file, bucket, s3_file, ExtraArgs={'ACL':'public-read'})
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

@app.route('/', methods=['GET'])
def home():
    return "<h1>Automating Data Visualisation</h1><p>This site is a prototype API for generating visualisations of uncertainty data using Blender.</p><p>For more, check out the GitHub Page <a href=\"https://github.com/NewcastleRSE/adv-powerbi-js\">here</a>.</p>"

@app.route('/api/v1/render/data', methods=['POST'])
def api_data():   
    global filepath
    global numRecords
    global lastCalls
    
    json_str = request.args.get('data')
    
    for lastCall in lastCalls:
        if (lastCall.string == json_str):               # first check that the dataset is not identical to that used in the previous render
            print("Duplicate Data Detected")
            return lastCall.result;
    
    lastCallString = json_str                        # if data has actually changed, render the new image
    json_str = json_str.replace('\"', '\\"')
    
    callStr = "blender \"" + filepath + "//CityModel.blend\" --background -noaudio --use-extension 1 --python \"" + filepath + "//GlyphDataTest.py\" --engine BLENDER_EEVEE --render-output //glyph_json_risk_# -F PNG --render-frame 1 -- " + "\"" + json_str + "\""
    
    #print("CALL STRING:")
    #print(callStr)
    
    return_code = subprocess.call(callStr, shell=True)
    
    local_file = filepath+'/glyph_json_risk_1.png'
    bucket = 'turing-adv'
    s3_file_name = ('render_'+randomString()+'.png')
    uploaded = upload_to_aws(local_file, bucket, s3_file_name)
    
    imgurl = "https://turing-adv.s3.eu-west-2.amazonaws.com/" + s3_file_name
        
    resp = make_response(imgurl)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['custom-header'] = 'custom'
    
    if (len(lastCalls) >= numRecords):               # store record for future use
        del lastCalls[0]
    
    lastCall = Record(lastCallString, resp)
    lastCalls.append(lastCall)
    
    return resp; 
    
app.run(host='0.0.0.0')