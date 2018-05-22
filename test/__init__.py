from unittest import TestCase

from app import db, create_app


class TemplateTestCase(TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()


if __name__ == '__main__':
    pass