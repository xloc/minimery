import os
import shutil
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'pretend to be a secret string'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass


class DeploymentConfig(Config):
    database_path = os.path.join(basedir, 'deployment', 'current.sqlite')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(database_path)

    def init_app(app):
        # Backup current database
        if os.path.isfile(DeploymentConfig.database_path):
            # File exist
            shutil.copy(DeploymentConfig.database_path,
                        os.path.join(basedir, 'deployment', datetime.now().isoformat()+'.sqlite'))


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_ECHO = True
    database_path = os.path.join(basedir, 'data-development.sqlite')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(database_path)

    def init_app(app):
        # Prepare Database
        db_template_path = os.path.join(basedir, 'test', 'database_template.sqlite')
        db_testing_path = DevelopmentConfig.database_path
        # - Check if template database is exist
        if not os.path.isfile(db_template_path):
            raise FileNotFoundError("Database Template is not found in test folder")
        # - Delete previous test database
        if os.path.isfile(db_testing_path):
            os.remove(db_testing_path)
        # - Copy
        shutil.copy(db_template_path, db_testing_path)


class TestingConfig(Config):
    TESTING = True
    # SQLALCHEMY_ECHO = True
    db_path = os.path.join(basedir, 'data-test.sqlite')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(db_path)

    @staticmethod
    def init_app(app):

        # Prepare Database
        db_template_path = os.path.join(basedir, 'test', 'database_template.sqlite')
        db_testing_path = TestingConfig.db_path
        # - Check if template database is exist
        if not os.path.isfile(db_template_path):
            raise FileNotFoundError("Database Template is not found in test folder")
        # - Delete previous test database
        if os.path.isfile(db_testing_path):
            os.remove(db_testing_path)
        # - Copy
        shutil.copy(db_template_path, db_testing_path)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'deployment': DeploymentConfig,

    'default': DevelopmentConfig
}
