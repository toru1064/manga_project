from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, Book, User, Like, Comment
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_
import requests
import os
import boto3

bp = Blueprint('main', __name__)

s3 = boto3.client(
    "s3",
    region_name="ap-northeast-1"
)

S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")

@bp.route("/", methods=["GET"])
@login_required
def index():

    # 検索・フィルターの条件を取得
    filter_option = request.args.get("filter", "")
    keyword = request.args.get("keyword", "")
    page = request.args.get("page", 1, type=int)

    # 自分の投稿だけ表示
    if filter_option == "my_posts":
        pagination = Book.query.filter_by(
            user_id=current_user.id
        ).order_by(
            Book.created_at.desc()
        ).paginate(
            page=page,
            per_page=5,
            error_out=False
        )

    # キーワード検索
    elif keyword:
        pagination = Book.query.filter(
            or_(
                Book.title.contains(keyword),
                Book.review.contains(keyword)
            )
        ).order_by(
            Book.created_at.desc()
        ).paginate(
            page=page,
            per_page=5,
            error_out=False
        )

    # すべての投稿を表示
    else:
        pagination = Book.query.order_by(
            Book.created_at.desc()
        ).paginate(
            page=page,
            per_page=5,
            error_out=False
        )

    # 投稿一覧画面を表示
    return render_template(
        "index.html",
        posts=pagination.items,
        pagination=pagination
    )

@bp.route("/create", methods=["GET", "POST"])
@login_required
def create_post():
    error = None

    # 検索画面から選択された漫画情報を受け取る
    title = request.args.get("title", "")
    author = request.args.get("author", "")
    thumbnail = request.args.get("thumbnail", "")

    review = ""
    rating = ""

    # 投稿ボタンが押されたとき
    if request.method == "POST":
        title = request.form["title"].strip()
        review = request.form["review"].strip()
        rating = request.form["rating"]
        author = request.form.get("author") or request.args.get("author", "")
        thumbnail = request.form.get("thumbnail") or request.args.get("thumbnail", "")

        # 入力内容をチェック
        if not title or not review:
            error = "タイトルと感想は必須です。"

        elif not rating.isdigit() or not (1 <= int(rating) <= 5):
            error = "評価は1～5の数字で入力してください。"

        # 問題なければDBへ保存
        else:
            new_book = Book(
                title=title,
                author=author,
                thumbnail=thumbnail,
                review=review,
                rating=int(rating),
                user_id=current_user.id
            )

            db.session.add(new_book)
            db.session.commit()

            # 投稿後はホームへ戻る
            return redirect(url_for("main.index"))

    # 投稿画面を表示
    return render_template(
        "create_post.html",
        error=error,
        input_title=title,
        input_author=author,
        input_thumbnail=thumbnail,
        input_review=review,
        input_rating=rating
    )

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
    profile_image_url = None

    if current_user.profile_image:
        profile_image_url = s3.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": S3_BUCKET_NAME,
                "Key": current_user.profile_image
            },
            ExpiresIn=3600
        )

    return render_template(
        "profile.html",
        user=current_user,
        profile_image_url=profile_image_url
    )

from flask import current_app
import os

@bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        display_name = request.form.get('display_name')
        bio = request.form.get('bio')
        image = request.files.get('profile_image')

        current_user.display_name = display_name
        current_user.bio = bio

        # 画像の保存処理（ファイル名を user_id に基づいて保存）
        if image and image.filename != '':
            filename = f'user_{current_user.id}.png'
            #S3にアップロード
            s3.upload_fileobj(
                image,
                S3_BUCKET_NAME,
                filename,
                ExtraArgs={"ContentType": image.content_type}
            )
            current_user.profile_image = filename

        db.session.commit()
        return redirect(url_for('main.profile', user_id=current_user.id))

    return render_template('edit_profile.html', user=current_user)

@bp.route("/user/<int:user_id>")
def user_profile(user_id):
    user = User.query.get_or_404(user_id)

    profile_image_url = None

    if user.profile_image:
        profile_image_url = s3.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": S3_BUCKET_NAME,
                "Key": user.profile_image
            },
            ExpiresIn=3600
        )

    return render_template(
        "profile.html",
        user=user,
        profile_image_url=profile_image_url
    )

@bp.route("/ranking")
@login_required
def ranking():
    books = Book.query.all()
    books = sorted(books, key=lambda book: book.likes.count(), reverse=True)
    return render_template("ranking.html", books=books)

@bp.route("/rating_ranking")
@login_required
def rating_ranking():
    books = Book.query.order_by(Book.rating.desc()).all()
    return render_template("rating_ranking.html", books=books)

@bp.route("/manga/search")
def manga_search():
    keyword = request.args.get("keyword")
    books = []
    error = None

    if keyword:
        url = "https://www.googleapis.com/books/v1/volumes"
        params = {
            "q": f"intitle:{keyword}",
            "maxResults": 10,
            "langRestrict": "ja",
            "key": os.environ.get("GOOGLE_BOOKS_API_KEY")
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()

            for item in data.get("items", []):
                volume_info = item.get("volumeInfo", {})

                title = volume_info.get("title", "タイトル不明")
                authors = volume_info.get("authors", ["著者不明"])
                description = volume_info.get("description", "")
                image_links = volume_info.get("imageLinks", {})
                thumbnail = image_links.get("thumbnail")

                books.append({
                    "title": title,
                    "authors": ", ".join(authors),
                    "description": description,
                    "thumbnail": thumbnail
                })

        elif response.status_code == 429:
            error = "Google Books APIの利用上限に達しました。時間をおいて再度検索してください。"

        else:
            error = "漫画情報の取得中にエラーが発生しました。"

    return render_template(
        "manga_search.html",
        books=books,
        keyword=keyword,
        error=error
    )