from django.shortcuts import render
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def login():
    return render_template('login.html')

# @app.route("/login")
# def user():
#     return request.url

@app.route("/pwd", methods=['POST', 'GET'])
def pwd():
    if request.method == "POST":
        if "form1" in request.form:
            return "form1"
        elif "form2" in request.form:
            return "form2"

@app.route("/upload-file", methods=["POST", "GET"])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        return f.filename
        
        
@app.route("/upload")
def upload():
    return render_template('upload.html')

