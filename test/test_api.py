import json
from unittest import TestCase, mock
from datetime import datetime, timedelta

from flask import url_for

import app.api
from app import create_app, db
from app.model import Review, WordInfo, Word
from test import TemplateTestCase
from util.timestamp_util import datetime_to_string


class TestAPI(TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def req(self, url, son):
        return self.client.post(url, json=son).get_json()

    def test_request(self):
        r = self.req('/api/get_words', {})
        self.assertIn('status', r)
        self.assertEqual(r['status'], 'ok')

    def test_get_cards_limit(self):
        def req(**kwargs):
            return self.req('/api/get_words', kwargs)['data']

        self.assertEqual(len(req(limit=10)), 10)
        self.assertEqual(len(req(limit=27)), 27)

        self.assertListEqual(
            'abandon abase abash abate abbreviate abdicate aberrant abet abeyance abhor'.split(),
            [w['front'] for w in req(limit=10)])

        self.assertEqual(self.req('/api/get_words', dict(limit=10))['total'], 100)

    def test_get_cards_offset(self):
        def req(**kwargs):
            return self.req('/api/get_words', kwargs)['data']

        # print(' '.join([w['front'] for w in req(limit=10, offset=20)]))

        all = req(limit=30)
        l = req(limit=12)
        r = req(limit=18, offset=12)
        self.assertListEqual(l+r, all)

    def test_get_words_by_ids(self):
        r = self.req('/api/get_words_by_ids', dict(ids=[1,2,3]))
        self.assertEqual(len(r['data']), 3)
        self.assertEqual([w['front'] for w in r['data']], ['abandon', 'abase', 'abash'])

    def test_add_review(self):
        now = datetime.now()
        r = self.req('/api/add_review', dict(word_id=1, familiarity=2, timestamp=datetime_to_string(now)))
        r = self.req('/api/add_review', dict(word_id=1, familiarity=3, timestamp=datetime_to_string(now)))
        r = self.req('/api/add_review', dict(word_id=1, familiarity=4, timestamp=datetime_to_string(now)))

        rs = Review.query.filter_by(word_id=1).all()
        self.assertEqual(len(rs), 3)
        self.assertListEqual([r.familiarity for r in rs], [2,3,4])

    def test_get_review(self):
        self.assertEqual(self.req('/api/get_reviews', {'word_id':0})['data'], [])

        now = datetime.now()
        for i in range(5):
            db.session.add(Review(word_id=0, familiarity=5, timestamp=now+i*timedelta(seconds=1)))
        db.session.commit()

        r = self.req('/api/get_reviews', {'word_id':0})['data']
        self.assertEqual(len(r), 5)

    def test_get_overall_familiarity(self):
        now = datetime.now()
        for i in range(10):
            db.session.add(Review(word_id=1, familiarity=2, timestamp=now+i*timedelta(seconds=1)))
        for i in range(10, 20):
            db.session.add(Review(word_id=1, familiarity=5, timestamp=now+i*timedelta(seconds=1)))
        db.session.commit()

        r = self.req('/api/get_overall_familiarity', dict(word_id=1))
        self.assertEqual(r['overall_familiarity'], 5.0)

    def prepare_data_1(self):
        tt = tick()
        [WordInfo.get(i) for i in range(27)]
        db.session.add_all(
            [Review(word_id=i, familiarity=1, timestamp=tt.__next__()) for i in range(27)] +
            [Review(word_id=i, familiarity=2, timestamp=tt.__next__()) for i in range(5)] +
            [Review(word_id=i, familiarity=4, timestamp=tt.__next__()) for i in range(3)]
        )
        db.session.commit()

    def limit_offset(self, url, **args):
        def update(**kwargs):
            a = dict(args)
            a.update(kwargs)
            return a

        rl = self.req(url, update(limit=11))['data']
        rr = self.req(url, update(limit=10, offset=11))['data']
        r = self.req(url, update(limit=21))['data']

        self.assertEqual(len(rl), 11)
        self.assertEqual(len(rr), 10)

        self.assertEqual(r, rl+rr)

    def test_get_learning_words_limit_offset(self):
        self.prepare_data_1()
        self.limit_offset('/api/get_learning_words')

    def test_get_today_reviewed_word_ids(self):
        now = datetime.now()
        db.session.add(Review(word_id=1, familiarity=2, timestamp=now + timedelta(days=-1, seconds=1)))
        db.session.add(Review(word_id=2, familiarity=2, timestamp=now + timedelta(days=-1, seconds=2)))
        db.session.add(Review(word_id=3, familiarity=2, timestamp=now + timedelta(days=-1, seconds=3)))
        db.session.add(Review(word_id=1, familiarity=2, timestamp=now + timedelta(seconds=1)))
        db.session.add(Review(word_id=2, familiarity=2, timestamp=now + timedelta(seconds=2)))
        db.session.add(Review(word_id=2, familiarity=2, timestamp=now + timedelta(seconds=3)))
        db.session.commit()

        ids = self.req('/api/get_today_reviewed_word_ids', {})
        self.assertEqual(ids['data'], [1, 2])


def tick():
    now = datetime.now()
    i = 0
    while True:
        i += 1
        yield now + timedelta(seconds=i)





