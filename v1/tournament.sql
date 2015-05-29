-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create PLAYERS table

CREATE TABLE PLAYERS (
  PLAYER_ID SERIAL PRIMARY KEY,
  PLAYER_NAME TEXT NOT NULL
);

CREATE TABLE MATCHES (
  MATCH_ID SERIAL PRIMARY KEY,
  WINNER INT REFERENCES PLAYERS(PLAYER_ID),
  LOSER INT REFERENCES PLAYERS(PLAYER_ID)
);
