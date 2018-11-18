import os
import json
import glob
import re
import csv
from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import xml.etree.cElementTree as ET

app = Flask(__name__)
app.config["DEBUG"] = True

SAVE_FOLDER = os.path.basename('savedFiles')
app.config['SAVE_FOLDER'] = SAVE_FOLDER
UPLOAD_FOLDER = os.path.basename('uploadedFile')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world():
    return render_template('index.html')

# POST method
@app.route('/upload', methods=['POST','GET'])
def upload_file():
    if request.method == 'POST':
        file = request.files['image']
        f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(f)
        with open(f,'r') as myfile:
            data=myfile.read().replace('\n', ' ')
        #print(data)
        clean_data = remove_tags(data)
        print(clean_data)
        clean_data = re.sub(',',' ',clean_data)
        clean_data = re.sub(' +',' ',clean_data)
        m = re.search("FOR THE COUNTY OF (\w+) (\w+) (\w+)",clean_data)
        if m is None:
            m = re.search("(\w+) (\w+) an individual",clean_data)
        print("Plaintiff is: " + m.group(1) + " " + m.group(2))

        result = re.search('vs.(.*)Defendants', clean_data)
        if result is None:
            result = re.search('v.(.*)j Defendants.', clean_data)
        print("Defendent is:" + result.group(1))

        # save to file
        file_name = os.path.splitext(os.path.basename(f))[0]
        # print(file_name)
        parsed_file = open(SAVE_FOLDER + '/' + file_name + '.txt', 'w')
        parsed_file.write(
            "Plaintiff is: " + m.group(1)+ " " + m.group(2) + "\n<br>" +
            "Defendent is: " + result.group(1)
            )
        return ("Plaintiff is: " + m.group(1) + " " + m.group(2) +"<br>"+ "Defendent is:" + result.group(1))
    return render_template('success.html')

# function to remove XML tags
def remove_tags(text):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', text)

# GET method to get the output file with file name
@app.route('/lawsuit/<file_name>', methods=['GET'])
def getfile(file_name):
    print(file_name)
    with open(SAVE_FOLDER + "/" + file_name + ".txt", 'r') as myfile:
        data=myfile.read().replace('\n', '')
    return (data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)
