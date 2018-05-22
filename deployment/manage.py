import os
from functools import partial

from flask_script import Shell, Manager

from app import create_app, db
from app.model import WordInfo, Word, Review, AppInfo
from util.db_manipulation import insert_json

app = create_app('deployment')

manager = Manager(app)

def make_context():
    return dict(
        db=db,
        Word=Word, WordInfo=WordInfo, Review=Review, AppInfo=AppInfo,
        insert_json=partial(insert_json, db)
    )

manager.add_command('shell', Shell(make_context=make_context))

if __name__ == '__main__':
    manager.run()

