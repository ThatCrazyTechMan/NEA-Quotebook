import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from database_Settings import postgresql as settings




def get_engine(username, password, host, port, database):
    url = sqlalchemy.engine.URL.create("postgresql+psycopg2", username=username, password=password, host=host, port=port, database=database)
    if not database_exists(url):
        create_database(url)

    engine = create_engine(url, pool_size=10, echo=False)
    return engine

def get_engine_from_settings():
    keys = ["username", "password", "host", "port", "database"]
    if not all(key in keys for key in settings.keys()):
        raise Exception("Invalid settings")

    return get_engine(settings["username"],
                    settings["password"],
                    settings["host"],
                    settings["port"],
                    settings["database"])

def get_session():
    engine = get_engine_from_settings()
    session = sessionmaker(bind=engine)
    return session()

session = get_session()


