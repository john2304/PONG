from flask import Flask, render_template, request
from flask_wtf import FlaskForm, CSRFProtect, form
from wtforms import StringField, SubmitField, validators
from wtforms.validators import DataRequired
from flask_heroku import Heroku
import sqlite3

app = Flask(__name__, static_folder='static')
heroku = Heroku(app)

# Set a secret key
app.config[
    'SECRET_KEY'] = '\xab\xbb\xb5([_c\x9f\xa2m\x00\xfdX\x03\x97\xa5\xe82\x1f\xf8\xda1\xd6\xd8'  # Replace with your actual secret key

# Initialize CSRF protection
csrf = CSRFProtect(app)


# defines a Flask form named SubmitForm with fields for user_name and score, mandatory fields
class SubmitForm(FlaskForm):
    user_name = StringField('User_name', validators=[validators.DataRequired()])
    score = StringField('Score', validators=[validators.DataRequired()])  # Adding the score field
    submit = SubmitField('Submit')


# submits the user_name and score to the leaderboard
def helper_submit_score(user_name, score, selected_ai_speed):
    # method should just push to db and return boolean if it worked

    # error handling
    try:
        db_path = 'database/pong.db'  # Defines the path to the SQLite database file
        conn = sqlite3.connect(db_path)  # establishes a connection to the SQLite database
        c = conn.cursor()  # The cursor is used to execute SQL queries on the database

        # test - selected_ai_speed = request.form.get('ai_speed') # gets speed from form

        # sql query to add new record to leaderboard
        c.execute("INSERT INTO leader_board (user_name, score, selected_ai_speed) values (?, ?, ?)",
                  (user_name, score, selected_ai_speed))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error inserting into database: {e}")
        return False


# collects the database and uses sql to display the leaderboard table
def helper_get_leaderboard():
    db_path = 'database/pong.db'
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    return [val for val in enumerate(c.execute("SELECT * FROM leader_board ORDER BY score DESC"))]


# home page
@app.route("/index/")
def home():
    return render_template('index.html')


# page for user vs ai
@app.route('/index/1player/', methods=['GET', 'POST'])
def player1():
    # count number of players in database and assign that number +1 to  anon name
    db_path = 'database/pong.db'
    conn = sqlite3.connect(db_path)  # connecting to the db
    c = conn.cursor()
    names = [tup[0] for tup in c.execute("SELECT user_name FROM leader_board")]  # sql to retrieve names

    # Get the selected AI speed from the form
    selected_ai_speed = request.form.get('ai_speed')

    form = SubmitForm()
    if form.validate_on_submit():
        # Perform the database submission operation here
        new_entry = helper_submit_score(user_name=form.user_name.data, score=form.score.data,
                                        selected_ai_speed=selected_ai_speed)
        conn.commit()
        c.close()
        conn.close()
    # loads the game with the users options
    return render_template("1player.html", title="1player", ai_speed=selected_ai_speed, form=form, names=names)


# player vs play er page, with w/s and uparrow/downarrow
@app.route("/index/2player/", methods=['GET', 'POST'])
def player2():
    form = SubmitForm()

    # get selected score winpoint from the form
    selected_win_point = request.form.get('win_point')
    # load game page with users options
    return render_template("2player.html", title="2player", win_point=selected_win_point, form=form)


# leaderboard page
@app.route('/index/leader_board/')
def leader_board():
    return render_template("leader_board.html", title="Leader Board", leader_board=helper_get_leaderboard())


if __name__ == "__main__":
    app.run(host='0.0.0.0')
