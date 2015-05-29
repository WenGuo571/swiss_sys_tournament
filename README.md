## Swiss-system Tournament - FSND P2
###### Swiss-system tournament defination: http://en.wikipedia.org/wiki/Swiss-system_tournament
### Versions:
v1 -- satisfy basic requirements  
v2 -- satisfy extra requirements
### API:
V1 API:
- deleteMatches(): remove all matches from database
- deletePlayers(): remove all players from database
- countPlayers(): count registered players in database
- registerPlayer(name): register player
- playerStandings(): return a list of the players and their win records, order by wins
- reportMatch(winner, loser): insert new match record into database
- swissPairsings(): return a list of pairs of players of next round

V2 API:
- deleteTournaments(t_name=''): delete tournament with tournament name or delete all records
- deleteMatches(): delete matches from database
- deletePlayers(): delete players from database
- countPlayers(t_name=''): count players in one tournament or count all registered players
- registerPlayer(name, t_name): register new player in one tournament
- playerStandings(t_name): return a list of the players in one tournament sorted by wins and OMW(Opponent Match Wins)
- reportMatch(player1, player2, winner=-1): report match with player1 id, player2 id and winner id. When winner is empty, match result is draw
- swissPairings(t_name): return a list of pairs for next round in one tournament. If player number is odd, the last player in playerStandings() result who does not have free win got free win and report match that opponent and winner are itself.

### What's included
swiss_sys_tournament/   
|--- v1/  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|--- tournament.py   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|--- tournament_test.py   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|--- tournament.sql  
|--- v2/    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|--- tournament.py    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|--- tournament_test.py    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|--- tournament.sql     

### Quick start
Put all files within one fold.

### Running locally
1. Start psql server
2. test v1: python tournament_test.py within directory v1;    
   test v2: python tournament_test.py within directory v2.

### Result
All tests passed!

### Creator
WEN GUO
