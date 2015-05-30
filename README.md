## Swiss-system Tournament - FSND P2
###### Swiss-system tournament defination: http://en.wikipedia.org/wiki/Swiss-system_tournament
### Poject Description:
Realize swiss system tournament with PostgreSQL and Python.      
Versions:     
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;v1 -- satisfy basic requirements  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;v2 -- satisfy extra requirements
### Function Details
V1 functions and parameters:   
- deleteMatches(): remove all matches from database
- deletePlayers(): remove all players from database
- countPlayers(): count registered players in database
- registerPlayer(name): register player
- playerStandings(): return a list of the players and their win records, order by wins
- reportMatch(winner, loser): insert new match record into database
- swissPairsings(): return a list of pairs of players of next round

V2 functions and parameters:
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
1. install vagrant and VM in your machine, intallation detail:
    https://www.udacity.com/wiki/ud088/vagrant
2. download and put folder swiss_sys_tournament within '~/fullstack/vagrant' which is the shared folder between VM and local file system

### Running locally
1. locate your terminal to directory '~/fullstack/vagrant'
2. run command 'vagrant up' in terminal to start VM
3. run command 'vagrant ssh' in terminal to login
4. start psql server and create database tournament
5. test  
    - test v1:
 - locate to directory v1
 - run command 'psql tournament'
 - input '\i tournament.sql' to create tables and functions in database
 - press 'Ctrl+D' to exit psql
 - input 'python tournament_test.py' to test 
    - test v2: 
 - locate to directory v2
 - run command 'psql tournament'
 - input '\i tournament.sql' to create tables and functions in database
 - press 'Ctrl+D' to exit psql
 - run 'python tournament_test.py' to test        
6. run 'exit' to logout
7. run 'vagrant halt' to shut down VM

### Result
All tests passed!

### Creator
WEN GUO
