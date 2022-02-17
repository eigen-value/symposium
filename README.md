###**SYMPOSIUM**
Symposium is a Flask application for the management of Conference web-sites. This application largely follows the mega-known [Flask mega-tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) by Miguel Grinberg.

What follows is a list of the most relevant features:

- Participants subscription with automated confirmation email and captcha
- Participants can express an accommodation preference
- Participants must upload a pdf copy of the wire-transfer fee payment
- A login protected Flask-admin back-end to manage users, participants and all the relevant models
- User password recovery by email confirmation

###**Dependencies**
Major dependencies:

- Flask-mail
- Flask-admin
- Flask-login
- Flask-sqlalchemy
- Flask-migrate
- Flask-WTF

###**Installation**
Download/clone the repo and create a virtualenv alongside the application code.
 
pip-install the dependencies from requirements.txt
    
        (venv) $ pip install -r requirements.txt

###**Initialization**
Set FLASK_APP env variable locally on Windows machines (eg cmd window):

    set FLASK_APP=symposium.py
    
    (venv) $ flask db init
    
###**Migration**
After changing the DB schema, to migrate run:

    (venv) $ flask db migrate -m "insert migration message here"

This will generate the migration scripts only - under /migrations/versions. In order to apply the scripts run:

    (venv) $ flask db upgrade

###**Updating**

Pull a new version and restart

    (venv) $ git pull                                        # download the new version
    (venv) $ sudo supervisorctl stop symposium     # stop the current server
    (venv) $ flask db upgrade                                # upgrade the database IF NEEDED
    (venv) $ sudo supervisorctl start symposium    # start a new server


###**Administration back-end**
Accessing the administration back-end needs a superuser.

The steps to activate a superuser are:

- Register the administrator user as a normal user via the application registration service.
Go to /admin and in the login page click on "Register"
- use sqlite3 or any other database api interface to create a Role with "super" type privileges
- assign the "super" role to the administrative user inserting a record in the user_role table

###**Testing email service**
To use a test SMTP run the following command in terminal:

    python -m smtpd -n -c DebuggingServer localhost:25
    
###**Sending emails**
If using SMTPS on port 465 remember to set in config:

    MAIL_USE_TLS = 0
    MAIL_USE_SSL = 1
