from flask import Flask, render_template, request
import requests
import smtplib

account = open('account.txt', 'r')
my_account = []

for acc in account:
    my_account.append(acc)

email = my_account[0][:-1]
password = my_account[1][:-1]

app = Flask(__name__)

@app.route('/')
def home():
    blogs = requests.get('https://api.npoint.io/1533435fde6c79cbc9ca').json()
    return render_template('index.html', blogs=blogs)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        return render_template('contact.html', msg_sent=False)
    elif request.method == 'POST':
        name = request.form['name']
        mail = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=email, password=password)
            connection.sendmail(
                    from_addr=email,
                    to_addrs=email,
                    msg='Subject:Message From Your Blog\n\nName: ' + name + '\nEmail: ' + mail + '\nPhone: ' + phone + '\nMessage: ' + message
                    )
        return render_template('contact.html', msg_sent=True)

@app.route('/post/<id>')
def post(id):
    post = requests.get('https://api.npoint.io/1533435fde6c79cbc9ca/' + id).json()
    return render_template('post.html', post=post)

if __name__ == '__main__':
    app.run(debug=True)
