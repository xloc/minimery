from test import TemplateTestCase

from app import db, create_app
from app.model import Word, WordInfo


class TestWord(TemplateTestCase):
    def test_get_by_id(self):
        w = Word.get_by_id(1)

        self.assertEqual(w.id, 1)
        self.assertEqual(w.front, 'abandon')


class TestWordInfo(TemplateTestCase):
    def test_get(self):
        wi = WordInfo.get(1)
        wi.overall_familiarity = 1

        db.session.add(wi)
        db.session.commit()

        wii = WordInfo.get(1)

        self.assertEqual(wi.word_id, wii.word_id)
        self.assertEqual(wi.overall_familiarity, wii.overall_familiarity)

    def test_word_foreign_key(self):
        wi = WordInfo.get(1)
        wi.overall_familiarity = 2

        db.session.add(wi)
        db.session.commit()

        a = Word.get_by_id(1).info
        self.assertEqual(len(a), 1)
        self.assertEqual(a[0].overall_familiarity, 2)

    def test_word_foreign_key_no_info(self):
        a = Word.get_by_id(1).info
        self.assertEqual(a, [])



