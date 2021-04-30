from flask import Flask, flash, render_template, session, redirect, request, url_for, jsonify
from functools import wraps
import urllib.request
import pymongo
from pymongo import MongoClient
#import magic
import urllib.request
from werkzeug.utils import secure_filename
import os


UPLOAD_FOLDER = 'static/img'



ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'

# Database
# client = pymongo.MongoClient('localhost', 27017)
# db = client.user_login_system

# Docker:
client = MongoClient(host='test_mongodb',
                      port=27017, 
                      username='root', 
                      password='pass',
                    authSource="admin")
db = client["user_db"]

# client = MongoClient(host = 'localhost', port = 27017)
# db = client["user_db"]



def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# Decorators
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')
  
  return wrap

# Routes
from user import routes

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/dashboard/',methods=['GET', 'POST'])
@login_required
def dashboard():
  if request.method == 'POST':
    # check if the post request has the file part
    if 'file' not in request.files:
      flash('No file part')
      return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
      flash('No selected file')
      return redirect(request.url)
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      return redirect(url_for('dashboard',
                                filename=filename))
  return '''
  <!doctype html>
  <title>Upload new File</title>
  <h1>Upload new File</h1>
  <form method=post enctype=multipart/form-data>
    <input type=file name=file>
    <input type=submit value=Upload>
  </form>
  '''

@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


# @app.route('/create', methods = ['POST'])
# def create():
#   if 'profile_image' in request.files:
#     profile_image = request.files['profile_image']
#     db.save_file(profile_image.filename, profile_image)
#     db.users.insert({'username' : request.form.get('username', 'profile_image_name: profile_image.filename ')})