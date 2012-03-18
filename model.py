from sqlalchemy import create_engine, Column, ForeignKey
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Movie(Base):
    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    year = Column(Integer)
    nth = Column(String)
    for_video = Column(Boolean)

    def __repr__(self):
        return '<movie %r%s (%s)%s>' % (
            self.title,
            (' (%s)' % self.nth if self.nth else ''),
            self.year,
            (' (V)' if self.for_video else '')
            )

class Actor(Base):
    __tablename__ = 'actor'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(String)

    def __repr__(self):
        suffix = 'or' if self.gender == 'm' else 'ress'
        return '<act%s %r>' % (suffix, self.name)

class Role(Base):
    __tablename__ = 'role'

    movie_id = Column(Integer, ForeignKey('movie.id'),
                      primary_key=True)
    actor_id = Column(Integer, ForeignKey('actor.id'),
                      primary_key=True)
    name = Column(String, primary_key=True)

    movie = relationship('Movie', backref=backref('roles'))
    actor = relationship('Actor', backref=backref('roles'))

    def __repr__(self):
        return '<role %r>' % (self.name)

def make_session(echo=True):
    engine = create_engine('sqlite:///movie.db', echo=echo)
    Session = sessionmaker(bind=engine)
    return Session()

if __name__ == '__main__':
    session = make_session()
    for movie in session.query(Movie).filter_by(
        title='Hamlet'):
        print movie
        for role in movie.roles:
            print '   ', role
