# dynamically generate flask models using sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine

# TODO include relationship fields in attributes?

class StatLine:
	"""
Stats model. Contains all of the statistics for a given stat line.
Attributes:
   stat_id The unique id of this stat line.
   player_id The id of the player this stat line belongs to, or None if it is a team stat line.
   team_id The id of the team this stat line belongs to, or the team of the player this stat line belongs to.
   season The season id that this stat line is from.
   gp Total games played during the season.
   wins Total games won during the season.
   losses Total games lost during the season.
   pct Win percentage during the season.
   mins The average minutes played per game during the season.
   fgm The average field goals made per game during the season.
   fga The average field goals attempted per game during the season.
   fg3m The average three-point field goals made per game during the season.
   fg3a The average three-point field goals attempted per game during the season.
   fg3pct The total three-point field goal percentage during the season.
   ftm The average free throws made per game during the season.
   fta The average free throws attempted per game during the season.
   ftpct The total free throw percentage during the season.
   oreb The average offensive rebounds per game during the season.
   dreb The average defensive rebounds per game during the season.
   reb The average rebounds per game during the season.
   ass The average assists per game during the season.
   tov The average turnovers per game during the season.
   stl The average steals per game during the season.
   blk The average blocks per game during the season.
   blka The average blocks attempted per game during the season.
   pf The average personal fouls per game during the season.
   pfd The average defensive personal fouls per game during the season.
   pts The average points scored per game during the season.
   plusminus The average plus/minus per game during the season.
"""
	pass

class Player:
	"""
Player Model. Contains all of the information for a specific player.
Attributes:
    player_id The id of the player.
    name The name of the player.
    nba_team_team_id The team_id of the most recent team this player belongs to.
"""
	pass

class Team:
	"""
Team Model. Contains all of the information for a specific team.
Attributes:
    team_id The id of the team.
    name The name of the team.
    abrv The three letter abbreviation the NBA uses for each team.
"""
	pass

class Season:
	"""
Season Model. Contains all of the information for a given season.
Attributes:
    season_id The id of the season.
	"""
	pass


def loadModels() :
    """
    Loads the model classes from sqlalchemy using automap.
    """
    global StatLine
    global Player
    global Team
    global Season

    Base = automap_base()

    Engine = create_engine("postgresql://postgres:nbaproject@23.253.119.99:5432/test")

    # reflect the tables
    Base.prepare(Engine, reflect=True)

    # load classes
    StatLine = Base.classes.nba_stats
    Player = Base.classes.nba_player
    Team = Base.classes.nba_team
    Season = Base.classes.nba_season

    return Engine
