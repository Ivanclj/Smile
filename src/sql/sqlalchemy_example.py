from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Column, Integer, String, MetaData
import sqlalchemy as sql
import logging
import pandas as pd

import os
import sqlalchemy as sql


Base = declarative_base()  

class User_Prediction(Base):
	"""Create a data model for the database to be set up for capturing songs """
	__tablename__ = 'user_prediction'
	id = Column(Integer, primary_key=True,unique=True,nullable=False)
	# uid = Column(Integer,nullable=False)
	age = Column(String(3),nullable=True)
	gender = Column(String(10),nullable=True)



# set up sqlite connection
engine_string = 'sqlite:///user_prediction.db'
engine = sql.create_engine(engine_string)
# create the tracks table
Base.metadata.create_all(engine)
# # set up looging config
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)
# create a db session
Session = sessionmaker(bind=engine)  
session = Session()
# add a record/track
user1 = User_Prediction(age = '23',gender = 'male' )
session.add(user1)
session.commit()

# To add multiple rows
# session.add_all([track1, track2])
#session.commit()
# logger.info("Database created with fake user added")
# query records
# user_record = session.query(User_Prediction.age, User_Prediction.gender).filter_by(id=1).first()
# print(user_record)
# query = "SELECT * FROM user_prediction"
# df = pd.read_sql(query, con=engine)
# print(df)
session.close()