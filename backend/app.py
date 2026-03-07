from flask import Flask
from models import db, User
from flask_jwt_extended import JWTManager
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)
    return app

app = create_app()

app.config['JWT_SECRET_KEY'] = "super-secret"
jwt = JWTManager(app)

from routes import api, cache
api.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
cache.init_app(app)


if __name__ == "__main__":

    with app.app_context():

        db.create_all()

        admin = User.query.filter_by(email='admin@gmail.com').first()

        if not admin:
            admin = User(email='admin@gmail.com', password_hash='admin', role='admin')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created with email: admin@gmail.com and password: admin")
        else:
            print("Admin user already exists with email: admin@gmail.com and password: admin")

    app.run(debug=True)


