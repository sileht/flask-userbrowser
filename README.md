User browser webapp
===================

This flask app is a very simple per user file browser

## Installation in virutalenv:

    apt-get install python-virtualenv python-pip
    
    mkdir myapp
    cd myapp
    
    virtualenv venv
    source venv/bin/activate
    pip install -e git+https://github.com/sileht/flask-userbrowser.git#egg=userbrowser


## Configuration file example:

    import os
    
    cfg_dir = os.path.dirname(os.path.abspath(__file__))
    
    DEBUG = True
    SESSION_KEY = "complicate secret session key"
    DATABASE = os.path.join(cfg_dir, 'db.sqlite')
    USERS_DIR = os.path.join(cfg_dir, 'users')


## Create an user: 
 
    ubmanager --config app.cfg --username user --password pass

## Run test webserver:

    ubrunserver -c app.cfg

## Run as WSGI application:

example in contrib/userbrowser.wsgi
