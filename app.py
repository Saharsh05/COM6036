import os
from datetime import datetime, timezone
from flask import Flask
from dotenv import load_dotenv
from sqlalchemy import text
from revisionService import RevisionService
from extensions import db, login_manager, csrf
from models import User
from models import Subject
from models import Flashcard
from models import ReviewLog
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

load_dotenv()


app = Flask(__name__)




app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


database_url = os.getenv("DATABASE_URL")


if database_url and database_url.startswith("postgresql://"):
    database_url = database_url.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1
    )


app.config["SQLALCHEMY_DATABASE_URI"] = database_url

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False



db.init_app(app)

login_manager.init_app(app)

csrf.init_app(app)


login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):

    return db.session.get(
        User,
        int(user_id)
    )

# @app.route("/database-test")
# def database_test():

#     try:
#         db.session.execute(text("SELECT 1"))

#         return "Database connection successful!"

#     except Exception as error:

#         return f"Database connection failed: {error}"
@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if current_user.is_authenticated:

        return redirect(
            url_for("dashboard")
        )


    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )


        if not email:

            flash("Please enter an email address.")

            return redirect(
                url_for("register")
            )


        if len(password) < 10:

            flash(
                "Password must contain at least 10 characters."
            )

            return redirect(
                url_for("register")
            )


        existing_user = User.query.filter_by(
            email=email
        ).first()


        if existing_user:

            flash(
                "An account already exists with that email."
            )

            return redirect(
                url_for("register")
            )


        user = User(
            email=email
        )

        user.set_password(
            password
        )


        db.session.add(
            user
        )

        db.session.commit()


        login_user(
            user
        )


        return redirect(
            url_for("dashboard")
        )


    return render_template(
        "register.html"
    )

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if current_user.is_authenticated:

        return redirect(
            url_for("dashboard")
        )


    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )


        user = User.query.filter_by(
            email=email
        ).first()


        if user and user.check_password(password):

            login_user(
                user
            )

            return redirect(
                url_for("dashboard")
            )


        flash(
            "Incorrect email or password."
        )


    return render_template(
        "login.html"
    )

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("login")
    )
@app.route(
    "/subjects/new",
    methods=["GET", "POST"]
)
@login_required
def create_subject():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()


        if not name:

            flash(
                "Please enter a subject name."
            )

            return redirect(
                url_for("create_subject")
            )


        subject = Subject(
            name=name,
            user_id=current_user.id
        )


        db.session.add(
            subject
        )

        db.session.commit()


        return redirect(
            url_for("dashboard")
        )


    return render_template(
        "createSubject.html"
    )
@app.route(
    "/flashcards/new",
    methods=["GET", "POST"]
)
@login_required
def create_flashcard():

    subjects = Subject.query.filter_by(
        user_id=current_user.id
    ).all()


    if request.method == "POST":

        question = request.form.get(
            "question",
            ""
        ).strip()

        answer = request.form.get(
            "answer",
            ""
        ).strip()

        subject_id = request.form.get(
            "subject_id",
            type=int
        )


        subject = Subject.query.filter_by(
            id=subject_id,
            user_id=current_user.id
        ).first()


        if not subject:

            flash(
                "Invalid subject."
            )

            return redirect(
                url_for("create_flashcard")
            )


        if not question or not answer:

            flash(
                "Question and answer are required."
            )

            return redirect(
                url_for("create_flashcard")
            )


        card = Flashcard(
            question=question,
            answer=answer,
            subject_id=subject.id,
            user_id=current_user.id
        )


        db.session.add(
            card
        )

        db.session.commit()


        return redirect(
            url_for("dashboard")
        )


    return render_template(
        "createFlashcard.html",
        subjects=subjects
    )
@app.route("/dashboard")
@login_required
def dashboard():

    cards = Flashcard.query.filter_by(
        user_id=current_user.id
    ).all()


    ranked_cards = []


    for card in cards:

        priority = (
            RevisionService.calculate_priority(
                card
            )
        )

        ranked_cards.append(
            {
                "card": card,
                "priority": priority
            }
        )


    ranked_cards.sort(
        key=lambda item: item["priority"],
        reverse=True
    )


    return render_template(
        "dashboard.html",
        ranked_cards=ranked_cards
    )
@app.route(
    "/flashcards/<int:card_id>/review",
    methods=["GET", "POST"]
)
@login_required
def review_flashcard(card_id):

    card = Flashcard.query.filter_by(
        id=card_id,
        user_id=current_user.id
    ).first_or_404()

    if request.method == "POST":

        rating = request.form.get(
            "rating",
            type=int
        )

        if rating not in range(0, 6):
            flash(
                "Confidence rating must be between 0 and 5."
            )

            return redirect(
                url_for(
                    "review_flashcard",
                    card_id=card.id
                )
            )

        now = datetime.now(timezone.utc)

        card.confidence = rating
        card.last_reviewed_at = now

        card.next_review_at = (
            RevisionService.calculate_next_review(
                rating,
                now
            )
        )

        review_log = ReviewLog(
            flashcard_id=card.id,
            rating=rating,
            reviewed_at=now
        )

        db.session.add(review_log)

        db.session.commit()

        flash("Review recorded successfully.")

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "review.html",
        card=card
    )

@app.route("/flashcards")
@login_required
def flashcards():

    search = request.args.get(
        "search",
        ""
    ).strip()

    query = Flashcard.query.filter_by(
        user_id=current_user.id
    )

    if search:

        query = query.filter(
            Flashcard.question.ilike(
                f"%{search}%"
            )
        )

    cards = query.order_by(
        Flashcard.created_at.desc()
    ).all()

    return render_template(
        "flashcards.html",
        cards=cards,
        search=search
    )
@app.route(
    "/flashcards/<int:card_id>/edit",
    methods=["GET", "POST"]
)
@login_required
def edit_flashcard(card_id):

    card = Flashcard.query.filter_by(
        id=card_id,
        user_id=current_user.id
    ).first_or_404()

    subjects = Subject.query.filter_by(
        user_id=current_user.id
    ).all()

    if request.method == "POST":

        question = request.form.get(
            "question",
            ""
        ).strip()

        answer = request.form.get(
            "answer",
            ""
        ).strip()

        subject_id = request.form.get(
            "subject_id",
            type=int
        )

        subject = Subject.query.filter_by(
            id=subject_id,
            user_id=current_user.id
        ).first()

        if not question or not answer:
            flash(
                "Question and answer are required."
            )

            return redirect(
                url_for(
                    "edit_flashcard",
                    card_id=card.id
                )
            )

        if not subject:
            flash("Invalid subject.")

            return redirect(
                url_for(
                    "edit_flashcard",
                    card_id=card.id
                )
            )

        card.question = question
        card.answer = answer
        card.subject_id = subject.id

        db.session.commit()

        flash("Flashcard updated.")

        return redirect(
            url_for("flashcards")
        )

    return render_template(
        "edit_flashcard.html",
        card=card,
        subjects=subjects
    )
@app.route(
    "/flashcards/<int:card_id>/delete",
    methods=["POST"]
)
@login_required
def delete_flashcard(card_id):

    card = Flashcard.query.filter_by(
        id=card_id,
        user_id=current_user.id
    ).first_or_404()

    ReviewLog.query.filter_by(
        flashcard_id=card.id
    ).delete()

    db.session.delete(card)

    db.session.commit()

    flash("Flashcard deleted.")

    return redirect(
        url_for("flashcards")
    )
if __name__ == "__main__":
    app.run(debug=True)