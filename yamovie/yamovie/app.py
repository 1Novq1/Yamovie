import os
from flask import Flask, render_template, g
from flask_cors import CORS
from users_routes import users_bp
from movies_routes import movies_bp
from api import api
from data_manager.data_models import User, Movie, UserMovie, MovieReview, db
from data_manager.users import Users
from data_manager.movies import Movies
from data_manager.users_movies import UsersMovies
from data_manager.movies_reviews import MoviesReviews
from data_manager.sqlite_data_manager import SQLiteDataManager

app = Flask(__name__)
app.app_context()
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                        os.path.join(basedir, 'data/yamovie.sqlite')

db.init_app(app)
with app.app_context():
    db.create_all()

users_data_manager = Users(SQLiteDataManager('id', User, db))
movies_data_manager = Movies(SQLiteDataManager('id', Movie, db))
users_movies_data_manager = UsersMovies(SQLiteDataManager('id', UserMovie, db))
movies_reviews_data_manager = MoviesReviews(SQLiteDataManager('id', MovieReview, db))

app.register_blueprint(users_bp)
app.register_blueprint(movies_bp)
app.register_blueprint(api, url_prefix='/api')


CORS(app)


@app.before_request
def before_request():
    g.users_data_manager = users_data_manager
    g.movies_data_manager = movies_data_manager
    g.users_movies_data_manager = users_movies_data_manager
    g.movies_reviews_data_manager = movies_reviews_data_manager


@app.route('/')
def home():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(_error):
    return render_template('404.html'), 404


@app.errorhandler(400)
def bad_request_error(error):
    print(error)
    return render_template('400.html', errors=error.description), 400


@app.errorhandler(500)
def internal_server_error(_error):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(port=5002)
