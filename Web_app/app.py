import scripts.textcleaning as TP
import pickle
import logging
import gensim
import praw
import os
import flask
import numpy as np
from praw.models import MoreComments
from werkzeug.utils import secure_filename
import urllib.request
from flask import Flask,send_file
from flask import render_template
from flask import request, redirect, jsonify
import json
from mimetypes import MimeTypes
from tempfile import mkdtemp
from werkzeug import serving
from werkzeug.datastructures import FileStorage
from werkzeug.datastructures import ImmutableMultiDict
import requests
import shutil
import ssl


#Logestic Regression data using PART_3
LOG = pickle.load(open('model_LOGREG.sav', 'rb'))
#PRAW credentials
reddit = praw.Reddit(client_id='gVDCZZMu0pAOFA', client_secret='y38ARCFgtLhnSzH3Z4iwW0SvBfw', user_agent='ScrappingData')



#predict flair by taking input as url
def prediction(url):
    submission = reddit.submission(url=url)
    data = {}
    data["title"] = str(submission.title)
    data["url"] = str(submission.url)
    data["body"] = str(submission.selftext)

    submission.comments.replace_more(limit=None)
    comment = ''
    count = 0
    for top_level_comment in submission.comments:
        comment = comment + ' ' + top_level_comment.body
        count += 1
        if(count > 10):
            break

    data["comment"] = str(comment)

    data['title'] = TP.clean_text(str(data['title']))
    data['body'] = TP.clean_text(str(data['body']))
    data['comment'] = TP.clean_text(str(data['comment']))

    feature_combine = data["title"] + data[
        "comment"] + data["body"] + data["url"]

    return LOG.predict([feature_combine])


app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('post.html')

#to allow only text file to be passed
ALLOWED_EXTENSIONS = set(['txt'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#to perform automated testing by passing a text file and returning response as JSON file
@app.route('/automated_testing', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            print ('**found file', file.filename)
            filename = secure_filename(file.filename)
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
  
            # resultant 
            dict1 = {} 
            
            i=0
            l=1
            with open(filename, 'r') as f:
              #line = f.readline()
             for line in f:
                if len(line)> 1:
                  print(len(line))
                  print(line.strip())
                  flair=np.array_str(prediction(line.strip()))
                  print(flair) 

                  dict1[line]=flair
                  i=i+1                 
                else:
                  break  

             out_file = open("test2.json", "w") 
             json.dump(dict1, out_file)  
             out_file.close() 

            return flask.send_file("test2.json", as_attachment=True)


#Given a url , predict the flair
@app.route("/action_page", methods=['POST'])
def action(flair=None):
    text = request.form.get('Posturl', False)
    flair = str(prediction(text))
    return render_template('result.html', flair=str(flair))


@app.route("/stats")
def stats():
    return render_template('graph.html')

# run the application
if __name__ == "__main__":
    app.run()
