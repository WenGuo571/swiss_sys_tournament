-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE IF NOT EXISTS TOURNAMENTS (
  T_ID SERIAL PRIMARY KEY,
  T_NAME TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS PLAYERS (
  P_ID SERIAL PRIMARY KEY,
  P_NAME TEXT NOT NULL,
  T_ID INT REFERENCES TOURNAMENTS(T_ID)
);

CREATE TABLE IF NOT EXISTS MATCHES (
  P1 INT REFERENCES PLAYERS(P_ID),
  P2 INT REFERENCES PLAYERS(P_ID),
  WINNER INT REFERENCES PLAYERS(P_ID) DEFAULT NULL,
  PRIMARY KEY (P1, P2)
);
