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
    (\ +(
        \((?P<as>as\ [^)]+( \([IV]+\))?)\)
      | \((?P<also_as>also\ as\ [^)]+)\)
      | \((?P<attached>attached)\)
      | \((?P<archive_footage>.*archive\ footage[^)]*)\)
      | \((?P<archive_sound>.*archive\ sound)\)
      | \((?P<credit_only>credit\ only)\)
      | (?P<hunter_number_2>Hunter \#2)
      | \((?P<in_talks>in\ talks)\)
      | \((?P<episode_details>(\d+\ )?episode[^)]*)\)
      | \((?P<made_for_video>V)\)
      | \((?P<rumored>rumored)\)
      | \((?P<scenes_deleted>scenes\ deleted)\)
      | \((?P<segment>segment [^)]*)\)
      | \((?P<singing_voice>singing\ voice[^)]*)\)
      | \((?P<song>song: [^)]+)\)
      | \((?P<songs>songs)\)
      | \{\{(?P<suspended>SUSPENDED)\}\}
      | \((?P<television>TV)\)
      | \((?P<unconfirmed>unconfirmed)\)
      | \((?P<uncredited>uncredited)\)\ ?\)?
      | \((?P<videogame>VG)\)
      | \((?P<voice>voice[^)]*)\)
      | \((?P<year_scenes>\d\d\d\d\ scenes)\)
      | \((?P<years>\d\d\d\d\ ?-?\ ?\d?\d?\d?\d?)\)
      | Chris
    ))*
    (\ +\[(?P<role>.+?)\] )?
    (\ +<(?P<rank>\d+)>)?
    \n$
    ''', re.X)
    # \ +
    # (?P<tv>\ \(TV\))?
    # (\ +\[(?P<role>[^]]+)\])?
    # \n
    # ''', re.X)

def import_actors(db, filename):
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
        print repr(line)
        print line_re.match(line).groupdict()
        continue
        maybe_actor, title = line.split('\t', 1)
        if maybe_actor:
            actor = maybe_actor
        role_bracket_index = title.find('[')
        if role_bracket_index == -1:
            continue  # ignore rows that do not name the role
        close_bracket_index = title.find(']')
        role = title[role_bracket_index + 1 : close_bracket_index]
        title = title[:role_bracket_index]
        as_index = title.find('(as ')
        if as_index != -1:
            title = title[:as_index]   # chop off '(as Beege Barkett)'
        title = title.strip()
        if '{' in title:  # TV episode
            continue
        db.execute('INSERT INTO actor_title_role VALUES'
                   ' (?, ?, ?)', (actor, title, role))
    db.commit()

if __name__ == '__main__':
#     db = sqlite3.connect('movie.db')
#     db.execute('''
# CREATE TABLE actor_title_role (actor TEXT, title TEXT, role TEXT);
# ''')
    db = None
    import_actors(db, 'actors.list.gz')
    import_actors(db, 'actresses.list.gz')
    
    for cmd in '''

CREATE TABLE movie (id INTEGER PRIMARY KEY, title TEXT UNIQUE);
CREATE TABLE actor (id INTEGER PRIMARY KEY, name TEXT UNIQUE);
CREATE TABLE role (movie_id INTEGER, actor_id INTEGER, role TEXT);

INSERT INTO movie (title) SELECT DISTINCT title FROM actor_title_role;
INSERT INTO actor (name) SELECT DISTINCT actor FROM actor_title_role;

INSERT INTO role (movie_id, actor_id, role)
  SELECT movie.id, actor.id, role FROM actor_title_role
   JOIN movie USING (title)
   JOIN actor ON (actor.name = actor_title_role.actor);

'''.split(';'):
        pass
        # db.execute(cmd)
        # db.commit()

# CREATE INDEX role_unique ON role (role, movie_id, actor_id);
