from flask import Flask, render_template, request 
from flask import redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Language, Work
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# initiates the flask framework
app = Flask(__name__)

# This is used for google oauth credientials
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Literature Menu Application"

# Connect to Database and create database session
engine = create_engine('sqlite:///worldliterature.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# used to login and also for anti-forgery token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

# redirecting to this page allows for logging in using google login API
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;\
    -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# redirecting to this page allows for logging out using google login API
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: ' 
    print login_session['username']
    if access_token is None:
      print 'Access Token is None'
      response = make_response(json.dumps('Current user not connected.'), 401)
      response.headers['Content-Type'] = 'application/json'
      return response
    url = 'https://accounts.google.com/o/oauth2/revoke? \
    token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
      # del login_session['access_token'] 
      # del login_session['gplus_id']
      # del login_session['username']
      # del login_session['email']
      # del login_session['picture']
      login_session.clear()
      response = make_response(json.dumps('Successfully disconnected.'), 200)
      response.headers['Content-Type'] = 'application/json'
      return response
    else:
  
      response = make_response(json.dumps('Failed to revoke token for given user.',\
        400))
      response.headers['Content-Type'] = 'application/json'
      return response

# API endpoint (JSON) for each literary work within each language
@app.route('/language/<int:language_id>/JSON')
def languageJSON(language_id):
    language = session.query(Language).filter_by(id=language_id).one()
    work = session.query(Work).filter_by(
        language_id=language_id).all()
    return jsonify(Work=[i.serialize for i in work])

#welcome
@app.route('/base')

def welcome():
    language = session.query(Language).all()
    return render_template('base.html',language = language,
        login_session = login_session)

# display available language
@app.route('/')
@app.route('/language/')
def language():
    language = session.query(Language).all()
    return render_template('language.html', language = language,
        login_session = login_session)

# display works within a specific language
@app.route('/language/<int:language_id>/')
def workList(language_id):
    language = session.query(Language).filter_by(id=language_id).one()
    work = session.query(Work).filter_by(language_id=language.id)
    return render_template('worklist.html', language=language, work=work)

# add a new language to the catalog
@app.route('/language/new/', methods=['GET', 'POST'])
def newLanguage():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newLang = Language(language=request.form['name'])
        session.add(newLang)
        session.commit()
        return redirect(url_for('language'))
    else:
        return render_template('newlanguage.html')

# Deletes a specific language
@app.route('/language/<int:language_id>/delete/', methods=['GET', 'POST'])
def deleteLanguage(language_id):
    if 'username' not in login_session:
        return redirect('/login')
    languageToDelete = session.query(Language).filter_by(id = language_id).one()
    if request.method == 'POST':
        session.delete(languageToDelete)
        session.commit()
        return redirect(url_for('language'))
    else:
        return render_template('deletelanguage.html', l = languageToDelete)


# Creates a new work within a specific language
@app.route('/language/<int:language_id>/new/', methods=['GET', 'POST'])
def newWork(language_id):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newWork = Work(
            title=request.form['title'], 
            author=request.form['author'],
            translator=request.form['translator'],
            translation_year=request.form['year'],
            genre=request.form['genre'],
            amazon_link=request.form['link'],
            summary=request.form['summary'],
            language_id=language_id)
        session.add(newWork)
        session.commit()
        return redirect(url_for('workList', language_id=language_id))
    else:
        return render_template('newwork.html', language_id=language_id)

# edit/change the values of specific attributes a literary work
@app.route('/language/<int:language_id>/<int:work_id>/edit/', methods=['GET', 'POST'])
def editWork(language_id, work_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedWork = session.query(Work).filter_by(id = work_id).one()
    if request.method == 'POST':
        if request.form['title']:
            editedWork.title = request.form['title']   
        if request.form['author']:
            editedWork.author = request.form['author']
        if request.form['translator']:
            editedWork.translator = request.form['translator']
        if request.form['year']:
            editedWork.translation_year = request.form['year']
        if request.form['genre']:
            editedWork.genre = request.form['genre']
        if request.form['link']:
            editedWork.amazon_link = request.form['link']
        if request.form['summary']:
            editedWork.summary = request.form['summary']
        session.add(editedWork)
        session.commit() 
        return redirect(url_for('workList', language_id=language_id))
    else:
        return render_template('editwork.html', language_id=language_id,
            work_id = work_id, w = editedWork)


# Deletes a specific literary work
@app.route('/language/<int:language_id>/<int:work_id>/delete/', 
    methods=['GET', 'POST'])
def deleteWork(language_id, work_id):
    if 'username' not in login_session:
        return redirect('/login')
    workToDelete = session.query(Work).filter_by(id = work_id).one()
    if request.method == 'POST':
        session.delete(workToDelete)
        session.commit()
        return redirect(url_for('workList', language_id = language_id))
    else:
        return render_template('deletework.html', w = workToDelete)




# Part of the black magic of Flask server and the port where it runs
if __name__ == '__main__':
    app.secret_key = 'secret'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)



