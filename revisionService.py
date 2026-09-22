from datetime import datetime, timedelta, timezone


class RevisionService:

    @staticmethod
    def calculate_priority(card):
        score = 0

        # Lower confidence = higher priority
        score += (5 - card.confidence) * 10

        # Brand new cards should be reviewed
        if card.last_reviewed_at is None:
            score += 20

        # Overdue cards get extra priority
        if card.next_review_at is not None:
            now = datetime.now(timezone.utc)

            next_review = card.next_review_at

            # PostgreSQL may sometimes return a value
            # without timezone information.
            if next_review.tzinfo is None:
                next_review = next_review.replace(
                    tzinfo=timezone.utc
                )

            if next_review < now:
                score += 20

        return score


    @staticmethod
    def calculate_next_review(rating, review_time=None):

        if review_time is None:
            review_time = datetime.now(timezone.utc)

        intervals = {
            0: 1,
            1: 1,
            2: 2,
            3: 4,
            4: 7,
            5: 14
        }

        if rating not in intervals:
            raise ValueError(
                "Rating must be between 0 and 5."
            )

        return review_time + timedelta(
            days=intervals[rating]
        )