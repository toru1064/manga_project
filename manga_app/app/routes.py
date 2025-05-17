from flask import Blueprint, render_template, request
from app.models import db, Book

bp = Blueprint('main', __name__)

@bp.route("/", methods=["GET", "POST"])
def index():
    error = None
    title = ""
    review = ""
    rating = ""

    if request.method == "POST":
        title = request.form["title"].strip()
        review = request.form["review"].strip()
        rating = request.form["rating"]

        #入力チェック
        if not title or not review:
            error = "タイトルと感想は必須です。"
        elif not rating.isdigit() or not (1 <= int(rating) <= 5):
            error = "評価は1～5の数字で入力してください。"
        else:
            #Bookモデルのインスタンスを作成して保存
            new_book = Book(title=title, review=review, rating=int(rating))
            db.session.add(new_book)
            db.session.commit()
            title = ""
            review = ""
            rating = ""

    #データベースから全権取得
    books = Book.query.all()
    return render_template("index.html", posts=books, error=error,
                           input_title=title, input_review=review, input_rating=rating)