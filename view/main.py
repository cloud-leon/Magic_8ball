import sys
from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm, QuestionForm
#from flask_behind_proxy import FlaskBehindProxy

sys.path.insert(0, '../model')
from GetAnswer import create_tables, insert_user, find_user, insert_question, get_history, get_answer

app = Flask(__name__)
#proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = 'thisisasecretkey'


# App Home Page; Search bar and results
@app.route("/")
def search():
    create_tables()
    return render_template('home.html', subtitle='Home Page', text='This is the home page')
   

# Page to register for an account
@app.route("/register", methods=['GET', 'POST'])
def register():
    create_tables()
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        insert_user(hash(request.form['email'][1:]), request.form['email'], hash(request.form['password']))
        flash(f'Account created for {form.email.data}!', 'success')
        return redirect(url_for('user-nav.html'))
    return render_template('register.html', title='Register')


@app.route("/login")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if find_user(int(hash(form.email.data))[1:], form.email.data, hash(form.password.data)):
            global id
            id = int(hash(form.email.data))[1:]
            return redirect(url_for('home.html'))
        else:
            flash(f'No account found for {form.email.data} with the given password')
            return redirect(url_for('user-nav.html'))
    return render_template('login.html', title='Login', form=form)


@app.route("/user")
def user():
    try:
        data = get_history(id)
    except error:
        flash("You must be logged in to reach this page")
        return redirect(url_for('home.html'))
    form = QuestionForm
    if form.validate_on_submit():
        answer = get_answer(form.question.data)
    return render_template('uers-nav.html', title='User', form=form)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")