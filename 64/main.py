from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies-collection.db'
Bootstrap5(app)

# CREATE DB
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[int] = mapped_column(String(150), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(50), nullable=True)
    img_url: Mapped[str] = mapped_column(String(100), nullable=False)

with app.app_context():
    db.create_all()

# CREATE TABLE
'''
new_movie = Movie(
        title="Avatar The Way of Water",
        year=2022,
        description="Set more than a decade after the events of the first film, learn the story of the Sully Family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
        rating=7.3,
        ranking=9,
        review="I liked the water.",
        img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg")

second_movie = Movie(
        title="Phone Booth",
        year=2002,
        description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
        rating=7.3,
        ranking=10,
        review="My favourite character was the caller.",
        img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg")

with app.app_context():
    db.session.add(second_movie)
    db.session.commit()
'''

# Get API
url = 'https://api.themoviedb.org/3/search/movie'

auth = open('auth.txt', 'r').read()[:-1]

headers = {
    'accept': 'application/json',
    'Authorization': auth
}

class editForm(FlaskForm):
    rating = StringField('Your Rating Out of 10 e.g. 7.5', validators=[DataRequired()])
    review = StringField('Your Review', validators=[DataRequired()])
    submit = SubmitField('Done')

class addForm(FlaskForm):
    movie = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField('Add Movie')

@app.route('/')
def home():
    movies = db.session.execute(db.select(Movie).order_by(Movie.rating.desc())).scalars()
    all_movies = movies.all()

    for i in range(len(all_movies)):
        all_movies[i].ranking = i+1
    db.session.commit()

    return render_template('index.html', movies=all_movies)

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = addForm()
    if request.method == 'POST':
        movie_title = form.movie.data
        response = requests.get(url, headers=headers, params={'query': movie_title})
        return render_template('select.html', movies=response.json()['results'])
    return render_template('add.html', form=form)

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    form = editForm()
    id = request.args.get('id')
    movie = db.get_or_404(Movie, id)
    if request.method == 'POST':
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', form=form, movie=movie)

@app.route('/delete')
def delete():
    id = request.args.get('id')
    movie = db.get_or_404(Movie, id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/find')
def find():
    id = request.args.get('id')
    url = 'https://api.themoviedb.org/3/movie/' + id
    response = requests.get(url, headers=headers)
    movie = response.json()
    new_movie = Movie(
            title=movie['title'],
            year=movie['release_date'][:4],
            description=movie['overview'],
            img_url='https://image.tmdb.org/t/p/w500' + movie['poster_path'])
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for('edit', id=new_movie.id))

if __name__ == '__main__':
    app.run(debug=True)
