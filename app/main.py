from django.shortcuts import render
from flask import Flask, render_template, request
import location
app = Flask(__name__)

@app.route("/")
def hello():
    data = location.give_region()
    return render_template('index.html', data=data)

@app.route("/upload-file", methods=["POST", "GET"])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        return f.filename
        
        
@app.route("/upload")
def upload():
    return render_template('upload.html')