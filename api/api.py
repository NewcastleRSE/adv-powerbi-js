import flask
from flask import request

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Automating Data Visualisation</h1><p>This site is a prototype API for generating visualisations of uncertainty data using Blender.</p><p>For more, check out the GitHub Page <a href=\"https://github.com/NewcastleRSE/adv-powerbi-js\">here</a>.</p>"

@app.route('/api/v1/render/data', methods=['GET'])
def api_data():
    return "https://turing-vis-blender.s3.eu-west-2.amazonaws.com/myImage.png";
     
@app.route('/api/v1/render/nodata', methods=['GET'])
def api_nodata():
    return "https://turing-vis-mturk.s3.eu-west-2.amazonaws.com/images/high_0_10.png";
	 
app.run(host='0.0.0.0')