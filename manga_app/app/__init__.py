from flask import Flask
from flask_login import LoginManager
from .routes import bp
from app.models import db, User

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'secret-key' # ログインに必要

    db.init_app(app)

    from app.routes import bp
    app.register_blueprint(bp)

    # ログインマネージャの設定
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "main.login"  # 未ログイン時のリダイレクト先

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app