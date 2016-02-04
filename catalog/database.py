import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# the different languages used in the app
class Language(Base):
    __tablename__ = 'language'

    id = Column(Integer, primary_key=True)
    language = Column(String(250), nullable=False)

# the different literary works
class Work(Base):
    __tablename__ = 'work'

    title = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    author = Column(String(80))
    translator = Column(String(250))
    translation_year =  Column(String(6))
    genre = Column(String(80))
    amazon_link = Column(String(250))
    language_id = Column(Integer, ForeignKey('language.id'))
    language = relationship(Language)
    summary = Column(String(1000))

    # JSON enpoint for the works within each language
    @property
    def serialize(self):

        return {
            'title': self.title,
            'id': self.id,
            'author': self.author,
            'translator': self.translator,
            'translation_year': self.translation_year,
            'genre': self.genre,
            'amazon_link': self.amazon_link,
            'language_id': self.language_id,
            'summary': self.summary,
        }



engine = create_engine('sqlite:///worldliterature.db')


Base.metadata.create_all(engine)