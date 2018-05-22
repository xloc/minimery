from datetime import datetime, timedelta
from itertools import count
from random import randint

from app import db
from app.learning import calculate_space_interval, add_review, get_review_word_ids
from app.model import WordInfo, Review
from test import TemplateTestCase


class TestLearning(TemplateTestCase):
    def fake_reviews(self, word_id, days_of_scores):
        now = datetime.now()
        tick = count()

        def review_factory(score, day):
            return Review(word_id=word_id, familiarity=score,
                          timestamp=now+timedelta(days=day, seconds=10*tick.__next__()))

        # if there is only one day, -1 + 1 = 0
        day_delta = -len(days_of_scores) + 1
        for ss in days_of_scores:
            for s in ss:
                db.session.add(review_factory(s, day_delta))

            day_delta += 1
        db.session.commit()

    def test_calculate_space_interval(self):
        # self.fake_reviews(1, [[i] for i in [6, 6, 2]])
        self.fake_reviews(1, [
            [1, 2, 4],
            [1, 4],
            [1, 3]
        ])

        interval = calculate_space_interval(word_id=1)
        print(interval)

    def test_tryings(self):
        self.fake_reviews(1, [
            [1, 2, 4],
            [1, 4],
            [1, 3]
        ])

        query = Review.query.filter_by(word_id=1).order_by(Review.timestamp).\
        from_self().group_by(db.func.date(Review.timestamp, "start of day"))

        print(query.as_scalar())
        for rw in query.all():
            print(rw.familiarity)

        # q = db.session.execute("select id, word_id, familiarity, timestamp, date(timestamp, 'start of day') as day "
        #                        "from reviews group by day order by reviews.timestamp desc")
        # for i in q:
        #     print(i)

    def test_get_review_word_ids(self):
        def fake_reviews(word_id, days_of_scores):
            now = datetime.now()
            tick = count()

            # if there is only one day, -1 + 1 = 0
            day_delta = -len(days_of_scores) + 1
            for ss in days_of_scores:
                for s in ss:
                    add_review(word_id=word_id, familiarity=s,
                               timestamp=now + timedelta(days=day_delta, seconds=10 * tick.__next__()))

                day_delta += 1

        fake_reviews(1, [[1, 1, 1], [2, 1, 2]])

        words = get_review_word_ids()
        for w in words:
            print(w)




