import json
import os

import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

from werkzeug.security import generate_password_hash


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()
    print(os.getcwd())
    with open(os.path.join(os.path.join(os.path.join(os.getcwd(),"webApp"),"flaskr"),"user.json")) as fid:
        user = json.load(fid)

    with current_app.open_resource('schema.sql') as f:
        sql_command = f.read().decode('utf8').replace("<USERNAME>",f"'{user['username']}'").replace("<PASSWORD>",f"'{generate_password_hash(user['password'])}'")
        db.executescript(sql_command)


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)