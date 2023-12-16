-- from the terminal run:
-- psql < music.sql


DROP DATABASE IF EXISTS music;

CREATE DATABASE music;

\c music 

CREATE TABLE songs (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  duration_in_seconds INTEGER NOT NULL,
  release_year INTEGER NOT NULL,
  artists TEXT [] NOT NULL,
  album TEXT NOT NULL,
  producers TEXT [] NOT NULL
);

CREATE INDEX idx_title ON songs (title);

INSERT INTO songs (
    title,
    duration_in_seconds,
    release_year,
    artists,
    album,
    producers
  )
VALUES (
    'MMMBop',
    238,
    1997,
    '{"Hanson"}',
    'Middle of Nowhere',
    '{"Dust Brothers", "Stephen Lironi"}'
  ),
  (
    'Bohemian Rhapsody',
    355,
    1975,
    '{"Queen"}',
    'A Night at the Opera',
    '{"Roy Thomas Baker"}'
  ),
  (
    'One Sweet Day',
    282,
    1995,
    '{"Mariah Carey", "Boyz II Men"}',
    'Daydream',
    '{"Walter Afanasieff"}'
  ),
  (
    'Shallow',
    216,
    2018,
    '{"Lady Gaga", "Bradley Cooper"}',
    'A Star Is Born',
    '{"Benjamin Rice"}'
  ),
  (
    'How You Remind Me',
    223,
    2001,
    '{"Nickelback"}',
    'Silver Side Up',
    '{"Rick Parashar"}'
  ),
  (
    'New York State of Mind',
    276,
    2009,
    '{"Jay Z", "Alicia Keys"}',
    'The Blueprint 3',
    '{"Al Shux"}'
  ),
  (
    'Dark Horse',
    215,
    2013,
    '{"Katy Perry", "Juicy J"}',
    'Prism',
    '{"Max Martin", "Cirkut"}'
  ),
  (
    'Moves Like Jagger',
    201,
    2011,
    '{"Maroon 5", "Christina Aguilera"}',
    'Hands All Over',
    '{"Shellback", "Benny Blanco"}'
  ),
  (
    'Complicated',
    244,
    2002,
    '{"Avril Lavigne"}',
    'Let Go',
    '{"The Matrix"}'
  ),
  (
    'Say My Name',
    240,
    1999,
    '{"Destiny''s Child"}',
    'The Writing''s on the Wall',
    '{"Darkchild"}'
  );