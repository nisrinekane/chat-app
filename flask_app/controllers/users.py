from crypt import methods
from flask_app import app, render_template, request, redirect, session, bcrypt, flash
from flask_app.models.user import User


# ! ROOT ROUTE
@app.route('/')
def index():
    return render_template('index.html', error=True)

# ! REGISTER A USER
@app.route('/register', methods = ['post'])
def register():
    ## validate them
    print(request.form)
    # check if there is a user already with this email in our db
    data = {'email': request.form['email']}
    user_in_db =  User.get_one_with_email(data)
    # validate all fiels simultaneously
    if not User.validate_user(request.form):
        flash("Please fill out all fields")
        return redirect('/')
    ## check the password the supply matches the hash in the database
    if not bcrypt.check_password_hash(user_in_db.password, request.form['log_password']):
        flash("invalid password")
        return redirect('/logout')
    ## log in the use by adding to session
    session['first_name'] = user_in_db.first_name
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')

# ! LOGIN
@app.route('/login', methods = ['post'])
def login():
    ## check the database for the email they enter
    data = {'email': request.form['log_email']}
    user_in_db = User.get_one_with_email(data)
    # validate the fields
    # if email doesnt exist in the db
    if not user_in_db:
        flash("invalid email")
        return redirect('/')
    # if password doesnt match the hash in the db
    if not bcrypt.check_password_hash(user_in_db.password, request.form['log_password']):
        flash("invalid password")
        return redirect('/')
    ## log in the use by adding to session
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    return redirect('/dashboard')


# ! LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
    pass


# ! dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {'id':session['user_id']}
    return render_template('chat.html');


