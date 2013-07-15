
User browser webapp
===================

This flask app is a very simple per user file browser

## Configuration file example:

> import os
> 
> cfg_dir = os.path.dirname(os.path.abspath(__file__))
> 
> DEBUG = True
> SESSION_KEY = "complicate secret session key"
> DATABASE = os.path.join(cfg_dir, 'db.sqlite')
> USERS_DIR = os.path.join(cfg_dir, 'users')


## Create an user: 
 
> ubmanager --config app.cfg --username user --password pass

## Run test webserver:

> brunserver -c app.cfg

## WSGI example:

> see contrib/userbrowser.wsgi
