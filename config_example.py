# DATABASE SETTINGS
pg_db_username  = 'database_username'
pg_db_password  = 'database_password'
pg_db_name      = 'databasename'

pg_db_hostname  = 'localhost'


# Twitter credentials
twitter = {
    'ckey'            : 'twitter_consumer_key',
    'csecret'         : 'twitter_consumer_secret',
    'atoken'          : 'twitter_access_token',
    'asecret'         : 'twitter_access_secret'
}

# Flask settings
DEBUG = True
PORT = 5000
HOST = "127.0.0.1"

# For SQL debugging set echo to True
SQLALCHEMY_ECHO = False

SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = "SOME SECRET"

# PostgreSQL
SQLALCHEMY_DATABASE_URI = "postgresql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER=pg_db_username,
                                                                                        DB_PASS=pg_db_password,
                                                                                        DB_ADDR=pg_db_hostname,
                                                                                        DB_NAME=pg_db_name)
