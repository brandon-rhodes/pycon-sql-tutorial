#!/usr/bin/env python

import gzip
import re
import sqlite3

line_re = re.compile(r'''
    (?P<actor_name>[^\t]+)?
    \t+
    (?P<is_televsion>")?(?P<movie_title>[^"]+)"?
    \ +\((?P<year>[\d?]+)(?P<nth_movie_that_year>/[IVX]+)?\)
    (\ +\{(?P<episode>[^}]+)\})?
    (\ *(
        \((?P<as>as\ [^)]+( \([IV]+\))?)\)\)?
      | \((?P<also_as>also\ as\ [^)]+)\)
      | \((?P<attached>attached)\)
      | \((?P<archive_footage>.*archive\ footage[^)]*)\)
      | \((?P<archive_sound>.*archive\ sound[^)]*)\)
      | (?P<bare_number>7|30)
      | (?P<compound_guard_number_3>Compound\ Guard\ \#3)
      | \((?P<credit_only>credit\ only[^)]*)\)
      | \((?P<from>from [^)]*)\)
      | (?P<hunter_number_2>Hunter\ \#2)
      | \((?P<in_talks>in\ talks)\)
      | \((?P<episode_details>(\d+\ )?episode[^)]*)\)
      | \((?P<made_for_video>V)\)
      | \((?P<rumored>rumored)\)
      | \((?P<scenes_deleted>scenes\ deleted)\)
      | \((?P<segment>segment [^)]*)\)
      | \((?P<singing_voice>singing\ voice[^)]*)\)
      | \((?P<song>song:? [^)]+)\)
      | \((?P<songs>songs?)\)
      | \{\{(?P<suspended>SUSPENDED)\}\}
      | \((?P<television>TV)\)
      | \((?P<unconfirmed>unconfirmed)\)
      | \((?P<uncredited>uncredited[^)]*)\)\ ?\)?
      | \((?P<videogame>VG)\)
      | \(?(?P<voice>voice[^)]*)\)
      | \(?(?P<voice2>;\ \(voice\))\)
      | \((?P<year_scenes>\d\d\d\d\ scenes)\)
      | \((?P<years>\d\d\d\d\ ?-?\ ?[?\d]?[?\d]?[?\d]?[?\d]?)\)
      | Chris
    ))*
    (\ +\[(?P<role>.+?)\] )?
    (\ +<(?P<rank>\d+)>)?
    \n$
    ''', re.X)

def import_actors(db, filename, gender):

    lines = iter(gzip.open(filename))

    while not next(lines).startswith('Name'):
        continue

    next(lines)   # skip the title underlines

    for line in lines:

        if line.startswith('-----------------------'):
            break
        if line == '\n':
            continue
        line = line.decode('latin-1')

        m = line_re.match(line)
        if m is None:
            print 'Could not parse %r' % line
            continue

        g = m.groupdict()

        if 'actor_name' in g:
            actor = g['actor_name']

        if (g['archive_footage']
            or g['archive_sound']
            or g['credit_only']
            or g['episode']
            or g['in_talks']
            or g['is_televsion']
            or g['rumored']
            or g['scenes_deleted']
            or g['song']
            or g['songs']
            or g['suspended']
            or g['television']
            or g['unconfirmed']
            or g['uncredited']
            or g['videogame']
            ):
            continue

        db.execute('INSERT INTO actor_title_role VALUES (?, ?, ?, ?, ?, ?)',
                   (actor, gender, g['movie_title'], g['year'],
                    g['made_for_video'], g['role']))

    db.commit()

if __name__ == '__main__':
    db = sqlite3.connect('movie.db')
    db.execute('''
CREATE TABLE actor_title_role (
    actor TEXT, gender TEXT,
    title TEXT, year INTEGER, for_video BOOLEAN,
    role TEXT
);
''')
    import_actors(db, 'cache/actors.list.gz', 'm')
    import_actors(db, 'cache/actresses.list.gz', 'f')

    for cmd in '''

CREATE TABLE movie (
  id INTEGER PRIMARY KEY, title TEXT, year INTEGER, for_video BOOLEAN
  );
CREATE TABLE actor (
  id INTEGER PRIMARY KEY, name TEXT, gender TEXT
  );
CREATE TABLE role (
  movie_id INTEGER, actor_id INTEGER, role TEXT
  );

INSERT INTO movie (title, year, for_video)
  SELECT DISTINCT title, year, for_video
    FROM actor_title_role;

INSERT INTO actor (name, gender)
  SELECT DISTINCT actor, gender
    FROM actor_title_role;

INSERT INTO role (movie_id, actor_id, role)
  SELECT movie.id, actor.id, role FROM actor_title_role
   JOIN movie USING (title, year)
   JOIN actor ON (actor.name = actor_title_role.actor AND
                  actor.gender = actor_title_role.gender);

'''.split(';'):
        db.execute(cmd)
        db.commit()

# CREATE INDEX role_unique ON role (role, movie_id, actor_id);
# TODO: why is there a movie from year 7? Fix my RE.
