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


###**Testing email service**
To use a test SMTP run the following command in terminal:

    python -m smtpd -n -c DebuggingServer localhost:25