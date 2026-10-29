import os

class Config:
    '''Application configuration'''
    SQLALCHEMY_DATABASE_URI = 'sqlite:///job_history.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False

class TestConfig(Config):
    '''Test configuration'''
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_job_history.db'
    TESTING = True
