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
    Base = automap_base()

    Engine = create_engine("postgresql://{user}:{pass}@{ip}:{port}/{dbname}")

    # reflect the tables
    Base.prepare(Engine, reflect=True)

    # load classes
    StatLine = Base.classes.nba_stats
    Player = Base.classes.nba_player
    Team = Base.classes.nba_team
    Season = Base.classes.nba_season

    return Engine
