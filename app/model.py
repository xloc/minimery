from flask import json

from app import db
from util.timestamp_util import datetime_to_string

Column = db.Column


class Word(db.Model):
    __tablename__ = 'words'

    id = Column(db.Integer, primary_key=True)

    front = Column(db.String, nullable=False)
    back = Column(db.String, nullable=False)
    phonetic = Column(db.String)

    pronunciation = Column(db.Text)
    explanation = Column(db.Text)

    reviews = db.relationship(
        'Review',
        backref=db.backref('word'),
        lazy='dynamic'
    )

    def __eq__(self, other):
        if isinstance(other, Word):
            return self.id == other.id
        else:
            return False

    def to_json(self, simple=True):
        r = dict(id=self.id, front=self.front, back=self.back, phonetic=self.phonetic)
        if not simple:
            r.update(pronunciation=self.pronunciation, explanation=json.loads(self.explanation))
        return r

    @classmethod
    def get_by_id(cls, id) -> 'Word':
        return cls.query.filter_by(id=id).one_or_none()


class Review(db.Model):
    __tablename__ = 'reviews'

    id = Column(db.Integer,primary_key=True)
    word_id = Column(db.Integer, db.ForeignKey('words.id'), index=True)
    timestamp = Column(db.DateTime, nullable=False, index=True)

    familiarity = Column(db.Integer, nullable=False)

    def to_json(self):
        return dict(id=self.id, timestamp=datetime_to_string(self.timestamp), familarity=self.familiarity)

    @classmethod
    def get(cls, word_id):
        return cls.query.filter_by(word_id=word_id).order_by(cls.timestamp).all()


class WordInfo(db.Model):
    __tablename__ = 'word-info'

    word_id = Column(db.Integer, db.ForeignKey('words.id'), primary_key=True)
    overall_familiarity = Column(db.Float)
    is_learning = Column(db.Boolean, default=True)
    due = Column(db.DateTime)
    last_score = Column(db.Integer)

    @classmethod
    def get(cls, word_id):
        wi = cls.query.filter_by(word_id=word_id).one_or_none()
        if wi is None:
            wi = cls(word_id=word_id)
            db.session.add(wi)
            db.session.commit()
        return wi

    def to_json(self):
        return dict(
            is_learning=self.is_learning,
            due=self.due
        )


class AppInfo(db.Model):
    __tablename__ = 'app-info'

    name = Column(db.String, primary_key=True)
    value = Column(db.String)
