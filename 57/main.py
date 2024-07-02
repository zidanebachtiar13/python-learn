from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def home():
    blog_url = 'https://api.npoint.io/c790b4d5cab58020d391'
    blog_response = requests.get(blog_url)
    blog_data = blog_response.json()
    return render_template('index.html', blogs=blog_data)

@app.route('/posts/<id>')
def posts(id):
    post_url = 'https://api.npoint.io/c790b4d5cab58020d391/' + id
    post_response = requests.get(post_url)
    post_data = post_response.json()
    return render_template('post.html', post=post_data)

if __name__ == '__main__':
    app.run(debug=True)
