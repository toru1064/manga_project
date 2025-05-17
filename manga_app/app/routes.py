from flask import Blueprint, render_template, request
from app.models import db, Book

bp = Blueprint('main', __name__)

@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form["title"]
        review = request.form["review"]
        rating = request.form["rating"]

        #Bookモデルのインスタンスを作成して保存
        new_book = Book(title=title, review=review, rating=rating)
        db.session.add(new_book)
        db.session.commit()

    #データベースから全権取得
    books = Book.query.all()
    return render_template("index.html", posts=books)