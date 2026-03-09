from flask import Flask
from models import db, User
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from celery.schedules import crontab
from celery_app import celery_init_app


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


app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost:6379/0",
        result_backend="redis://localhost:6379/1",
        timezone="Asia/Kolkata",
        task_ignore_result=True,
    ),
)
celery_app = celery_init_app(app)

import celery_tasks

celery_app.conf.beat_schedule = {

    "daily-reminders": {
        "task": "celery_tasks.daily_reminder",
        "schedule": crontab(hour=10, minute=0),
    },

    "monthly-reports-companies": {
        "task": "celery_tasks.monthly_report_companies",
        "schedule": crontab( day_of_month=1, minute=0),
    },

    "monthly-report-admin":{
        "task": "celery_tasks.monthly_report_admin",
        "schedule": crontab( day_of_month=1, minute=0),
    }
}


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


