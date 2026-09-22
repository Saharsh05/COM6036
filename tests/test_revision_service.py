from revisionService import RevisionService


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


def test_weak_card_has_higher_priority():

    weak_card = FakeCard(
        confidence=1
    )

    strong_card = FakeCard(
        confidence=5
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