import argparse
import logging.config
import yaml
import os


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker
import sqlalchemy

#from src.helpers.helpers import create_connection, get_session



logger = logging.getLogger(__name__)
logger.setLevel("INFO")

Base = declarative_base()




class User_Prediction(Base):
    """Create a data model for the database to be set up for capturing songs """
    __tablename__ = 'user_predictions'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    #uid = Column(Integer,nullable=False)
    age = Column(String(3), nullable=True)
    gender = Column(String(10), nullable=True)
    benefits = Column(String(3), nullable=True)
    country = Column(String(20),nullable=True)
    states = Column(String(20),nullable=True)
    care_options = Column(String(3), nullable=True)
    leave = Column(String(3), nullable=True)
    coworksers = Column(String(3), nullable=True)
    family_history = Column(String(3),nullable=True)
    no_employees = Column(String(20), nullable=True)
    predicted_score = Column(String(5),nullable=False)

def ifin(param, dictionary, alt=None):

    assert type(dictionary) == dict
    if param in dictionary:
        return dictionary[param]
    else:
        return alt

def create_connection(host='127.0.0.1', database="", sqltype="mysql+pymysql", port=3308,
                      user_env="amazonRDS_user", password_env="amazonRDS_pw",
                      username=None, password=None, dbconfig=None, engine_string=None):

    if engine_string is None:
        if dbconfig is not None:
            with open(dbconfig, "r") as f:
                db = yaml.load(f)

            host = db["host"]
            database = ifin("dbname", db, "")
            sqltype = ifin("type", db, sqltype)
            port = db["port"]
            user_env = db["user_env"]
            password_env = db["password_env"]

        username = os.environ.get(user_env) if username is None else username
        password = os.environ.get(password_env) if password is None else password

        engine_string = "{sqltype}://{username}:{password}@{host}:{port}/{database}"
        engine_string = engine_string.format(sqltype=sqltype, username=username,
                                             password=password, host=host, port=port, database=database)

    conn = sqlalchemy.create_engine(engine_string)

    return conn


def get_session(engine=None, engine_string=None):
    """
    Args:
        engine_string: SQLAlchemy connection string in the form of:
            "{sqltype}://{username}:{password}@{host}:{port}/{database}"
    Returns:
        SQLAlchemy session
    """

    if engine is None and engine_string is None:
        return ValueError("`engine` or `engine_string` must be provided")
    elif engine is None:
        engine = create_connection(engine_string=engine_string)

    Session = sessionmaker(bind=engine)
    session = Session()

    return session


def create_db(args):
    """Creates a database with the data model given by obj:`apps.models.Track`
    Args:
        args: Argparse args - should include args.title, args.artist, args.album
    Returns: None
    """

    engine = create_connection(engine_string=args.engine_string)

    Base.metadata.create_all(engine)

    session = get_session(engine=engine)

    user = User_Prediction(age=args.age, gender=args.gender,country = args.country,states = args.states,
                           benefits = args.benefits,care_options = args.care_options,
                           leave = args.leave, coworksers = args.coworksers, family_history = args.family_history,
                           no_employees = args.no_employees, predicted_score = args.predicted_score
                           )
    session.add(user)
    session.commit()
    #logger.info("Database created with song added: %s by %s from album, %s ", args.title, args.artist, args.album)
    session.close()


def add_user(args):
    """Seeds an existing database with additional songs.
    Args:
        args: Argparse args - should include args.title, args.artist, args.album
    Returns:None
    """

    session = get_session(engine_string=args.engine_string)

    user = User_Prediction(age=args.age, gender=args.gender,country = args.country,states = args.states,
                           benefits = args.benefits,care_options = args.care_options,
                           leave = args.leave, coworksers = args.coworksers, family_history = args.family_history,
                           no_employees = args.no_employees, predicted_score = args.predicted_score)
    session.add(user)
    session.commit()
    #logger.info("%s by %s from album, %s, added to database", args.title, args.artist, args.album)
    session.close()


if __name__ == '__main__':

    # Add parsers for both creating a database and adding songs to it
    parser = argparse.ArgumentParser(description="Create and/or add data to database")
    subparsers = parser.add_subparsers()

    parser.add_argument("--age", default='Null', help="age to be added")
    parser.add_argument("--gender", default='Null', help="gender to be added")
    parser.add_argument("--country", default='Null', help="gender to be added")
    parser.add_argument("--states", default='Null', help="gender to be added")
    parser.add_argument("--benefits", default='Null', help="benefits to be added")
    parser.add_argument("--care_options", default='Null', help="care_options to be added")
    parser.add_argument("--leave", default='Null', help="leave to be added")
    parser.add_argument("--coworksers", default='Null', help="coworksers to be added")
    parser.add_argument("--family_history", default='Null', help="family_history to be added")
    parser.add_argument("--no_employees", default='Null', help="no_employees to be added")
    parser.add_argument("--predicted_score", default='Null', help="predicted_score to be added")
    parser.add_argument("--engine_string", default='sqlite:///../data/user_predictions.db',
                           help="SQLAlchemy connection URI for database")

    # Sub-parser for creating a database
    # sb_create = subparsers.add_parser("create", description="Create database")
    # sb_create.add_argument("--ip_address", default=None, help="ip to be added")
    # sb_create.add_argument("--age", default=None, help="age to be added")
    # sb_create.add_argument("--gender", default=None, help="gender to be added")
    # sb_create.add_argument("--benefits", default=None, help="benefits to be added")
    # sb_create.add_argument("--care_options", default=None, help="care_options to be added")
    # sb_create.add_argument("--leave", default=None, help="leave to be added")
    # sb_create.add_argument("--coworksers", default=None, help="coworksers to be added")
    # sb_create.add_argument("--family_history", default=None, help="family_history to be added")
    # sb_create.add_argument("--no_employees", default=None, help="no_employees to be added")
    # sb_create.add_argument("--predicted_score", default=None, help="predicted_score to be added")
    # sb_create.add_argument("--engine_string", default='sqlite:///../data/user_predictions.db',
    #                        help="SQLAlchemy connection URI for database")
    # sb_create.set_defaults(func=create_db)

    # # Sub-parser for ingesting new data
    # sb_ingest = subparsers.add_parser("ingest", description="Add data to database")
    # sb_create.add_argument("--ip_address", default=None, help="ip to be added")
    # sb_create.add_argument("--age", default=None, help="age to be added")
    # sb_create.add_argument("--gender", default=None, help="gender to be added")
    # sb_create.add_argument("--benefits", default=None, help="benefits to be added")
    # sb_create.add_argument("--care_options", default=None, help="care_options to be added")
    # sb_create.add_argument("--leave", default=None, help="leave to be added")
    # sb_create.add_argument("--coworksers", default=None, help="coworksers to be added")
    # sb_create.add_argument("--family_history", default=None, help="family_history to be added")
    # sb_create.add_argument("--no_employees", default=None, help="no_employees to be added")
    # sb_create.add_argument("--predicted_score", default=None, help="predicted_score to be added")
    # sb_ingest.add_argument("--engine_string", default='sqlite:///../data/user_predictions.db',
    #                        help="SQLAlchemy connection URI for database")
    # sb_ingest.set_defaults(func=add_user)

    args = parser.parse_args()
    #args.func(args)
    create_db(args)