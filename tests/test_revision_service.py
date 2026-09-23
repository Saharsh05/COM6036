from datetime import datetime, timezone

from revisionService import RevisionService
import pytest

class FakeCard:

    def __init__(
        self,
        confidence,
        last_reviewed_at=None,
        next_review_at=None
    ):

        self.confidence = confidence

        self.last_reviewed_at = (
            last_reviewed_at
        )

        self.next_review_at = (
            next_review_at
        )


def test_low_confidence_has_higher_priority():

    weak_card = FakeCard(
        confidence=1,
        last_reviewed_at=datetime.now(
            timezone.utc
        )
    )

    strong_card = FakeCard(
        confidence=5,
        last_reviewed_at=datetime.now(
            timezone.utc
        )
    )

    weak_score = (
        RevisionService.calculate_priority(
            weak_card
        )
    )

    strong_score = (
        RevisionService.calculate_priority(
            strong_card
        )
    )

    assert weak_score > strong_score

def test_new_card_receives_extra_priority():

    new_card = FakeCard(
        confidence=3,
        last_reviewed_at=None
    )

    reviewed_card = FakeCard(
        confidence=3,
        last_reviewed_at=datetime.now(
            timezone.utc
        )
    )

    assert (
        RevisionService.calculate_priority(
            new_card
        )
        >
        RevisionService.calculate_priority(
            reviewed_card
        )
    )

def test_high_confidence_schedules_later_review():

    now = datetime.now(
        timezone.utc
    )

    weak_date = (
        RevisionService.calculate_next_review(
            1,
            now
        )
    )

    strong_date = (
        RevisionService.calculate_next_review(
            5,
            now
        )
    )

    assert strong_date > weak_date




def test_invalid_rating_raises_error():

    with pytest.raises(ValueError):

        RevisionService.calculate_next_review(
            8
        )