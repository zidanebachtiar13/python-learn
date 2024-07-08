from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'

db.init_app(app)

class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

with app.app_context():
    db.create_all()

'''
with app.app_context():
    new_book = Book(id=1, title='Harry Potter', author='J. K. Rowling', rating=9.3)
    db.session.add(new_book)
    db.session.commit()
'''

@app.route('/')
def home():
    books = db.session.execute(db.select(Book).order_by(Book.title)).scalars()
    return render_template('index.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_book = Book(title=request.form['book_name'],
                        author=request.form['book_author'],
                        rating=request.form['rating'])
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route('/edit')
def edit():
    id = request.args.get('id')
    book = db.session.execute(db.select(Book).where(Book.id == id)).scalar()
    return render_template('edit.html', book=book)

if __name__ == '__main__':
    app.run(debug=True)
