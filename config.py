import configparser
from sqlalchemy import create_engine

config = configparser.ConfigParser()
config.read('db.txt')

engine = create_engine(config.get('database', 'con'))