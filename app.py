from flask import Flask, render_template, g, request ,redirect, url_for
from hamlish_jinja import HamlishExtension
#from werkzeug import ImmutableDict
from werkzeug.datastructures import ImmutableDict
import os
from flask_sqlalchemy import SQLAlchemy # 変更

class FlaskWithHamlish(Flask):
    jinja_options = ImmutableDict(
        extensions=[HamlishExtension]
    )
app = FlaskWithHamlish(__name__)

db_uri = "sqlite:///" + os.path.join(app.root_path, 'flask.db') # 追加
#db_uri = os.environ.get('DATABASE_URL') or "postgresql://localhost/flasknote"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri # 追加
db = SQLAlchemy(app) # 追加

class Entry(db.Model): # 追加
    __tablename__ = "entries" # 追加
    id = db.Column(db.Integer, primary_key=True) # 追加
    title = db.Column(db.String(), nullable=False) # 追加
    body = db.Column(db.String(), nullable=False) # 追加

@app.route('/')
def hello_world():
    entries = Entry.query.all() #変更
    return render_template('index.haml', entries=entries)

@app.route('/post', methods=['POST'])
def add_entry():
    entry = Entry()
    entry.title = request.form['title']
    entry.body = request.form['body']
    db.session.add(entry)
    db.session.commit()
    return redirect(url_for('hello_world'))