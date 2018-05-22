import json
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import app as mini_mery
import config
from app.model import Word, Review, WordInfo


def insert_json(db, json_path):
    json_path = os.path.expanduser(json_path)
    with open(json_path, encoding='utf-8') as f:
        son = json.load(f)

    """
    [{
            word, phonetic
            explanation: [{PoS, Chinese, English}, ...]
            pronunciation: {content, type, encoding:base64}
            tags: [list?, unit?]
    }, ...]
    """
    for word in son:
        w = Word(front=word['word'], phonetic=word['phonetic'], explanation=json.dumps(word['explanation']),
                 back='; '.join(['%s %s' % (exp['PoS'], exp['Chinese']) for exp in word['explanation']]),
                 pronunciation=word['pronunciation']['content'])
        db.session.add(w)
        db.session.commit()
        print("Added [{}]".format(w.front))


def export_words(json_path):
    words = []
    for w in Word.query:
        words.append(w.to_json())

    reviews = []
    for rv in Review.query:
        reviews.append(rv.to_json())

    word_info = []
    for wi in WordInfo.query:
        word_info.append(wi.to_json())

    with open(json_path, 'w') as f:
        json.dump(dict(
            words=words,
            word_info=word_info,
            reviews=reviews
        ), f)


def make_app_with_db(db_path):
    class AConfig(config.Config):
        SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(db_path)

    config.config['a_config'] = AConfig
    app = mini_mery.create_app('a_config')
    return app


if __name__ == '__main__':
    DB_PATH = os.path.join(config.basedir, 'test_template.sqlite')
    JSON_PATH = '~/Downloads/3kL1.completed.json'

    app = make_app_with_db(DB_PATH)
    with app.app_context():
        mini_mery.db.create_all()
        insert_json(mini_mery.db, os.path.expanduser(JSON_PATH))
