from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class StudentProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    full_name = db.Column(db.String(100))
    branch = db.Column(db.String(100))
    year = db.Column(db.Integer)
    cgpa = db.Column(db.Float)
    phone = db.Column(db.String(15))
    resume_path = db.Column(db.String(256))
    is_blacklisted = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref=db.backref('student_profile', uselist=False))


class CompanyProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    company_name = db.Column(db.String(150))
    hr_contact = db.Column(db.String(100))
    website = db.Column(db.String(200))
    description = db.Column(db.Text)
    approval_status = db.Column(db.String(20), default='pending')
    is_blacklisted = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref=db.backref('company_profile', uselist=False))


class PlacementDrive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company_profile.id'))
    drive_name = db.Column(db.String(150))
    job_title = db.Column(db.String(150))
    job_description = db.Column(db.Text)
    salary = db.Column(db.String(50))
    location = db.Column(db.String(100))
    eligiblility_criteria= db.Column(db.Text)
    application_deadline = db.Column(db.DateTime)
    interview_type = db.Column(db.String(50))
    status = db.Column(db.String(20), default='ongoing')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    company = db.relationship('CompanyProfile', backref='drives')


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profile.id'))
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drive.id'))
    applied_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String(20), default='applied')
    remark = db.Column(db.String(256))

    student = db.relationship('StudentProfile', backref='applications')
    drive = db.relationship('PlacementDrive', backref='applications')