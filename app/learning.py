from itertools import count

from datetime import datetime, timedelta

from app import db, model
from app.model import Review, Word, WordInfo


def add_review(word_id, familiarity, timestamp):
    wi = model.WordInfo.get(word_id)
    # Implicitly start learning if is not learning
    if not wi.is_learning:
        wi.is_learning = True
        print("Implicit start learning")
        db.session.add(wi)

    # Add review
    rv = Review(word_id=word_id, familiarity=familiarity, timestamp=timestamp)
    db.session.add(rv)

    # Update due
    days = calculate_space_interval(word_id=word_id)
    wi.due = datetime.now() + timedelta(days=days)

    # Update last_score
    wi.last_score = familiarity

    db.session.add(wi)
    db.session.commit()


def calculate_space_interval(word_id, from_scratch=False):
    w = Word.get_by_id(word_id)
    wi = WordInfo.get(word_id)

    query = Review.query.filter_by(word_id=word_id).order_by(Review.timestamp)

    reviews = []
    date = None
    for rv in query.all():
        if date != rv.timestamp.date():
            date = rv.timestamp.date()
            reviews.append(rv)

    # todo: differentiate algorithm for whether from scratch

    smi_i = count(1)
    ef = 2.5
    period = None
    for rv in reviews:
        # Update ef
        q = rv.familiarity
        ef += 0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)
        if ef < 1.3:
            ef = 1.3

        # Calculate period
        if rv.familiarity < 3:
            smi_i = count(1)

        sm_i = smi_i.__next__()
        if sm_i == 1:
            period = 1
        elif sm_i == 2:
            period = 6
        else:
            period = period * ef

    return round(period)


def get_review_word_ids():
    q = Word.query.join(WordInfo).filter(db.or_(WordInfo.last_score < 4, WordInfo.last_score == None), WordInfo.is_learning)
    low_score_words = q.all()
    low_score_words_ids = {w.id for w in low_score_words}

    # fixme: the time standard
    q = WordInfo.query.filter(WordInfo.due < datetime.now())
    due_words = q.all()
    due_words_ids = {w.word_id for w in due_words}

    return list(low_score_words_ids | due_words_ids)







