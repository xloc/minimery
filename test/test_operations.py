from datetime import timedelta, datetime

from app.operations import query_words_whose_latest_review_satisfies
from test import TemplateTestCase

from app import db, create_app
from app.model import Word, WordInfo, Review


class TestWord(TemplateTestCase):

    def test_satisfies_query(self):
        # Prepare data
        def tick():
            t = datetime.now()
            while True:
                t += timedelta(seconds=1)
                yield t

        tt = tick()
        db.session.add_all([
            Review(word_id=1, familiarity=1, timestamp=tt.__next__()),

            Review(word_id=2, familiarity=1, timestamp=tt.__next__()),
            Review(word_id=2, familiarity=2, timestamp=tt.__next__()),
            Review(word_id=2, familiarity=2, timestamp=tt.__next__()),
            Review(word_id=2, familiarity=3, timestamp=tt.__next__()),

            Review(word_id=3, familiarity=2, timestamp=tt.__next__()),
            Review(word_id=3, familiarity=4, timestamp=tt.__next__()),
            Review(word_id=3, familiarity=3, timestamp=tt.__next__()),

            Review(word_id=4, familiarity=2, timestamp=tt.__next__()),
            Review(word_id=4, familiarity=4, timestamp=tt.__next__()),
            Review(word_id=4, familiarity=2, timestamp=tt.__next__()),
        ])

        # Trying
        # t = Review.query.order_by(Review.timestamp).group_by(Review.word_id).from_self(Word)\
        #     .filter(Review.word_id == Word.id, Review.familiarity < 3).all()

        words = query_words_whose_latest_review_satisfies(Review.familiarity <= 4).all()
        print(words)
        self.assertListEqual([w.id for w in words], [1, 2, 3, 4])

        words = query_words_whose_latest_review_satisfies(Review.familiarity <= 3).all()
        print(words)
        self.assertListEqual([w.id for w in words], [1, 2, 3, 4])

        words = query_words_whose_latest_review_satisfies(Review.familiarity <= 2).all()
        print(words)
        self.assertListEqual([w.id for w in words], [1, 4])

        words = query_words_whose_latest_review_satisfies(Review.familiarity <= 1).all()
        print(words)
        self.assertListEqual([w.id for w in words], [1])

    def test_need_review_words(self):
        pass

