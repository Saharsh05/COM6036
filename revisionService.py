from datetime import datetime, timedelta, timezone

# Scoring and scheduling logic for the spaced-repetition system.
class RevisionService:

    @staticmethod
    def calculate_priority(card):
        # Higher scores mean the card should be reviewed sooner.
        score = 0

        score += (5 - card.confidence) * 10

        if card.last_reviewed_at is None:
            score += 20

        
        if card.next_review_at is not None:
            now = datetime.now(timezone.utc)

            next_review = card.next_review_at

            if next_review.tzinfo is None:
                next_review = next_review.replace(
                    tzinfo=timezone.utc
                )

            if next_review < now:
                score += 20

        return score


    @staticmethod
    def calculate_next_review(rating, review_time=None):
        # Map rating to the number of days until the next review.

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
    @staticmethod
    def priority_label(score):

        if score >= 60:
            return "High"

        if score >= 30:
            return "Medium"

        return "Low"
    @staticmethod
    def priority_reasons(card):

        reasons = []

        if card.confidence <= 2:
            reasons.append(
                "low confidence"
            )

        if card.last_reviewed_at is None:
            reasons.append(
                "not reviewed yet"
            )

        if card.next_review_at is not None:

            now = datetime.now(timezone.utc)

            next_review = card.next_review_at

            if next_review.tzinfo is None:
                next_review = next_review.replace(
                    tzinfo=timezone.utc
                )

            if next_review < now:
                reasons.append(
                    "review overdue"
                )

        if not reasons:
            reasons.append(
                "routine revision"
            )

        return reasons