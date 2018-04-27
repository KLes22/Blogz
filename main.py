from flask import Flask, request, redirect, session, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://Blogz:launchcode@localhost:8889/Blogz"
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

app.secret_key = 'launchcode'

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')
    
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    post = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, post, owner):
        self.title = title
        self.post = post
        self.owner = owner

@app.before_request
def require_login():
    allowed_routes = ['login', 'list_blogs', 'index', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['Password']

        user = User.query.filter_by(username=username).first()

        if not username and not password:
            flash("Username and password cannot be blank")
            return render_template('login.html')
        if not password:
            flash("Invalid password")
            return render_template('login.html')
        if not username:
            flash("Invalid username")
            return render_template('login.html')

        if user and user.password == password:
            session['username'] = username
            flash("Successful login")
            return redirect('/newpost')
        if user and not user.password == password:
            flash("Invalid password")
            return render_template('login.html')
        if not user:
            flash("User does not exist.")
            return render_template('login.html')
 
    else:
        return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['Password']
        verify = request.form['VerifyPassword']

        existing_user = User.query.filter_by(username=username).first()

        if not username or not password or not verify:
            flash("Fields cannot be blank")
            return render_template('signup.html')

        if len(username) < 3:
            flash("Username must be three characters or more")
            return render_template('signup.html')
        if len(password) < 3:
            flash("Password must be three characters or more")
            return render_template('signup.html')

        if existing_user:
            flash("Username already exists")
            return render_template('signup.html')

        if not existing_user and not password==verify:
            flash("Passwords do not match")
            return render_template('signup.html')

        if not existing_user and password==verify:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')

    else: 
        return render_template('signup.html')

@app.route('/blog', methods=['POST', 'GET'])
def list_blogs():
    post_id = request.args.get('id')
    author_id = request.args.get('owner_id')
    all_posts = Blog.query.all()
    if post_id:
        indv_post = Blog.query.get(post_id)
        return render_template('singlepost.html', posts=indv_post)
    if author_id:
            posts_from_author = Blog.query.filter_by(owner_id=author_id)
            return render_template('singleUser.html', posts=posts_from_author)
    
    return render_template('blog.html', posts=all_posts)


def is_empty(x):
    if len(x) == 0:
        return True
    else:
        return False

@app.route('/newpost', methods=['GET', 'POST'])
def add_entry():

    if request.method == 'POST':
        title_error = ''
        blog_entry_error = ''

        post_title = request.form['blog_title']
        post_entry = request.form['blog_post']
        owner = User.query.filter_by(username=session['username']).first()
        new_post = Blog(post_title, post_entry, owner)

        if not is_empty(post_title) and not is_empty(post_entry):
            db.session.add(new_post)
            db.session.commit()
            post_link = "/blog?id=" + str(new_post.id)
            return redirect(post_link)
        else:
            if is_empty(post_title) and is_empty(post_entry):
                title_error = "Blog title is missing"
                blog_entry_error = "Blog content is missing"
                return render_template('newpost.html', title_error=title_error, blog_entry_error=blog_entry_error)
            elif is_empty(post_title) and not is_empty(post_entry):
                title_error = "Blog title is missing"
                return render_template('newpost.html', title_error=title_error, post_entry=post_entry)
            elif is_empty(post_entry) and not is_empty(post_title):
                blog_entry_error = "Blog content is missing"
                return render_template('newpost.html', blog_entry_error=blog_entry_error, post_title=post_title)

    else: 
        return render_template('newpost.html')

@app.route('/logout')
def logout():
    del session['username']
    flash("Successfully logged out")
    return redirect('/blog')

@app.route('/')
def index():
    all_users = User.query.distinct()
    author_id = request.args.get('owner_id')
    posts_from_author = Blog.query.filter_by(owner_id=author_id)
    if author_id:
        return render_template('singleUser.html', posts=posts_from_author)
    return render_template('index.html', usernames=all_users)

if __name__ == '__main__':
    app.run()