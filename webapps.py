import time
from hashlib import md5
from datetime import datetime
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.pymongo import PyMongo
import json
import uuid
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
import os
from DBStuffAPI import *
from knn import  *


DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('"routely"', silent=True)
mongo = PyMongo(app)
data = None

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        rv = mongo.db.users.find({"user_id": session['user_id']})
        g.user = rv[0] if rv.count() != 0 else None


def get_user_id(username):
    """Convenience method to look up the id for a username."""
    rv = mongo.db.user.find({"username": username})
    return rv[0]["user_id"] if rv.count() != 0 else None



def format_datetime(timestamp):
    """Format a timestamp for display."""
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')


def gravatar_url(email, size=80):
    """Return the gravatar image for the given email address."""
    return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
        (md5(email.strip().lower().encode('utf-8')).hexdigest(), size)

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        rv = mongo.db.users.find({"user_id": session['user_id']})
        g.user = rv[0] if rv.count() != 0 else None


@app.route('/')
def index():

    if not g.user:
        return render_template('landing.html')
    return render_template('dashboard.html', [session['user_id'], session['user_id'], 30])


@app.route('/data')
def data_handler():

    # if not g.user:
    #     return render_template('landing.html')
    # else:
    # element_db = ElementLngLatCostDB()
    # data = element_db.get_data()
    element_db = ElementLngLatCostDB()
    if data == None:
        rv =  element_db.get_data({"origin" : { "lat" : 12.9261416, "lng" : 77.5975514 } }, {"_id": 0, "origin": 0, "cost" : 0 } )
        lngs_and_lats = []
        lngs_and_lats_kmeans = []
        for i in rv:
            lngs_and_lats.append(i["dest"])
            lngs_and_lats_kmeans.append([i["dest"]["lat"],i["dest"]["lng"]])
        sbcluster = SubCluster(lngs_and_lats_kmeans,40)

        result = []
        for i in range(40):
            results = sbcluster.get_datapoints(i)
            result.append([])
            for r in results:
                latlng = {"lat" :r[0] , "lng" : r[1] }
                result[i].append(latlng)

        return json.dumps([result])
    else:

        return json.dumps(data)



@app.route('/login', methods=['GET', 'POST'])
def login():
    """Logs the user in."""
    if g.user:
        return redirect(url_for('index'))
    error = None
    if request.method == 'POST':
        rv = mongo.db.users.find({"username": request.form['username']})
        user = rv[0] if rv.count() != 0 else None
        if user is None:
            error = 'Invalid username'
        elif not check_password_hash(user['pw_hash'],
                                     request.form['password']):
            error = 'Invalid password'
        else:
            flash('You were logged in')
            session['user_id'] = user['user_id']
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registers the user."""
    if g.user:
        return redirect(url_for('index'))
    error = None
    if request.method == 'POST':
        if not request.form['username']:
            error = 'You have to enter a username'
        elif not request.form['email'] or \
                '@' not in request.form['email']:
            error = 'You have to enter a valid email address'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords do not match'
        elif get_user_id(request.form['username']) is not None:
            error = 'The username is already taken'
        else:
            mongo.db.users.insert(
                {"user_id" : str(uuid.uuid4()), "username": request.form['username'], "email": request.form['email'],
                 "pw_hash": generate_password_hash(request.form['password'])})
            flash('You were successfully registered and can login now')
            return redirect(url_for('login'))
    return render_template('register.html', error=error)


@app.route('/logout')
def logout():
    """Logs the user out."""
    flash('You were logged out')
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    """dashboard (testing)."""
    return render_template('dashboard.html', caravan=[{'code':1,'name':"1"},{'code':2,'name':'2'}])


# add some filters to jinja
app.jinja_env.filters['datetimeformat'] = format_datetime
app.jinja_env.filters['gravatar'] = gravatar_url

if __name__ == "__main__":
    app.run()