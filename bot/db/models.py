import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Owner(Base):
    __tablename__ = 'owner'

    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=False)
    telegram_id = Column(Integer, nullable=False)


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, unique=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=True, unique=True)
    phone_number = Column(String(50), nullable=True)
    created_at = Column(DateTime, nullable=True, default=datetime.datetime.utcnow())


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)


class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    link = Column(String(250), nullable=False)
    description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"))


class Promotion(Base):
    __tablename__ = 'promotions'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=True, default=datetime.datetime.utcnow())
    link = Column(String(250), nullable=False)
    is_active = Column(Boolean, default=False)
