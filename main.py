from flask import Flask, render_template, redirect, url_for, request,flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap5
from wtforms.widgets import NumberInput
from wtforms import StringField, SubmitField ,SelectField
from wtforms.validators import InputRequired,ValidationError,URL,DataRequired, NumberRange
import sqlite3
import requests





app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'
app.secret_key = 'hello'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Movies_data.db"
db = SQLAlchemy()
db.init_app(app)
Bootstrap5(app)


class Movieform(FlaskForm):
    title = StringField('Movie:-', render_kw={"autocomplete": "off"},validators=[InputRequired()])
    img_url = StringField('Image Url', render_kw={"autocomplete": "off"},validators=[DataRequired(), URL()])
    Year = StringField('Year',render_kw={"autocomplete": "off"}, widget=NumberInput(), validators=[InputRequired(message="This field is required.")])
    ranking = StringField('Rank', render_kw={"autocomplete": "off"},validators=[InputRequired()])
    description = StringField('Description', render_kw={"autocomplete": "off"},validators=[InputRequired()])
    rating = StringField('Rating',render_kw={"autocomplete": "off"},widget=NumberInput(), validators=[InputRequired()])
    review = StringField('Review', render_kw={"autocomplete": "off"},validators=[InputRequired()])
    submit = SubmitField('Submit')

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    ranking = db.Column(db.Float, nullable=True)
    description = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    review = db.Column(db.String, nullable=True)
    img_url = db.Column(db.String, nullable=False)

class ratemovie(FlaskForm):
    rating = StringField("Your Rating Out of 10 e.g. 7.5" ,render_kw={"autocomplete": "off"},validators=[InputRequired()])
    review = StringField("Your Review" , render_kw={"autocomplete": "off"},validators=[InputRequired()])
    submit = SubmitField("Done")

# Create the database tables
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    result = db.session.execute(db.select(Movie).order_by(Movie.rating))
    all_movies = result.scalars().all() # convert ScalarResult to Python List
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()

    return render_template("index.html", movies=all_movies)

@app.route("/Add", methods=["GET", "POST"])
def add_movies():
    form = Movieform()
    if request.method == 'POST':
        url = f'http://www.omdbapi.com/?s={form.title.data}&apikey=4a347cbe'  # Replace with the URL of the website or API you want to access
        response = requests.get(url)
        search_results = response.json()
        return render_template('add.html' ,form=form, search_results = search_results)
    elif request.method == 'GET':
        flash("you are successfuly logged in",category='alert')  
        return render_template('add.html' ,form=form)
    
@app.route("/get_movie_details", methods=["GET", "POST"])
def get_movie_details():
    parameter_value = request.args.get('parameter_name')
    url = f'http://www.omdbapi.com/?i={parameter_value}&apikey=4a347cbe'  # Replace with the URL of the website or API you want to access
    response = requests.get(url)
    if response.status_code == 200:
            movie_data = response.json()
            new_movie = Movie(
                title=movie_data['Title'],
                year=int(movie_data['Year']),
                description=movie_data['Plot'],
                rating=1,
                ranking=None,
                review=None,
                img_url=movie_data['Poster']
            )
            with app.app_context():
                db.session.add(new_movie)
                db.session.commit()
                return redirect(url_for('home'))
    

@app.route("/Edit", methods=["GET", "POST"])
def Edit():
    form = ratemovie()
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie, movie_id)
    if request.method == 'POST':
        if form.validate_on_submit():
            movie.rating = float(form.rating.data)
            movie.review = form.review.data
            db.session.commit()
            return redirect(url_for('home'))
    else:
        form.rating.data = movie.rating 
        form.review.data = movie.review
        return render_template('edit.html', form=form, movie=movie)
    # If the request method is not 'POST' or the form doesn't validate, render the template.
    
@app.route("/delete")
def delete_movie():
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie, movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


