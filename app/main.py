from flask import Flask, g, render_template, request, redirect, url_for
import sqlite3
import dateutil.parser
from datetime import datetime

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


@app.route("/")
def index():
    cur = get_db().cursor()
    res = cur.execute("SELECT min(id), max(id) FROM articles")
    counter = res.fetchone()
    return render_template("index.html", counter = counter)

@app.route('/', methods=['POST'])
def index_post():
    text = request.form['url']
    id = ''.join(x for x in text if x.isdigit())
    if id != '':
        return redirect(url_for('show_post', post_id=id))
    else: return "Некорректный ввод"


@app.route('/post/<int:post_id>/')
def show_post(post_id):
    cur = get_db().cursor()
    res = cur.execute("SELECT * FROM articles WHERE id = :id", {"id": post_id} )
    article = res.fetchone()

    if article == None:
        return render_template("404.html")

    res = cur.execute("SELECT * FROM comments WHERE article = :id", {"id": post_id} )
    comments = res.fetchall()

    date = dateutil.parser.parse(article[1])

    date = datetime.strftime(date, "%d.%m.%Y %H:%M")


    return render_template("post.html", post=article, date=date, comments=comments)