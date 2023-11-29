from flask import Flask, render_template, request, flash, redirect
from flask_wtf import FlaskForm, CSRFProtect, form
from wtforms import StringField, SubmitField, validators
from wtforms.validators import DataRequired
from flask_heroku import Heroku
import sqlite3

app = Flask(__name__)
heroku = Heroku(app)

# Set a secret key
app.config['SECRET_KEY'] = '\xab\xbb\xb5([_c\x9f\xa2m\x00\xfdX\x03\x97\xa5\xe82\x1f\xf8\xda1\xd6\xd8'  # Replace with your actual secret key

# Initialize CSRF protection
csrf = CSRFProtect(app)


class SubmitForm(FlaskForm):
    user_name = StringField('User_name', validators=[validators.DataRequired()])
    score = StringField('Score', validators=[validators.DataRequired()])  # Adding the score field
    submit = SubmitField('Submit')

def helper_submit_score(user_name, score):
    """
    no need for an app route, this method should just push to db and return boolean if it worked
    """
    try:
        db_path = 'database/pong.db'
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("INSERT INTO leader_board (user_name, score) values (?, ?)",
                  (form.user_name.data, form.score.data))
        conn.commit()
        conn.close()
        return True
    except:
        return False


def helper_get_leaderboard():
    db_path = 'database/pong.db'
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # use enumerate to generate rank for users.
    # Ties will be broken by time i.e. the first user to get a given score will appear highest
    return [val for val in enumerate(c.execute("SELECT * FROM leader_board ORDER BY score DESC"))]


@app.route("/")
def home():
    return render_template('index.html')


@app.route('/index/1player/', methods=['GET', 'POST'])
def player1():

    # count number of players in database and assign that number +1 to default anon name
    db_path = 'database/pong.db'
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    names = [tup[0] for tup in c.execute("SELECT user_name FROM leader_board")]

    form = SubmitForm()
    if form.validate_on_submit():
        # Perform the database submission operation here
        new_entry = helper_submit_score(user_name=form.user_name.data, score=form.score.data)
        c.execute("INSERT INTO leader_board (user_name, score) values (?, ?)",
                  (form.user_name.data, form.score.data))

        conn.commit()
        c.close()
        conn.close()

    # Get the selected AI speed from the form
    selected_ai_speed = request.form.get('ai_speed')
    return render_template("1player.html", title="1player", ai_speed=selected_ai_speed, form=form, names=names)

@app.route("/index/2player/", methods=['GET', 'POST'])
def player2():
    # count number of players in database and assign that number +1 to default anon name
    db_path = 'database/pong.db'
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    names = [tup[0] for tup in c.execute("SELECT user_name FROM leader_board")]

    form = SubmitForm()
    if form.validate_on_submit():
        # Perform the database submission operation here
        new_entry = helper_submit_score(user_name=form.user_name.data, score=form.score.data)
        c.execute("INSERT INTO leader_board (user_name, score) values (?, ?)",
                  (form.user_name.data, form.score.data))

        conn.commit()
        c.close()
        conn.close()

    # get selected score winpoint from the form
    selected_win_point = request.form.get('win_point')
    return render_template("2player.html", title="2player", win_point=selected_win_point, form=form, names=names)


@app.route('/index/leader_board/')
def leader_board():
    return render_template("leader_board.html", title="Leader Board", leader_board=helper_get_leaderboard())


if __name__ == "__main__":
    app.run(host='0.0.0.0')
