from flask import Flask, render_template, request
import requests


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
        return render_template('contact.html', msg_sent=True)

@app.route('/post/<id>')
def post(id):
    post = requests.get('https://api.npoint.io/1533435fde6c79cbc9ca/' + id).json()
    return render_template('post.html', post=post)

if __name__ == '__main__':
    app.run(debug=True)
