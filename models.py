from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# 👤 USER TABLE
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    resume_score = db.Column(db.String(20))

    # relationship (optional but good for structure)
    jobs = db.relationship('Job', backref='user', lazy=True)


# 💼 JOB TABLE
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    company = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(20), default="Medium")

    salary = db.Column(db.String(50))
    work_type = db.Column(db.String(50))
    location = db.Column(db.String(100))

    notes = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.now)

    # foreign key (better than plain integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)