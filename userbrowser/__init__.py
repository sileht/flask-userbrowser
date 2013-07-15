# -*- coding: utf-8 -*-
###
#
# Copyright (c) 2012 Mehdi Abaakouk <sileht@sileht.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA
#
###

import argparse
import os.path
import sys

import sqlite3

from flask import Flask
from flask import render_template, redirect, flash, g


from flask.ext.autoindex import AutoIndex
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from flask.ext.login import LoginManager, UserMixin, current_user
from flask.ext.login import login_user, logout_user, login_required
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired

from passlib.hash import sha256_crypt

app = Flask(__name__)
app.config['BOOTSTRAP_FONTAWESOME'] = True

Bootstrap(app)
AI = AutoIndex(app, add_url_rules=False)
login_manager = LoginManager()
login_manager.init_app(app)


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


class User(UserMixin):
    def __init__(self, userid, username):
        self.id = userid
        self.username = username

    def set_password(self, password):
        password_hash = sha256_crypt.encrypt(password)
        db = get_db()
        db.execute('update users set password = ? where id = ?',
                   [password_hash, self.id])
        db.commit()

    @staticmethod
    def check_and_get(username, password=None):
        row = get_db().execute(
            'select * from users where username = ?',
            [username]).fetchone()

        if not row:
            return

        userid, username, password_hash = row
        if password_hash and \
                sha256_crypt.verify(password, password_hash):
            return User(userid, username)

    @staticmethod
    def get(userid):
        cur = get_db().execute('select * from users where id = ?', [userid])
        row = cur.fetchone()
        if row:
            userid, username, password_hash = row
            return User(userid, username)


@login_manager.user_loader
def load_user(userid):
    return User.get(str(userid))


@app.route("/")
def home():
    if current_user.is_authenticated():
        return redirect('/browser')
    else:
        return redirect('/login')


@app.route("/login", methods=('GET', 'POST'))
def login():
    class LoginForm(Form):
        username = TextField("Login", validators=[DataRequired()])
        password = PasswordField("Mot de passe", validators=[DataRequired()])

    form = LoginForm()
    if form.validate_on_submit():
        user = User.check_and_get(str(form.username.data),
                                  form.password.data)
        if user:
            login_user(user)
            flash("Connection réussie")
            return redirect('browser')
    return render_template("login.html",
                           form=form)


@app.route("/settings", methods=('GET', 'POST'))
@login_required
def settings():
    class SettingsForm(Form):
        password = PasswordField("Mot de passe")
        password_bis = PasswordField("Mot de passe (Bis)")

    form = SettingsForm()
    if form.validate_on_submit():
        if form.password.data == form.password_bis.data:
            current_user.set_password(form.password.data)
            flash("Mot de passe changé")
            return redirect('/browser')
        else:
            flash("Les mot de passe ne corresponds pas")

    return render_template("settings.html",
                           form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


@AI.base.route('/browser')
@AI.base.route('/browser/')
@AI.base.route('/browser/<path:path>')
@login_required
def browser(path='/'):
    root = os.path.join(app.config.get("USERS_DIR", "users"),
                        current_user.username)
    print root
    return AI.render_autoindex(path=path, browse_root=root,
                               template='browser.html', endpoint='browser')


def load_config(filepath):
    app.config.from_pyfile(os.path.abspath(filepath))
    app.secret_key = app.config["SESSION_KEY"]
    app.debug = app.config.get("DEBUG", False)
    init_db()


def ubmanager():
    parser = argparse.ArgumentParser(prog='ubmanager')
    parser.add_argument('--config', '-c', help='config', required=True)
    parser.add_argument('--username', '-u', help='username', required=True)
    parser.add_argument('--password', '-p', help='password', required=True)
    parser.add_argument('--force', '-f', help='force user overwrite',
                        action='store_true')

    args = parser.parse_args(sys.argv[1:])

    load_config(args.config)

    with app.app_context():
        db = get_db()
        cur = db.execute('select * from users where username = ?',
                         [args.username])
        user_exist = cur.fetchone()

        if not args.force and user_exist:
            print "Error: user '%s' exist" % args.username
            return 1

        password_hash = sha256_crypt.encrypt(args.password)
        db = get_db()
        if user_exist:
            db.execute('update users set password = ? where username = ?',
                       [password_hash, args.username])
        else:
            db.execute('insert into users (username, password) values (?, ?)',
                       [args.username, password_hash])
        db.commit()

        print "Success: user '%s' modified" % args.username


def ubrunserver():
    parser = argparse.ArgumentParser(prog='ubmanager')
    parser.add_argument('--config', '-c', help='config', required=True)

    args = parser.parse_args(sys.argv[1:])

    load_config(args.config)
    app.run("0.0.0.0")
