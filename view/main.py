import sys
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_behind_proxy import FlaskBehindProxy

sys.path.insert(0, '/home/codio/workspace/Magic_8ball/model')
from GetAnswer import create_tables, insert_user, find_user, insert_question

app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = ''

# App Home Page; Search bar and results
@app.route("/")
@app.route("/home")
def search():
    create_tables()
    return render_template('home.html', subtitle='Home Page', text='This is the home page')
   
# Page to register for an account
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.email.data}!', 'success')
        return redirect(url_for('user-page.html'))
    return render_template('register.html', title='Register', form=form)

# User Home Page
@app.route("/user")
def user_home():
    return render_template('user-page.html', subtitle='User Account Page', text='This is the user\'s home page')
    insert_user(int(hash(form.email.data))[1:], form.email.data, hash(form.password.data))
    return redirect(url_for('user-nav.html'))
    return render_template('register.html', title='Register', form=form)

# Login Page
@app.route("/login")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if find_user(int(hash(form.email.data))[1:], form.email.data, hash(form.password.data)):
            global id = int(hash(form.email.data))[1:]
            return redirect(url_for('home.html'))
        else:
            flash(f'No account found for {form.email.data} with the given password')
            return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")