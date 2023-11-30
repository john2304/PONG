import sqlite3
from flask_wtf import Form, RecaptchaField
from wtforms import StringField, validators


def unique_user(form):
    """
    when a user tries to submit a score to the leaderboard, they must use a unique name
    """

    db_path = 'database/pong.db'
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    user = list(c.execute("SELECT * FROM leader_board WHERE user_name = (?)", (form.user_name.data,)))

    # if the name is in the database already throw an error
    if user != []:
        raise validators.ValidationError('This name is taken, please choose a different one.')


class SubmitForm(Form):
    user_name = StringField('name', [validators.DataRequired(), unique_user])
    score = StringField("score")
    selected_ai_speed = StringField("ai_speed")
