from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap4
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired
import email_validator

class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[validators.Email()])
    password = PasswordField(label='Password', validators=[validators.length(min=8)])
    submit = SubmitField(label='Log In')

app = Flask(__name__)
app.secret_key = 'c29neW8gbW9neW8K'

bootstrap = Bootstrap4(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if login_form.email.data == 'admin@email.com' and login_form.password.data == '12345678':
            return render_template('success.html')
        else:
            return render_template('denied.html')
    return render_template('login.html', form=login_form)

if __name__ == '__main__':
    app.run(debug=True)
