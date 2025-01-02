import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DEVELOPMENT_URL').replace('postgres+psycopg2', 'postgresql+psycopg2')
    SESSION_COOKIE_SECURE = False  # Disable secure cookies for local development
    MIGRATIONS_DIR = "migrations/local"  # Separate directory for local migrations
    DEBUG=True

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL').replace('postgres+psycopg2', 'postgresql+psycopg2')
    MIGRATIONS_DIR = "migrations/production"  # Separate directory for production migrations
    DEBUG=False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}