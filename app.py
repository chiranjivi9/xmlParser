import os
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import csv
# import requests
import xml.etree.ElementTree as ET


app = Flask(__name__)

UPLOAD_FOLDER = os.path.basename('image')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['xml']
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

    # add your custom code to check that the uploaded file is a valid image and not a malicious file (out-of-scope for this post)
    file.save(f)
    parseXML(f)
    return render_template('index.html')

# def parseXML(xmlfile):


if __name__ == '__main__':
   app.run(debug = True)
