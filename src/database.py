"""
Created on 5/12/19

@author: Lingjun Chen

"""
import os
import sys
import logging
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sql

import argparse

logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
logger = logging.getLogger('sql_db')


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
#
# class Contact(Base):
#     __tablename__ = 'contact_form'
#     id = Column(Integer, primary_key=True, unique=True, nullable=False)
#     #uid = Column(Integer,nullable=False)
#     name = Column(String(20), nullable=True)
#     email = Column(String(20), nullable=True)
#     subject = Column(String(20), nullable=True)
#     msg = Column(String(250), nullable=True)

def get_engine_string(RDS = False):
    if RDS:
        conn_type = "mysql+pymysql"
        user = os.environ.get("MYSQL_USER")
        password = os.environ.get("MYSQL_PASSWORD")
        host = os.environ.get("MYSQL_HOST")
        port = os.environ.get("MYSQL_PORT")
        DATABASE_NAME = 'msia423'
        engine_string = "{}://{}:{}@{}:{}/{}". \
            format(conn_type, user, password, host, port, DATABASE_NAME)
        # print(engine_string)
        logging.debug("engine string: %s"%engine_string)
        return  engine_string
    else:
        return 'sqlite:///data/user_predictions.db' # relative path



def create_db(args,engine=None):
    """Creates a database with the data models inherited from `Base`.

    Args:
        engine (:py:class:`sqlalchemy.engine.Engine`, default None): SQLAlchemy connection engine.
            If None, `engine_string` must be provided.
        engine_string (`str`, default None): String defining SQLAlchemy connection URI in the form of
            `dialect+driver://username:password@host:port/database`. If None, `engine` must be provided.

    Returns:
        None
    """
    if engine is None:
        RDS = eval(args.RDS) # evaluate string to bool
        logger.info("RDS:%s"%RDS)
        engine = sql.create_engine(get_engine_string(RDS = RDS))

    Base.metadata.create_all(engine)
    logging.info("database created")

    return engine





if __name__ == "__main__":
    # create engine
    #engine = sql.create_engine(get_engine_string(RDS = False))

    parser = argparse.ArgumentParser(description="Create and/or add data to database")
    subparsers = parser.add_subparsers()
    parser.add_argument("--RDS", default="False", help="True if want to create in RDS else None")
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

    args = parser.parse_args()
    engine = create_db(args)


    # create a db session
    Session = sessionmaker(bind=engine)  
    session = Session()

    user1 = User_Prediction(age=args.age, gender=args.gender,country = args.country,states = args.states,
                           benefits = args.benefits,care_options = args.care_options,
                           leave = args.leave, coworksers = args.coworksers, family_history = args.family_history,
                           no_employees = args.no_employees, predicted_score = args.predicted_score)
    session.add(user1)
    session.commit()

    logger.info("Data added")

    session.close()

