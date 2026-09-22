from datetime import datetime
from datetime import timedelta
from datetime import timezone


class RevisionService:


    @staticmethod
    def calculate_priority(card):

        score = 0


        
        score += (
            5 - card.confidence
        ) * 10


        
        if card.last_reviewed_at is None:

            score += 20


        # Overdue cards receive extra priority
        if card.next_review_at is not None:

            now = datetime.now(
                timezone.utc
            )

            if card.next_review_at < now:

                score += 20


        return score


    @staticmethod
    def calculate_next_review(
        rating,
        review_time=None
    ):

        if review_time is None:

            review_time = datetime.now(
                timezone.utc
            )


        review_intervals = {
            0: 1,
            1: 1,
            2: 2,
            3: 4,
            4: 7,
            5: 14
        }


        days = review_intervals[
            rating
        ]


        return review_time + timedelta(
            days=days
        )