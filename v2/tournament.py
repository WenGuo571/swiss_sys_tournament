#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteTournaments(t_name = ''):
    """Remove specific tournament or all tournaments from database.

    Args:
      t_name: if t_name is empty, remove all tournaments records; otherwise
              delete tournament whose name is t_name.
    """
    conn = connect()
    cur = conn.cursor()
    if t_name == '':
        cur.execute("DELETE FROM TOURNAMENTS;")
    else:
        cur.execute("DELETE FROM TOURNAMENTS WHERE T_NAME = %s", (t_name, ))
    conn.commit()
    conn.close()

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

def countPlayers(t_name = ''):
    """Returns the number of players currently registered."""
    conn = connect()
    cur = conn.cursor()
    if t_name == '':
        cur.execute("SELECT COUNT(*) FROM PLAYERS;")
    else:
        t_id = getTournamentID(t_name, False)
        if t_id == -1:
            return 0
        cur.execute("SELECT COUNT(*) FROM PLAYERS WHERE T_ID = %s", (t_id,))
    row = cur.fetchone()
    conn.close()
    return row[0]

def getTournamentID(t_name, create = True):
    """If t_name is not in database, insert into table. Return tournament id.

    Args:
      t_name: tournament name
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT T_ID FROM TOURNAMENTS WHERE T_NAME = %s;", (t_name,))
    t_id = cur.fetchone()
    if t_id == None and create:
        cur.execute("INSERT INTO TOURNAMENTS (T_NAME) VALUES (%s);", (t_name,))
        conn.commit()
        cur.execute("SELECT T_ID FROM TOURNAMENTS ORDER BY T_ID DESC LIMIT 1;")
        t_id = cur.fetchone()
    conn.close()
    if t_id == None and create == False:
        return -1
    return t_id[0]

def registerPlayer(name, t_name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cur = conn.cursor()
    t_id = getTournamentID(t_name)
    cur.execute("INSERT INTO PLAYERS (P_NAME, T_ID) VALUES (%s, %s);", (name, t_id,))
    conn.commit()
    conn.close()

def playerStandings(t_name):
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
    t_id = getTournamentID(t_name, False)
    if t_id == -1:
        return []
    conn = connect()
    cur = conn.cursor()
    cur.execute("CREATE OR REPLACE VIEW WINS AS SELECT P_ID, COUNT(WINNER) \
                 AS WIN_CNT FROM PLAYERS LEFT JOIN MATCHES ON P_ID = WINNER\
                 GROUP BY P_ID ORDER BY P_ID;")
    conn.commit()
    cur.execute("CREATE OR REPLACE VIEW MATCH_WIN AS \
                 SELECT T1.P1, T1.P2, CNT1, WIN_CNT AS CNT2 FROM \
                 (SELECT P1, P2, WIN_CNT AS CNT1 FROM MATCHES, WINS \
                 WHERE P_ID = P1) AS T1, WINS WHERE T1.P2 = P_ID;")
    conn.commit()
    cur.execute("CREATE OR REPLACE VIEW OMW AS\
                 SELECT T.P_ID, SUM(T.CNT) AS OP_CNT FROM (SELECT P1 AS P_ID, \
                 CNT2 AS CNT FROM MATCH_WIN UNION ALL SELECT P2 AS P_ID, CNT1 \
                 AS CNT FROM MATCH_WIN) AS T GROUP BY P_ID ORDER BY P_ID;")
    conn.commit()
    cur.execute("CREATE OR REPLACE VIEW SUMMARY AS SELECT WINS.P_ID, T2.P_NAME,\
                 WINS.WIN_CNT, T2.COUNT AS MATCH_CNT FROM WINS, \
                 (SELECT PLAYERS.P_ID, PLAYERS.P_NAME, COUNT(WINNER) FROM \
                 PLAYERS LEFT JOIN MATCHES ON P_ID = P1 OR P_ID = P2 WHERE \
                 T_ID = %s GROUP BY P_ID) AS T2 WHERE WINS.P_ID = T2.P_ID \
                 ORDER BY WIN_CNT DESC;", (t_id,))
    cur.execute("SELECT SUMMARY.P_ID, SUMMARY.P_NAME, SUMMARY.WIN_CNT, \
                 SUMMARY.MATCH_CNT FROM (SUMMARY LEFT JOIN OMW ON \
                 SUMMARY.P_ID=OMW.P_ID) ORDER BY SUMMARY.WIN_CNT DESC, \
                 OMW.OP_CNT DESC;")
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
    conn = connect()
    cur = conn.cursor()
    if winner != -1 :
        cur.execute("INSERT INTO MATCHES (P1, P2, WINNER) VALUES (%s, %s, %s)",
                    (p1, p2, winner,))
    else :
        cur.execute("INSERT INTO MATCHES (P1, P2) VALUES (%s, %s);",
                    (p1, p2,))
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
    conn = connect()
    cur = conn.cursor()
    if p1 > p2:
        p1, p2 = p2, p1
    cur.execute("SELECT * FROM MATCHES WHERE P1 = %s and P2 = %s;", (p1, p2,))
    row = cur.fetchone()
    conn.close()
    return row != None

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
    if len(rank)%2!=0:
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
