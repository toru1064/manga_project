from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, Book, User, Like, Comment
from flask_login import login_user, logout_user, login_required, current_user

bp = Blueprint('main', __name__)

@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    error = None
    title = ""
    review = ""
    rating = ""

    if request.method == "POST":
        title = request.form["title"].strip()
        review = request.form["review"].strip()
        rating = request.form["rating"]

        # 入力チェック
        if not title or not review:
            error = "タイトルと感想は必須です。"
        elif not rating.isdigit() or not (1 <= int(rating) <= 5):
            error = "評価は1～5の数字で入力してください。"
        else:
            new_book = Book(title=title, review=review, rating=int(rating), user_id=current_user.id)
            db.session.add(new_book)
            db.session.commit()
            title = review = rating = ""

    # 検索・フィルター処理（現在のユーザーの投稿のみ表示）
    filter_option = request.args.get("filter", "")
    keyword = request.args.get("keyword", "")

    if filter_option == "my_posts":
        books = Book.query.filter_by(user_id=current_user.id).all()
    elif keyword:
        books = Book.query.filter(Book.title.contains(keyword)).order_by(Book.created_at.desc()).all()
    else:
        books = Book.query.order_by(Book.created_at.desc()).all()

    return render_template("index.html", posts=books, error=error,
                           input_title=title, input_review=review, input_rating=rating)

@bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):
    book = Book.query.get(id)
    if book and book.user_id == current_user.id:
        db.session.delete(book)
        db.session.commit()
    return redirect("/")

@bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    book = Book.query.get(id)
    if not book or book.user_id != current_user.id:
        return redirect("/")

    return render_template("edit.html", book=book)

@bp.route("/update/<int:id>", methods=["POST"])
@login_required
def update(id):
    book = Book.query.get(id)
    if book and book.user_id == current_user.id:
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

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))

from flask_login import login_required, current_user
from app.models import Like, Book, db

@bp.route("/like/<int:book_id>", methods=["POST"])
@login_required
def like(book_id):
    book = Book.query.get_or_404(book_id)

    # すでにいいねしていないか確認
    existing_like = Like.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    if not existing_like:
        new_like = Like(user_id=current_user.id, book_id=book_id)
        db.session.add(new_like)
        db.session.commit()

    return redirect(url_for('main.index'))

@bp.route("/unlike/<int:book_id>", methods=["POST"])
@login_required
def unlike(book_id):
    like = Like.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    if like:
        db.session.delete(like)
        db.session.commit()

    return redirect(url_for('main.index'))

@bp.route("/toggle_like/<int:book_id>", methods=["POST"])
@login_required
def toggle_like(book_id):
    book = Book.query.get_or_404(book_id)

    # すでにいいねしているかを確認
    existing_like = Like.query.filter_by(user_id=current_user.id, book_id=book.id).first()

    if existing_like:
        # いいねを取り消す
        db.session.delete(existing_like)
    else:
        # 新しくいいねする
        new_like = Like(user_id=current_user.id, book_id=book.id)
        db.session.add(new_like)

    db.session.commit()
    return redirect(url_for("main.index"))

@bp.route("/comment/<int:book_id>", methods=["POST"])
@login_required
def add_comment(book_id):
    content = request.form["content"].strip()
    if content:
        comment = Comment(content=content, user_id=current_user.id, book_id=book_id)
        db.session.add(comment)
        db.session.commit()
    return redirect(url_for("main.index"))

@bp.route("/comment/<int:comment_id>/delete", methods=["POST"])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    
    if comment.user_id != current_user.id:
        abort(403)  # 自分のコメント以外は削除できない

    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('main.index'))

@bp.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)

@bp.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    if request.method == "POST":
        bio = request.form.get("bio", "").strip()
        current_user.bio = bio
        db.session.commit()
        return redirect(url_for("main.profile"))

    return render_template("edit_profile.html", user=current_user)

@bp.route("/user/<int:user_id>")
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("profile.html", user=user)
