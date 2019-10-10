from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from forms import RegistrationForm, LoginForm
import os


host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/MoviesF')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
movies = db.movies
users = db.users

movie = [
{ 'title': 'Alvin and the Chipmunks 3', 'description':'Alvin and the Chipmunks 3 Full Movie English - Alvin Movies For Kid 2017',
      'link':"https://www.youtube.com/embed/Dbln5lECx2o",
      'image':"https://images-na.ssl-images-amazon.com/images/I/91isIKhEZBL._SX342_.jpg"},
{ 'title': 'Sophie & Sheba', 'description':'A seventeen-year-old girl, is forced to sell Sheba the elephant to a traveling\
        circus in order to afford the tuition for her ballet school.',
      'link':"https://www.youtube.com/embed/4un5gHqzbqI",
     'image':"https://m.media-amazon.com/images/M/MV5BMjE5NDU1NTIzOV5BMl5BanBnXkFtZTcwMTU2MTEzOA@@._V1_.jpg"},

{ 'title': 'Minions', 'description':'Minions Full Movie in English Compilation - Animation Movies - New Disney Cartoon 2019',
      'link':"https://www.youtube.com/embed/VO4F0FrSmzs",
     'image':"https://www.ft.com/__origami/service/image/v2/images/raw/https%3A%2F%2Fs3-ap-northeast-1.amazonaws.com%2Fpsh-ex-ftnikkei-3937bb4%2Fimages%2F9%2F1%2F8%2F0%2F3020819-2-eng-GB%2F1019N-USJ-Minions.jpg?source=nar-cms"},
{ 'title': 'Tom & Jerry', 'description':'LOONEY TUNES BIGGEST COMPILATION: Bugs Bunny, Daffy Duck and more!',
      'link':"https://www.youtube.com/embed/OM6xvpzqCUA",
     'image':"https://upload.wikimedia.org/wikipedia/en/5/5f/TomandJerryTitleCardc.jpg"},


]

movies.remove( { } )
movies.insert_many(movie)


app = Flask(__name__)

app.config['SECRET_KEY'] = '7ab8d9b149706a3cbec1a4b2af427e06c9db4c7449b6d042'

class user(object):
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def json(self):
        return {
            'username': self.username,
            'password': self.password,
            'email': self.email
            }

@app.route('/')
def index():
    """Return homepage."""
    return render_template('home.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    """Takes user to regestration page"""
    if request.method == 'POST':
        form = RegistrationForm()
        if form.validate_on_submit():
            if users.find_one({"username": form.username.data}):
                flash(f'That account already exists')
                return redirect(url_for('index'))
            else:
                current_user = users.insert_one(user(form.username.data, form.password.data, form.email.data).json())
                return redirect(url_for('index'))
        else:
            flash(f'Incorrect crednetials')
            return render_template('register.html', form=form)

    if request.method == 'GET':
        form = RegistrationForm()
        return render_template('register.html', form=form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    """Takes user to regestration page"""
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if users.find_one({"email": form.email.data}):
                if (form.email.data == users.find_one({"email": form.email.data})["email"]) and (form.password.data == users.find_one({"email": form.email.data})["password"]):
                    return redirect(url_for('movies_index'))
            else:
                flash(f'Log in unsuccessful. Please Check password and email', 'danger')
    return render_template('login.html', form=form)

    if request.method == 'GET':
        return render_template('login.html', form=form)

@app.route('/movies')
def movies_index():
    """Show all movies."""
    return render_template('movies_index.html', movies=movies.find())

@app.route('/movies/<movie_id>')
def movies_show(movie_id):
    """Show a single movie."""
    movie = movies.find_one({'_id': ObjectId(movie_id)})
    return render_template('movies_show.html', movie=movie)

@app.route('/movies/<movie_id>/edit', methods = ['GET', 'POST'])
def movies_edit(movie_id):
    """Show the edit form for a movie."""
    movie = movies.find_one({'_id': ObjectId(movie_id)})
    return render_template('movies_edit.html', movie=movie)

@app.route('/movies/<movie_id>', methods=['POST'])
def movies_update(movie_id):
    """Submit an edited movie."""
    updated_movie = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        # 'link': request.form.get('link').split(),
        'image': request.form.get('image')
    }
    movies.update_one(
        {'_id': ObjectId(movie_id)},
        {'$set': updated_movie})
    return redirect(url_for('movies_show', movie_id=movie_id))

@app.route('/movies/<movie_id>/delete', methods=['POST'])
def movies_delete(movie_id):
    """Delete one movie."""
    movies.delete_one({'_id': ObjectId(movie_id)})
    return redirect(url_for('movies_index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
