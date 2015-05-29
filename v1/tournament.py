#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM MATCHES;")
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM PLAYERS;")
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM PLAYERS;")
    row = cur.fetchone()
    conn.close()
    return row[0]

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO PLAYERS (PLAYER_NAME) VALUES (%s);", (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("CREATE OR REPLACE VIEW SUMMARY AS \
                 SELECT T1.PLAYER_ID, T1.PLAYER_NAME, T1.COUNT AS WIN_CNT, \
                 T2.COUNT AS MATCH_CNT FROM \
                 (SELECT PLAYER_ID, PLAYER_NAME, COUNT(MATCH_ID) FROM \
                 PLAYERS LEFT JOIN MATCHES ON PLAYER_ID = WINNER\
                 GROUP BY PLAYER_ID) AS T1, \
                 (SELECT PLAYER_ID, COUNT(MATCH_ID) FROM \
                 PLAYERS LEFT JOIN MATCHES ON PLAYER_ID = WINNER OR \
                 PLAYER_ID = LOSER GROUP BY PLAYER_ID) AS T2 \
                 WHERE T1.PLAYER_ID = T2.PLAYER_ID \
                 ORDER BY WIN_CNT;")
    conn.commit()
    cur.execute("SELECT * FROM SUMMARY;")
    results = [(int(row[0]), str(row[1]), int(row[2]), int(row[3]))
                for row in cur.fetchall()]
    conn.commit()
    return results;


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO MATCHES (WINNER, LOSER) VALUES (%s, %s);",
                (winner, loser,))
    conn.commit()
    conn.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    players = playerStandings()
    pairs = [(players[2*i][0], players[2*i][1], players[2*i+1][0], players[2*i+1][1]) for i in range(0, len(players)/2)]
    return pairs
