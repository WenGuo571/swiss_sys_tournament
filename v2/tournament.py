#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        conn = psycopg2.connect("dbname=tournament")
        cursor = conn.cursor()
        return conn, cursor
    except:
        print("Cannot connect to database!")


def deleteTournaments(t_name=''):
    """Remove specific tournament or all tournaments from database.

    Args:
      t_name: if t_name is empty, remove all tournaments records; otherwise
              delete tournament whose name is t_name.
    """
    conn, cur = connect()
    if t_name == '':
        cur.execute("TRUNCATE MATCHES, PLAYERS, TOURNAMENTS;")
    else:
        query = "DELETE FROM TOURNAMENTS WHERE T_NAME = %s"
        param = (t_name,)
        cur.execute(query, param)
    conn.commit()
    conn.close()


def deleteMatches():
    """Remove all the match records from the database."""
    conn, cur = connect()
    cur.execute("DELETE FROM MATCHES;")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn, cur = connect()
    cur.execute("DELETE FROM PLAYERS;")
    conn.commit()
    conn.close()


def countPlayers(t_name=''):
    """Returns the number of players currently registered."""
    conn, cur = connect()
    if t_name == '':
        cur.execute("SELECT COUNT(*) FROM PLAYERS;")
    else:
        t_id = getTournamentID(t_name, False)
        if t_id == -1:
            return 0
        query = "SELECT COUNT(*) FROM PLAYERS WHERE T_ID = %s"
        param = (t_id, )
        cur.execute(query, param)
    row = cur.fetchone()
    conn.close()
    return row[0]


def getTournamentID(t_name, create=True):
    """If t_name is not in database, insert into table. Return tournament id.

    Args:
      t_name: tournament name
    """
    conn, cur = connect()
    query = "SELECT T_ID FROM TOURNAMENTS WHERE T_NAME = %s;"
    param = (t_name, )
    cur.execute(query, param)
    t_id = cur.fetchone()
    if t_id is None and create:
        query = "INSERT INTO TOURNAMENTS (T_NAME) VALUES (%s);"
        cur.execute(query, param)
        conn.commit()
        cur.execute("SELECT MAX(T_ID) FROM TOURNAMENTS;")
        t_id = cur.fetchone()
    conn.close()
    if t_id is None and create is False:
        return -1
    return t_id[0]


def registerPlayer(name, t_name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn, cur = connect()
    t_id = getTournamentID(t_name)
    query = "INSERT INTO PLAYERS (P_NAME, T_ID) VALUES (%s, %s);"
    param = (name, t_id,)
    cur.execute(query, param)
    conn.commit()
    conn.close()


def playerStandings(t_name):
    """Returns a list of the players and their win records, sorted by wins,
    omw, player_id.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    t_id = getTournamentID(t_name, False)
    if t_id == -1:
        return []
    conn, cur = connect()
    cur.execute("SELECT create_summary();")
    conn.commit()
    query = "SELECT P_ID, P_NAME, WIN, MATCH FROM SUMMARY WHERE T_ID = %s"
    param = (t_id, )
    cur.execute(query, param)
    ps = [(int(row[0]), str(row[1]), int(row[2]), int(row[3]))
          for row in cur.fetchall()]
    return ps


def reportMatch(p1, p2, winner=-1):
    """Records the outcome of a single match between two players.

    Args:
      player1:  the id number of player whose id number is smaller
      player2:  the id number of player whose id number is bigger
      winner:   the id number of the player who won. If result is draw, winner
                should be empty.
    """
    if p1 > p2:
        p1, p2 = p2, p1
    conn, cur = connect()
    query = "SELECT report_match(%s, %s, %s)"
    param = (p1, p2, winner,)
    cur.execute(query, param)
    conn.commit()
    conn.close()


def played(p1, p2):
    """Returns boolean that tells whether this is rematch between playes or not

    Args:
      p1: the id number of one player
      p2: the id number of another player
    Returns:
      Return true if this is rematch between p1 and p2, otherwise return false
    """
    conn, cur = connect()
    if p1 > p2:
        p1, p2 = p2, p1
    cur.execute("SELECT * FROM MATCHES WHERE P1 = %s and P2 = %s;", (p1, p2,))
    row = cur.fetchone()
    conn.close()
    return row is not None


def swissPairings(t_name):
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
    rank = playerStandings(t_name)
    pairs = []
    if len(rank) % 2 != 0:
        for i in range(len(rank), 0, -1):
            if played(rank[i-1][0], rank[i-1][0]) == False:
                ele = rank[i-1]
                reportMatch(ele[0], ele[0], ele[0])
                rank.remove(ele)
                break
    for i in range(0, len(rank)/2):
        p1 = rank[0]
        rank.remove(p1)
        for player in rank:
            if(played(p1[0], player[0])):
                continue
            p2 = player
            rank.remove(p2)
            break
        pairs.append((p1[0], p1[1], p2[0], p2[1]))
    return pairs
