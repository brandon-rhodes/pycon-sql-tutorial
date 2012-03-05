from sqlalchemy.orm import joinedload, subqueryload
from model import Movie, Role, Actor, make_session

if __name__ == '__main__':
    session = make_session(echo=True)
    title = 'Inception'

    # Ugly

    for mrow in session.execute(
        "SELECT * FROM movie WHERE title = :t",
        {'t': title}
        ):
        print mrow['title'], 'was made in', mrow['year']
        print 'The characters were named:'
        for rrow in session.execute(
            "SELECT * FROM role WHERE movie_id = :id",
            {'id': mrow['id']}
            ):
            print rrow['name'], '/',

    print
    print '-' * 79

    # Pretty

    for movie in session.query(Movie).filter_by(
        title=title
        ):
        print movie.title, 'was made in', movie.year
        print 'The characters were named:'
        # for role in movie.roles:
        #     print role.name, '/',
        for role in session.query(Role).filter_by(
            movie=movie).options(joinedload('actor')
            ):
            print role.name, '/', role.actor.name
        print
