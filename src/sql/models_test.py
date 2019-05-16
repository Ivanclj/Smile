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
    ip = Column(String(20),nullable=True)
    age = Column(String(3), nullable=True)
    gender = Column(String(10), nullable=True)
    work_interfere = Column(String(3), nullable=True)
    family_history = Column(String(3),nullable=True)
    no_employees = Column(String(20), nullable=True)
    predicted_score = Column(String(5),nullable=False)




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
        return 'sqlite:///user_prediction.db' # relative path



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
    parser = argparse.ArgumentParser(description="Create defined tables in database")
    parser.add_argument("--RDS", default="False",help="True if want to create in RDS else None")
    args = parser.parse_args()
    engine = create_db(args)

    # create engine
    #engine = sql.create_engine(get_engine_string(RDS = False))


    # create a db session
    Session = sessionmaker(bind=engine)  
    session = Session()

    use1 = User_Prediction(ip = "12345",age = "26",gender = "female",predicted_score = "0.8",
                           work_interfere = "Yes", family_history = "Yes", no_employees = "1000" )
    session.add(use1)
    session.commit()

    logger.info("Data added")

    query = "SELECT * FROM user_predictions"
    df = pd.read_sql(query, con=engine)
    logger.info(df)
    session.close()

