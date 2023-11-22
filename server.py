from flask import Flask, render_template, g
import sqlite3

app = Flask(__name__)
db_location = 'database.sqlite3.db'


@app.route("/index/")
def index():
    return render_template('index.html')


@app.route("/index/1player/")
def game():
    return render_template('1player.html')


def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = sqlite3.connect(db_location)
        g.db = db
    return db


@app.teardown_appcontext
def close_dbconnection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('database.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


# @app.route('/index/')
# def root():
#   db = get_db()
#  db.cursor().execute('insert into user_info values("001", "John", 10, 5)')
# db.commit()


if __name__ == "__main__":
    app.run(host='0.0.0.0')
