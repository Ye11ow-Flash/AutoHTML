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
        # try:
        res = main(destination)
        # if res!='templates/ui.html':
            # return render_template('ui.html')
            # return send_file('ui.html',as_attachment=True)
            # @after_this_request
            # def send(response):
                # with open('templates/ui.html','r') as inp_file:
                #     inp = inp_file.readlines()
                # with open('response.txt','w') as out_file:
                #     out_file.writelines(inp)
                # return send_file('templates/ui.html',as_attachment=True)
        
    return send_file('templates/ui.html',as_attachment=True)
# @app.route("/showui",methods=['GET','POST'])
# def new():
#     print("\n\n\n I am here!!!")
#     return render_template('ui.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000,debug = True)