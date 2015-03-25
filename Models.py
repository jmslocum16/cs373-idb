# dynamically generate flask models using sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine

"""
Stats model
TODO
"""
StatLine = None

"""
Player Model
TODO
"""
Player = None

"""
Team Model
TODO
"""
Team = None

"""
Season Model
TODO
"""
Season = None


"""
Loads the model classes from sqlalchemy using automap.
"""
def loadModels() :
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
