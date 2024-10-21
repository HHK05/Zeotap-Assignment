from sqlalchemy import create_engine,Column,Integer,String,Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

base=declarative_base()
class Rule(base):
    __tablename__='rules'
    id = Column(Integer,primary_key=True)
    rule_string=Column(String)
    ast_representation = Column(Text)

engine = create_engine('sqlite:///rules.db')
base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

