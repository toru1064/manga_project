from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, Book, User
from flask_login import login_user

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

    #検索処理しデータベースから取得
    keyword = request.args.get("keyword", "")
    if keyword:
        books = Book.query.filter(Book.title.contains(keyword)).all()
    else:
        books = Book.query.all()

    return render_template("index.html", posts=books, error=error,
                           input_title=title, input_review=review, input_rating=rating)


@bp.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    book = Book.query.get(id)
    if book:
        db.session.delete(book)
        db.session.commit()
    return redirect("/")

@bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    book = Book.query.get(id)
    if not book:
        return redirect("/")

    return render_template("edit.html", book=book)

@bp.route("/update/<int:id>", methods=["POST"])
def update(id):
    book = Book.query.get(id)
    if book:
        book.title = request.form["title"]
        book.review = request.form["review"]
        book.rating = request.form["rating"]
        db.session.commit()
    return redirect(url_for("main.index"))

@bp.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        # 入力チェック
        if not username or not password:
            error = "すべての項目を入力してください。"
        elif User.query.filter_by(username=username).first():
            error = "このユーザー名は既に使われています。"
        else:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("main.login"))

    return render_template("register.html", error=error)

@bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("main.index"))
        else:
            error = "ユーザー名またはパスワードが正しくありません。"

    return render_template("login.html", error=error)