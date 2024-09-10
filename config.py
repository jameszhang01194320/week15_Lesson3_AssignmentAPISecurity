
class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:abc123@localhost/tacos'
    CACHE_TYPE = "SimpleCache"
    DEBUG = True