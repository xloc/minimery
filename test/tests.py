from datetime import datetime
from unittest import TestCase, mock
from test import TemplateTestCase
from app import db

import sqlite3

import app.model as m


class TestWordModel(TemplateTestCase):
    def test_query_before_commit(self):
        ai = m.AppInfo(name='test', value='world')
        db.session.add(ai)

        a = m.AppInfo.query.all()
        print(len(a))


