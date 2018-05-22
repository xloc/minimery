from unittest import TestCase

from util.json_check import check_fields, FieldNotFoundError


class TestAPI(TestCase):
    def test_split(self):
        self.assertEqual(check_fields(dict(a=1, b=2), 'a'), [1])
        self.assertEqual(check_fields(dict(a=1, b=2), 'a,'), [1])

        self.assertEqual(check_fields(dict(a=1, b=2), 'a, b'), [1,2])
        self.assertEqual(check_fields(dict(a=1, b=2), 'a b'), [1, 2])
        self.assertEqual(check_fields(dict(a=1, b=2), 'a,  b'), [1, 2])
        self.assertEqual(check_fields(dict(a=1, b=2), 'a,  b'), [1, 2])
        self.assertEqual(check_fields(dict(a=1, b=2), 'a,  b, '), [1, 2])

    def test_exception(self):
        try:
            check_fields(dict(a=1, b=2), 'c')
        except FieldNotFoundError as e:
            self.assertEqual(str(e), 'required parameters not complete\nNeed: c\nGot : a, b')
        else:
            self.fail('FieldNotFoundError not raised')


