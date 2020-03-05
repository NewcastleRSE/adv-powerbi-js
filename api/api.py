import flask
from flask import request
from flask import make_response

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "<h1>Automating Data Visualisation</h1><p>This site is a prototype API for generating visualisations of uncertainty data using Blender.</p><p>For more, check out the GitHub Page <a href=\"https://github.com/NewcastleRSE/adv-powerbi-js\">here</a>.</p>"

@app.route('/api/v1/render/data', methods=['GET'])
def api_data():   
    data = request.args.get('data')
    imgurl = ""
    
    if (data == "good"):
        imgurl = "https://turing-vis-blender.s3.eu-west-2.amazonaws.com/myImage.png"
    else:
        imgurl = "https://turing-vis-mturk.s3.eu-west-2.amazonaws.com/images/high_0_10.png"
        
    resp = make_response(imgurl)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['custom-header'] = 'custom'
    return resp; 
     
app.run(host='0.0.0.0')