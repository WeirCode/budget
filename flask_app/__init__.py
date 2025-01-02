from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_caching import Cache
from flask_migrate import Migrate

from config import config
import os

load_dotenv()

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
cache = Cache()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    env = os.getenv('FLASK_ENV')
    app.config.from_object(config[env])
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    cache.init_app(app, config={'CACHE_TYPE': 'simple'})
    migrate_dir = app.config.get('MIGRATIONS_DIR')
    migrate.init_app(app, db, directory=migrate_dir)
    
    from flask_app.routes import user_bp
    
    app.register_blueprint(user_bp)
    
    login_manager.login_view = "user.login"
    
    from flask_app.models import User,Project,Item,Category
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    if os.getenv('FLASK_ENV') == 'production':
        @app.before_request
        def before_request():
        # Redirect all HTTP requests to HTTPS
            if not request.is_secure:
                url = request.url.replace("http://", "https://", 1)
                return redirect(url, code=301)
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    with app.app_context():
        db.create_all()

    return app