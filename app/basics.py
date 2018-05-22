import base64

from flask import Blueprint, render_template, request, jsonify
from app.model import Word

basics = Blueprint('basics', __name__)


@basics.route('/')
def entrance():
    return render_template('list-word.html')


@basics.route('/learn')
def learn_words():
    return render_template('learn-words.html')


@basics.route('/learn_setting')
def learn_setting():
    return render_template('learn_setting.html')


# @basics.route('/list')
# def list_words():
#     words = Word.all()
#     return render_template('list_words-old.html', words=words)
#
#
# @basics.route('/card/<word_id>/pronunciation')
# def get_pronunciation(word_id):
#     p = Word.get_by_id(word_id).pronunciation
#     p = p.encode()
#     return base64.b64decode(p)
#
#
# @basics.route('/api/get-cards', methods=['POST'])
# def get_cards():
#     d = dict(request.json)
#     d['limit'] = d.get('limit', 30)
#     d['offset'] = d.get('offset', 0)
#     d['sort_key'] = d.get('sort_key', 'id')
#
#     return jsonify()
#
#
# @basics.route('/api/record-learn', methods=['POST'])
# def record_learn(card_id, score):
#     card_id, score = map(int, (card_id, score))
#     print("card:%d, score:%d" % (card_id, score))
#
#     return jsonify({'result': 'ok'})
