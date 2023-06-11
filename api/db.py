from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import and_
from sqlalchemy.engine.url import URL
from sqlalchemy import Column, String, DateTime, ForeignKey, Uuid
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy.dialects.postgresql import BYTEA

from models import POSTGRES_DSN


DeclarativeBase = declarative_base()
DeclarativeBase.metadata.schema = 'content'

class User(DeclarativeBase):
    __tablename__ = 'users'

    id = Column(Uuid, primary_key=True)
    name = Column('name', String, nullable=False)
    token = Column(Uuid, nullable=False)
    created_at = Column(DateTime(), default=datetime.now)

    def __repr__(self):
        return "".format(self.name)

class Audio(DeclarativeBase):
    __tablename__ = 'audios'

    id = Column(Uuid, primary_key=True)
    user_id = Column(Uuid, ForeignKey('users.id'), nullable=False)
    mp3 = Column(BYTEA, nullable=False)
    created_at = Column(DateTime(), default=datetime.now)


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DbManager:
    __metaclass__ = Singleton

    def __init__(self):
        self.engine = create_engine(URL.create(**POSTGRES_DSN))
        self.session = sessionmaker(bind=self.engine)

        DeclarativeBase.metadata.create_all(self.engine)

    def create_record(self, data_rec: dict, table: User | Audio) -> None:
        session = self.session()
        new_rec = table(**data_rec)
        session.add(new_rec)
        session.commit()
        session.close()

    def get_mp3(self, mp3_id: str, user_id: str) -> str|None:
        session = self.session()

        rec_mp3 = session.query(Audio.mp3).filter(
            and_(
                Audio.id == mp3_id,
                Audio.user_id == user_id)
        ).first()

        if rec_mp3:
            path_to_mp3 = f"mp3/{mp3_id}.mp3"
            with open(path_to_mp3, "wb") as binary_file:
                # Write bytes to file
                binary_file.write(rec_mp3[0])
        else:
            path_to_mp3 = None

        session.close()

        return path_to_mp3

    def check_user_token(self, user_id: str, token: str) -> bool:
        session = self.session()

        rec_1 = session.query(User).filter(
            and_(
                User.id == user_id,
                User.token == token)
        ).first()

        session.close()

        return True if rec_1 else False


