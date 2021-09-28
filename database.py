from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from settings import DATABASE_URI

engine = create_engine(
    DATABASE_URI,
    convert_unicode=True,
    echo=False
)

metadata = MetaData()

db_session = scoped_session(sessionmaker(
    autocommit=False,
    bind=engine
))

Base = declarative_base()


def init_db():
    Base.metadata.create_all(bind=engine)
