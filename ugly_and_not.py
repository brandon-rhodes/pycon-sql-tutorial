import sqlite3
import sys
from sqlalchemy.orm import joinedload, subqueryload
from model import Movie, Role, Actor, make_session

if __name__ == '__main__' and sys.argv[-1] == 'ugly':

    connection = sqlite3.connect('movie.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    title = 'Inception'

    cursor.execute("SELECT * FROM movie WHERE title = :t",
                   {'t': title})
    for mrow in cursor.fetchall():
        print mrow['title'], 'was made in', mrow['year']
        print 'The characters were named:'
        cursor.execute(
            "SELECT role.name AS role_name, actor.name AS actor_name"
            " FROM role JOIN actor ON (role.actor_id = actor.id)"
            " WHERE movie_id = :id",
            {'id': mrow['id']})
        for rrow in cursor.fetchall():
            print rrow[0], '/', rrow[1]

if __name__ == '__main__' and sys.argv[-1] == 'pretty1':


    session = make_session(echo=False)
    title = 'Inception'

    for movie in session.query(Movie).filter_by(
        title=title
        ):
        print movie.title, 'was made in', movie.year
        print 'Cast:'
        for role in movie.roles:
            print '%r played %r' % (
                role.actor.name, role.name)

if __name__ == '__main__' and sys.argv[-1] == 'pretty2':

    session = make_session(echo=False)
    title = 'Inception'

    for movie in session.query(Movie).filter_by(
        title=title
        ):
        print movie.title, 'was made in', movie.year
        for role in session.query(Role).filter_by(
            movie=movie).options(joinedload('actor')
            ):
            print '%r played %r' % (
                role.actor.name, role.name)
