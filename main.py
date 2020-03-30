from flask import Flask, escape, request, g, render_template, redirect
import sqlite3
from datetime import datetime
from json import loads

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'superwde412sjersxcsdjhasjdasd'

DATABASE = "./habr.db"

# helper method to get the database since calls are per thread,
# and everything function is a new thread when called
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.route('/')
def hello():
    return render_template("index.html")


@app.route('/post/<int:post_id>/')
def show_post(post_id):
    post_id = str(post_id)
    cur = get_db().cursor()
    res = cur.execute("SELECT * FROM articles WHERE id = :id", {"id": post_id} )
    article = res.fetchone()

    if article == None:
        return render_template("404.html")

    res = cur.execute("SELECT * FROM comments WHERE article = :id", {"id": post_id} )
    comments = res.fetchall()

    date = datetime.strptime(article[1], "%Y-%m-%dT%H:%M:%S%z")
    date = datetime.strftime(date, '%d-%m-%Y %H:%M')


    return render_template("post.html", post=article, date=date, comments=comments)