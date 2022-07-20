from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy

app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = ''

# App Home Page; Search bar and results
@app.route("/")
def search():
    return render_template('home.html', subtitle='Home Page', text='This is the home page')
   
# Page to register for an account
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.email.data}!', 'success')
        return redirect(url_for('user-nav.html'))
    return render_template('register.html', title='Register', form=form)



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")