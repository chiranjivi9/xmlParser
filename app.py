import os
import glob
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import csv
import xml.etree.cElementTree as ET
import re

app = Flask(__name__)
# app = Flask(__name__, instance_relative_config=True)

SAVE_FOLDER = os.path.basename('savedFiles')
app.config['SAVE_FOLDER'] = SAVE_FOLDER
UPLOAD_FOLDER = os.path.basename('uploadedFile')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():

    file = request.files['image']
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    # add your custom code to check that the uploaded file is a valid image and not a malicious file (out-of-scope for this post)
    file.save(f)

    with open(f,'r') as myfile:
        data=myfile.read().replace('\n', ' ')
    #print(data)
    clean_data = remove_tags(data)
    print(clean_data)
    # , an individual
    # m = re.search("Attorneys for Plaintiff (\w+) (\w+)", clean_data)
    clean_data = re.sub(',',' ',clean_data)
    clean_data = re.sub(' +',' ',clean_data)
    m = re.search("(\w+) (\w+) an individual",clean_data)
    if m is None:
        m = re.search("Attorneys for Plaintiff (\w+) (\w+)",clean_data)
    print("Plaintiff is: " + m.group(1) + " " + m.group(2))

    # result = re.search('vs.(.*)Defendants', clean_data)
    # print("Defendent is:" + result.group(1)) 

    # save to file

    # new_file = open('file.txt', 'w') #open the file(this will not only open the file also
    # #if you had one will create a new one on top or it would create one if you
    # #didn't have one
    # new_file.write("Plaintiff is: " + m.group(1) + " " + m.group(2) + "\n \nDefendent is:" + result.group(1)) #this will put the info in the file
    # new_file.close()
    #parseXML()
    return render_template('success.html')

def remove_tags(text):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', text)

# def parseXML():
#     dir_path = UPLOAD_FOLDER
#     files = [ ]
#     f = open(dir_path)
#     for file in files:  # add files to the message
#         file_path = os.path.join(dir_path, file)
#         print(file_path)
#         tree = ET.ElementTree(file = file_path)
#         root = tree.getroot()
#         for data in root:
#             # if(data.tag=='plane')
#             return child.get('color')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)
