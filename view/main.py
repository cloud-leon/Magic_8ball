import sys
from flask import Flask, render_template, url_for, flash, redirect, request
#from flask_behind_proxy import FlaskBehindProxy

sys.path.insert(0, '../model')
from GetAnswer import create_tables, insert_user, find_user, insert_question, get_history, get_answer, user_exists

app = Flask(__name__)
#proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = 'thisisasecretkey'
create_tables()


# App Home Page; Search bar and results
@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        answer = get_answer(request.form['question'])
        return render_template('home.html', subtitle='Home Page', text='This is the home page', answer=answer)
    return render_template('home.html', subtitle='Home Page', text='This is the home page')
   

# Page to register for an account
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        if user_exists(request.form['email']):
            flash('Account already exists for ' + request.form['email'])
            return redirect(url_for('login'))
        insert_user(request.form['email'], request.form['password'])
        flash('Account created for' + request.form['email'] + '!', 'success')
        global id
        id = find_user(request.form['email'], request.form['password'])
        return redirect(url_for('user'))
    return render_template('register.html', title='Register')

# User Home Page
@app.route("/user", methods=['GET', 'POST'])
def user_home():
    try:
        data = get_history(id)
    except:
        flash("You must be logged in to reach this page")
        return redirect(url_for('home'))
    if request.method == 'POST' and 'question' in request.form:
        answer = get_answer(request.form['question'])
        insert_question(id, request.form['question'], answer)
        return render_template('user-page.html', answer=answer, data=data)
    return render_template('user-page.html',  data=data)

    


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        if find_user(request.form['email'], request.form['password']) != False:
            global id
            id = find_user(request.form['email'], request.form['password'])
            return redirect(url_for('user'))
        else:
            flash(f'No account found for with the given email password')
            return redirect(url_for('home'))
    return render_template('login.html', title='Login')


@app.route("/user", methods=['GET', 'POST'])
def user():
    try:
        data = get_history(id)
    except:
        flash("You must be logged in to reach this page")
        return redirect(url_for('home'))
    if request.method == 'POST' and 'question' in request.form:
        answer = get_answer(request.form['question'])
        insert_question(id, request.form['question'], answer)
        return render_template('user.html', subtitle='User Page', text='This is your personal page', answer=answer, data=data)
    return render_template('user.html', subtitle='User Page', text='This your personal page', data=data)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")