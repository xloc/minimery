from datetime import datetime

from flask import Blueprint, request, jsonify
from sqlalchemy import func

from app import db, learning
from app.model import Word, Review, WordInfo
from util import json_check
from util.timestamp_util import datetime_from_string

api = Blueprint("api", __name__)


@api.route('get_words', methods=['POST'])
def get_words():
    # print(request.get_data())
    d = dict(request.json)

    limit = d.get('limit', 30)
    offset = d.get('offset', 0)

    q = Word.query.order_by(Word.id)

    words = q.limit(limit).offset(offset).all()
    words_json = [w.to_json() for w in words]
    return jsonify({'status': 'ok', 'data': words_json, 'total': q.count()})


@api.route('get_words_by_ids', methods=['POST'])
def get_words_by_ids():
    ids, = json_check.check_fields(request.json, 'ids')

    words_json = []
    for id in ids:
        word = Word.query.filter_by(id=id).one()
        j = word.to_json()
        word_info = WordInfo.get(id)
        j.update(word_info.to_json())
        words_json.append(j)

    return jsonify(status='ok', data=words_json)


@api.route('add_review', methods=['POST'])
def add_review():
    word_id, familiarity, timestamp = \
        json_check.check_fields(request.json, 'word_id, familiarity, timestamp')

    learning.add_review(word_id, familiarity, datetime_from_string(timestamp))
    return jsonify({'status': 'ok'})


@api.route('get_reviews', methods=['POST'])
def get_reviews():
    word_id, = json_check.check_fields(request.json, 'word_id')
    reviews = Review.query.filter_by(word_id=word_id).all()
    return jsonify(data=[r.to_json() for r in reviews])


@api.route('get_overall_familiarity', methods=['POST'])
def get_overall_familiarity():
    word_id, = json_check.check_fields(request.json, 'word_id')
    reviews = Word.get_by_id(word_id).reviews.order_by(Review.timestamp.desc()).limit(10).all()

    return jsonify(overall_familiarity=sum([r.familiarity for r in reviews])/len(reviews))


@api.route('get_learning_words', methods=['POST'])
def get_learning_words():
    d = request.json
    limit, = json_check.check_fields(request.json, 'limit')
    offset = d.get('offset', 0)

    q = Word.query.join(WordInfo).filter(WordInfo.is_learning)
    q = q.order_by(WordInfo.overall_familiarity.desc())

    words = q.limit(limit).offset(offset).all()
    words_json = [w.to_json() for w in words]
    return jsonify({'status': 'ok', 'data': words_json})


@api.route('get_need_review_word_id', methods=['POST'])
def get_need_review_word_id():
    wids = learning.get_review_word_ids()

    return jsonify({'status': 'ok', 'data': wids})


@api.route('get_today_reviewed_word_ids', methods=['POST'])
def get_today_reviewed_word_ids():
    rvs = Review.query.filter(Review.timestamp > datetime.today()).group_by(Review.word_id)

    ids = []
    for rv in rvs:
        ids.append(rv.word_id)

    return jsonify(status='ok', data=ids)


@api.route('set_learning', methods=['POST'])
def set_learning():
    word_ids, = json_check.check_fields(request.json, 'word_ids')

    for id in word_ids:
        wi = WordInfo.get(word_id=id)
        wi.is_learning = True
        db.session.add(wi)
    db.session.commit()

    return jsonify(status='ok')







