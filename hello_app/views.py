from datetime import datetime
import requests
import json
from flask import Flask, request, jsonify, render_template, url_for
from . import app
#
url = "https://smokerdetect-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/c8c993a8-c90d-4b37-b3cf-86fd7b854f9b/classify/iterations/SmokerDetector/url"
global result
result=""

#
@app.route("/")
def home():
    return render_template("home.html")

#
@app.route('/predict',methods = ['POST'])
def predict():
    int_features =request.form.get('experience')
    payload = json.dumps(
        {
            "Url": "{}".format(int_features)
        }
    )
    headers = {
    'Prediction-Key': '53b52759e2694da9a75fd1fa4c413b67',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    out=json.loads(response.text)
    predictions=out['predictions']
    max_prob=0.000001
    num=0
    for n,i in enumerate(predictions):
        if i['probability']>max_prob:
            max_prob=i['probability']
            num=n
    tag="Predicted Image Tag : {}".format(predictions[num]['tagName'])
    prob="Prediction Probability : {}".format(predictions[num]['probability']*100)
    return render_template('result.html',user_image=int_features,imgtag=tag,imgprob=prob)



@app.route('/predict_api',methods=['POST'])
def predict_api():
    data = request.get_json(force=True)
    payload = json.dumps(
        {
            "Url": "{}".format(data.values())
        }
    )
    headers = {
    'Prediction-Key': '53b52759e2694da9a75fd1fa4c413b67',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    output = response
    return jsonify(output)




app.run(host='0.0.0.0')

#
#@app.route("/about/")
#def about():
#    return render_template("about.html")

#@app.route("/contact/")
#def contact():
#    return render_template("contact.html")

#@app.route("/hello/")
#@app.route("/hello/<name>")
#def hello_there(name = None):
#    return render_template(
#        "hello_there.html",
#        name=name,
#        date=datetime.now()
#    )

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")
