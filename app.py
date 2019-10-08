from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from forms import RegistrationForm, LoginForm


client = MongoClient()
db = client.MoviesF
movies = db.movies
users = db.users
movie = [
{ 'title': 'aladdin', 'description':'Aladdin 2019 Full Movie Subtitle Indonesia aladin 2019 sub indonesia',
    'realse_date': 'May 19, 2019', 'time': '1:27:39', 'link':"https://www.youtube.com/embed/jYMP6WUlYoo",
    'image':"https://cdn3-www.comingsoon.net/assets/uploads/2019/07/Aladdin.jpg"},
{ 'title': 'Alvin and the Chipmunks 3', 'description':'Alvin and the Chipmunks 3 Full Movie English - Alvin Movies For Kid 2017',
     'realse_date': 'Nov 30, 2017', 'time': '1:16:20', 'link':"https://www.youtube.com/embed/Dbln5lECx2o",
      'image':"https://images-na.ssl-images-amazon.com/images/I/91isIKhEZBL._SX342_.jpg"},
{ 'title': 'Sophie & Sheba', 'description':'A seventeen-year-old girl, is forced to sell Sheba the elephant to a traveling\
        circus in order to afford the tuition for her ballet school.',
     'realse_date': 'Feb 5, 2016', 'time': '1:43:23', 'link':"https://www.youtube.com/embed/4un5gHqzbqI",
     'image':"https://m.media-amazon.com/images/M/MV5BMjE5NDU1NTIzOV5BMl5BanBnXkFtZTcwMTU2MTEzOA@@._V1_.jpg"}
]

movies.remove( { } )
movies.insert_many(movie)


app = Flask(__name__)

app.config['SECRET_KEY'] = '7ab8d9b149706a3cbec1a4b2af427e06c9db4c7449b6d042'




@app.route('/')
def index():
    """Return homepage."""
    return render_template('home.html')

@app.route('/movies')
def movies_index():
    """Show all movies."""
    return render_template('movies_index.html', movies=movies.find())

@app.route('/movies/<movie_id>')
def playlists_show(movie_id):
    """Show a single movie."""
    movie = movies.find_one({'_id': ObjectId(movie_id)})
    # return f'movie id {movie_id} /n {movie}'
    return render_template('movies_show.html', movie=movie)

@app.route('/forms', methods=['POST'])
def form():
    """create a new form."""
    if request.method == "POST":
        data = request.form.to_dict()
        return f' Hello World! {request.form.to_dict()} Hello World!'

    # return redirect(url_for('playlists_index'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    """Takes user to regestration page"""
    # client sends flask a POST request (clients sends over data)
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
    if form.validate_on_submit():
        if form.email.data == 'red@gmail.com' and form.password.data == 'password':
            flash(f'You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash(f'Log in unsuccessful. Please Check password and user name', 'danger')
    return render_template('login.html', form=form)
