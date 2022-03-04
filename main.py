from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# all_books = []

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), unique=True, nullable=False)
    rating = db.Column(db.Float, nullable=False)


# create dB
# db.create_all()
all_books = Book.query.all()
print(all_books)


@app.route('/')
def home():
    if not all_books:
        message = "Library is empty."
        check = True
        return render_template('index.html', message=message, check=check)
    else:
        check_books = Book.query.all()
        return render_template('index.html', message=check_books)


@app.route("/add")
def add():
    return render_template('add.html')


@app.route("/datas", methods=["GET", "POST"])
def to_data():
    if request.method == "POST":
        data = request.form
        # books = {"title": data['title'],
        #          "author": data['author'],
        #          "rating": data['rating'],
        #
        #          }

        # all_books.append(books)
        db.session.add(Book(title=data['title'], author=data['author'], rating=data['rating']))
        db.session.commit()

    return redirect(url_for('home'))


@app.route("/change/<int:number>", methods=["GET", "POST"])
def update(number):
    if request.method == "POST":
        print(number)
        new_rating = request.form
        rating_to_update = Book.query.get(number)
        print(rating_to_update)
        rating_to_update.rating = new_rating['new_rating']
        db.session.commit()

    return redirect(url_for('home'))


@app.route("/edit/<int:number>")
def edit(number):
    record = Book.query.filter_by(id=number).first()
    return render_template('edit.html', number=number, record=record)


if __name__ == "__main__":
    app.run(debug=True)
