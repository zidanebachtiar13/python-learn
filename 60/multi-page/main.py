from flask import Flask, render_template
import requests


app = Flask(__name__)

@app.route('/')
def home():
    blogs = requests.get('https://api.npoint.io/1533435fde6c79cbc9ca').json()
    return render_template('index.html', blogs=blogs)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/post/<id>')
def post(id):
    post = requests.get('https://api.npoint.io/1533435fde6c79cbc9ca/' + id).json()
    return render_template('post.html', post=post)

@app.route('/form-entry')
def receive_data():
    return

if __name__ == '__main__':
    app.run(debug=True)
