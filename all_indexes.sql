-- Create indexes that support searches and joins from all directions.

create index idx_movie_title_binary on movie(title COLLATE BINARY);
create index idx_movie_title_nocase on movie(title COLLATE NOCASE);
create index idx_movie_year on movie(year);

create index idx_actor_name_binary on actor(name COLLATE BINARY);
create index idx_actor_name_nocase on actor(name COLLATE NOCASE);

create index idx_role_movie on role(movie_id);
create index idx_role_actor on role(actor_id);
create index idx_role_name_binary on role(name COLLATE BINARY);
create index idx_role_name_nocase on role(name COLLATE NOCASE);
