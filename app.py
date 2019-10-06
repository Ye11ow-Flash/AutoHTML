from flask import Flask, request, Response,render_template,send_file,jsonify,send_from_directory
from flask import json, flash, redirect, session, abort
from flask_cors import CORS, cross_origin
from flask import jsonify
from flask import after_this_request
from render import *
from io import StringIO
app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
@app.route("/",methods=['GET','POST'])
def home():
    return render_template('index.html')

@app.route("/getui",methods=['GET','POST'])
def get_html():
    path = request.form.get('file')
    target = os.path.join(APP_ROOT, 'templates/')
    if not os.path.isdir(target):
        os.mkdir(target)
    for file in request.files.getlist("file"):
        filename = file.filename
        destination = "/".join([target, filename])
        file.save(destination)
        try:
            res = main(destination)
            return render_template('ui.html')
        except:
            return render_template('meme.html')

@app.route("/downloadui",methods=['GET','POST'])
def download_html():
    path = request.form.get('file')
    target = os.path.join(APP_ROOT, 'templates/')
    if not os.path.isdir(target):
        os.mkdir(target)
    for file in request.files.getlist("file"):
        filename = file.filename
        destination = "/".join([target, filename])
        file.save(destination)
        try:
            res = main(destination)
            return render_template('ui.html')
        except:
            return send_file('templates/ui.html',as_attachment=True)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000,debug = True)