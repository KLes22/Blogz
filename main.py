from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://Blogz:launchcode@localhost:8889/Blogz"
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

app.secret_key = 'launchcode'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), unique=True)
    body = db.Column(db.string(2000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.owner = owner

@app.before_request
def require_login():
    allowed_routes = ['login', 'blog', 'signup', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/blog', methods=['GET', 'POST'])
def blog():
    id = request.args.get('id')
    user = request.args.get('username')

    if id:
        blog = Blog.query.filter_by(owner_id=user).all()
        username = User.query.filter_by(id=user).first()
        retur rener_template('singleUser.html', blogs=blogs, user=username)

    else:
        blogs = Blog.query.all()
        return render_template('blog.html', blogs=blogs)

@app.route('/newpost', methods=['GET', 'POST'])
def new_post():
    title_err = ''
    body_err = ''
    
    if request.method == 'POST':
        title = requets.form['title']
        body = request.form['body']
        owner = User.query.filter_by(username=session['username']).first()

        if title == '' or body == '':
            title_err = "Please enter a valid title"
            body_err = "Please enter content"
            return render_template('newpost.html', title_err=title_err, body_err=body_err)

        else:
            blog = Blog(title, body, owner)
            db.session.add(blog)
            db.session.commit()
            return redirect('/blog?id=' + str(blogid))

    return render_template('newpost.html')

@app.route('/login', methods=['POST', 'GET'])
def login()
    username_err = ''
    password_err = ''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

    if username == '' or password == ''
        username_err = 'Enter a valid username'
        password_err = 'Enter a valid password'
        return render_template('login.html', username_err=username_err, password_err=password_err)

    if user and user.password == password:
        session['username'] = username
        return redirect('/newpost')

    else:
        username_err = "User doesn't exist, please register."
        return render_template('login.html', username_err=username_err)

    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    username_err = ''
    verify_err = ''
    password_err = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

         
        existing_user = User.query.filter_by(username=username).first()
        
        if username == '' or password == '' or verify == '':
            username_err = 'Enter a valid email'
            password_err = 'Enter a valid password'
            verify_err = 'Please verify password'
            return render_template('signup.html', username_err=username_err, password_err=password_err, verify_err=verify_err)

        if '@' not in username or '.' not in username or ' ' in username:
            username_err = 'Enter a valid email'
            return render_template('signup.html', username_err=username_err)
        
        if len(password) < 3:
            password_err = "Password must contain more than 3 characters!"
            return render_template('signup.html', password_err=password_err)
        
        if existing_user:  
            username_err = 'User already exists! Continue to login'
            return render_template('signup.html', username_err=username_err)
        
        if not verify == password:
            verify_err = 'Passwords do not match!'
            return render_template('signup.html', verify_err=verify_err) 

        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')

    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
return redirect('/blog')


if __name__ == '__main__':
    app.run()