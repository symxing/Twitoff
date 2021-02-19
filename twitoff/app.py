"""Main app/routing file for Twitoff"""

from flask import Flask, render_template, request
from .models import DB, User, insert_example_users
from .twitter import add_or_update_user
from .predict import predict_user
from .nlp_model import NLP

def create_app():
    """Creating and configuring an instance of the Flask application"""
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    DB.init_app(app)
    nlp = NLP()

    # http://127.0.0.1:5000/
    @app.route('/', methods=['GET'])
    def landing():
        DB.drop_all()
        DB.create_all()
        example_users = ['elonmusk', 'katyperry', 'rihanna', 'barackobama']
        for user in example_users:
            add_or_update_user(user)
        return render_template("hello.html", title="Home", users=User.query.all())

    @app.route('/update')
    def update():
        # insert_example_users()
        return render_template('hello.html', title="TwitOff", users=Users.query.all())

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('hello.html', title="TwitOff")

    #This route 'POST's data to the server
    @app.route('/compare', methods=['POST'])
    def compare():
        user1 = request.form['selected_user_1'] #extracts the form data
        user2 = request.form['selected_user_2']
        tweet_text = request.values['tweet_text']

        if user1 == user2:
            message = "Cannot compare the same user to itself"

        else:
            prediction = predict_user(user1, user2, tweet_text)
            message = str(prediction) + " is more likely to have said " + str(tweet_text)

        return render_template('prediction.html', title="Predict Tweet Author", message=message)

    return app

app=create_app()

if __name__ == "__main__":
    app.run()