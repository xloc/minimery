import json
import sqlite3 as sqlite

from os.path import expanduser
db = sqlite.connect(expanduser('~/Downloads/try.db'), check_same_thread=False)


class Review(object):
    TABLE_NAME = 'reviews'
    CREATE_COMMAND = "CREATE TABLE reviews" \
                     "(" \
                     "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                     "word_id INTEGER," \
                     "time DATETIME, score INTEGER" \
                     ")"

    def __init__(self, id=None, word_id=None, time=None, score=None):
        assert None not in (word_id, score)

        self.id = id
        self.score = score
        self.time = time
        self.word_id = word_id

    def commit(self):
        db.execute("INSERT INTO reviews(id, word_id, time, score) VALUES (?,?,?,?)",
                   (self.id, self.word_id, self.time, self.score))
        db.commit()

    @staticmethod
    def get_by_id(review_id):
        c = db.execute('SELECT '
                       'id, word_id, time, score'
                       ' FROM reviews WHERE id=?', (review_id,))
        # print(c)
        results = [w for w in c]
        assert len(results) == 1
        r = results[0]

        return Review(*r)

    def __repr__(self):
        return 'Review(%d:at%s score%d for%d)' % (
            self.id, self.time.isoformat(), self.score, self.word_id)


class Word(object):
    TABLE_NAME = 'words'
    CREATE_COMMAND = "CREATE TABLE words" \
                     "(" \
                     "id INTEGER PRIMARY KEY AUTOINCREMENT , " \
                     "front text, back text, phonetic text," \
                     "detailed_back text, pronunciation text" \
                     ")"

    def __init__(self, id=None, front=None, back=None, phonetic=None, pronunciation=None, detailed_back=None):
        assert None not in (front, back)
        self.id = id
        self.front = front
        self.back = back
        self.phonetic = phonetic
        self.pronunciation = pronunciation
        if isinstance(detailed_back, str):
            self.detailed_back = json.loads(detailed_back)
        else:
            self.detailed_back = detailed_back

    def commit(self):
        db.execute("INSERT INTO words(id, front, back, phonetic, pronunciation, detailed_back) "
                   "VALUES (?,?,?,?,?,?)", (
            self.id, self.front, self.back, self.phonetic, self.pronunciation,
            json.dumps(self.detailed_back)
        ))
        db.commit()

    @staticmethod
    def all():
        c = db.execute('SELECT '
                       'w.id, w.front, w.back, w.phonetic, w.pronunciation, w.detailed_back'
                       ' FROM words AS w LIMIT 10')

        return [Word(*r) for r in c]

    @staticmethod
    def get_by_id(card_id):
        c = db.execute('SELECT '
                       'id, front, back, phonetic, pronunciation, detailed_back'
                       ' FROM words WHERE id=?', (card_id,))
        # print(c)
        results = [w for w in c]
        assert len(results) == 1
        r = results[0]

        return Word(*r)


models = [Word, Review]


def init_all_tables():
    for i in models:
        a = db.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='%s';" % (i.TABLE_NAME,))
        if a.__next__()[0] == 1:
            print('[%s] exist, dropping' % i.__name__, end='')
            db.execute("DROP TABLE %s" % (i.TABLE_NAME))

        db.execute(i.CREATE_COMMAND)
        db.commit()
        print('[%s] inserted' % i.__name__, end='')


def insert_absent():
    for i in models:
        a = db.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='%s';" % (i.TABLE_NAME,))
        if a.__next__()[0] == 0:
            db.execute(i.CREATE_COMMAND)
            db.commit()
            print('[%s] not exist, inserted' % i.__name__)


def assert_all_table_exists():
    for m in models:
        a = db.execute("select count(*) from sqlite_master where type='table' and name='%s';" % (m.TABLE_NAME,))
        assert a.__next__()[0]


def import_words():
    import os.path
    pth = '~/Downloads/3kL1.completed.json'
    pth = os.path.expanduser(pth)

    with open(pth) as f:
        data = json.load(f)

    for word in data:
        mw = Word(front=word['word'], phonetic=word['phonetic'], detailed_back=word['explanation'],
                  back='; '.join(['%s %s' % (exp['PoS'], exp['Chinese']) for exp in word['explanation']]),
                  pronunciation=word['pronunciation']['content'])
        print('[%s] imported' % mw.front)
        mw.commit()

if __name__ == '__main__':
    # init_all_tables()
    # assert_all_table_exists()
    # import_words()
    # for row in db.execute('SELECT * FROM words'):
    #     print(row)

    insert_absent()


