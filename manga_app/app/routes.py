from flask import Blueprint, render_templates, request

bp = Blueprint('main', __name__)

#投稿を一時的に保存（メモリ上）
post = []

@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form["title"]
        review = request.form["review"]
        rating = request.form["rating"]

        posts.append({
            "title": title,
            "review": review,
            "rating": rating
        })

    return render_templates("index.html", posts=posts)