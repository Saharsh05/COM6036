from extensions import db
from models import User, Subject, Flashcard

def test_dashboard_requires_login(client):

    response = client.get(
        "/dashboard",
        follow_redirects=False
    )

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]

def test_user_cannot_access_another_users_flashcard(client):

    with client.application.app_context():

        user_a = User(
            email="usera@example.com"
        )

        user_a.set_password(
            "Password123"
        )

        user_b = User(
            email="userb@example.com"
        )

        user_b.set_password(
            "Password123"
        )

        db.session.add_all([
            user_a,
            user_b
        ])

        db.session.commit()

        subject = Subject(
            name="Private Subject",
            user_id=user_a.id
        )

        db.session.add(subject)
        db.session.commit()

        card = Flashcard(
            question="Private question",
            answer="Private answer",
            subject_id=subject.id,
            user_id=user_a.id
        )

        db.session.add(card)
        db.session.commit()

        card_id = card.id



    client.post(
        "/login",
        data={
            "email": "userb@example.com",
            "password": "Password123"
        }
    )



    response = client.get(
        f"/flashcards/{card_id}/edit"
    )

    assert response.status_code == 404

def test_duplicate_subject_is_rejected(client):

    client.post(
        "/register",
        data={
            "email": "test@example.com",
            "password": "Password123"
        }
    )

    client.post(
        "/subjects/new",
        data={
            "name": "Maths"
        }
    )

    response = client.post(
        "/subjects/new",
        data={
            "name": "Maths"
        },
        follow_redirects=True
    )

    with client.application.app_context():

        subjects = Subject.query.filter_by(
            name="Maths"
        ).all()

        assert len(subjects) == 1

    assert b"You already have a subject with that name." in response.data