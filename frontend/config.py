import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    BACKEND_URL = os.getenv('BACKEND_URL')
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False