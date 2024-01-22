from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///batyamemory.db", echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Aneky(Base):
    __tablename__ = "aneky"
    id: int = Column(Integer, Sequence("anek_id_seq"), primary_key=True)
    text: str = Column(String)


Base.metadata.create_all(engine)
