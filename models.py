from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from extensions import db


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    def set_password(self, password):

        self.password_hash = generate_password_hash(
            password
        )

    def check_password(self, password):

        return check_password_hash(
            self.password_hash,
            password
        )

class Subject(db.Model):

    __tablename__ = "subjects"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(120),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    user = db.relationship(
        "User",
        backref="subjects"
    )

class Flashcard(db.Model):

    __tablename__ = "flashcards"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    question = db.Column(
        db.String(500),
        nullable=False
    )

    answer = db.Column(
        db.Text,
        nullable=False
    )

    confidence = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    last_reviewed_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True
    )

    next_review_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    subject_id = db.Column(
        db.Integer,
        db.ForeignKey("subjects.id"),
        nullable=False
    )

    user = db.relationship(
        "User",
        backref="flashcards"
    )

    subject = db.relationship(
        "Subject",
        backref="flashcards"
    )

class ReviewLog(db.Model):

    __tablename__ = "review_logs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    rating = db.Column(
        db.Integer,
        nullable=False
    )

    reviewed_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    flashcard_id = db.Column(
        db.Integer,
        db.ForeignKey("flashcards.id"),
        nullable=False
    )

    flashcard = db.relationship(
        "Flashcard",
        backref="reviews"
    )