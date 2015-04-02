import os.path

import Models

from flask import Flask, jsonify
from sqlalchemy.orm import Session

app = Flask(__name__, static_folder='static_html')
app.debug = False

STATIC_FOLDER = './static_html/'

def player_to_dict(player):
    return { "player_id" : player.player_id, "name" : player.name }

def season_to_dict(season):
    return { "season_id" : season.season_id }

def team_to_dict(team):
    return { "team_id" : team.team_id, "name" : team.name, "abrv" : team.abrv }

def statline_to_dict(line):
    return { "stat_id" : line.stat_id,
        "player_id" : line.player_id,
        "team_id" : line.team_id,
        "season" : line.season_id,
        "gp" : line.gp,
        "wins" : line.wins,
        "losses" : line.losses,
        "pct" : line.pct,
        "mins" : line.mins,
        "fgm" : line.fgm,
        "fga" : line.fga,
        "fg3m" : line.fg3m,
        "fg3a" : line.fg3a,
        "fg3pct" : line.fg3pct,
        "ftm" : line.ftm,
        "fta" : line.fta,
        "ftpct" : line.ftpct,
        "oreb" : line.oreb,
        "dreb" : line.dreb,
        "reb" : line.reb,
        "ass" : line.ass,
        "tov" : line.tov,
        "stl" : line.stl,
        "blk" : line.blk,
        "blka" : line.blka,
        "pf" : line.pf,
        "pfd" : line.pfd,
        "pts" : line.pts,
        "plusminus" : line.plusminus
        }

def aggregateStatLines(lines, player_id = None, season_id = None):
    """
    Aggregate a iterable of stat lines, for players who were traded during a season
    lines an iterable of StatLines
    player_id a player_id to overwrite the result
    """
    result = {}
    for line in lines:
      games_played = line["gp"]
      for stat in line:
        if stat not in result and line[stat] != None:
          result[stat] = line[stat]
        elif stat == "gp":
          result[stat] += line[stat]
        else:
          result[stat] += (line[stat] * games_played)
    for stat in result:
      if stat == "season_id":
        continue
      result[stat] /= result["gp"]
    result["pct"] = result["wins"] / result["losses"]
    result["ftpct"] = result["ftm"] / result["fta"]
    result["fg3pct"] = result["fg3m"] / result["fg3a"]
    if player_id != None:
      result["player_id"] = player_id
    if season_id != None:
      result["season_id"] = season_id
    result["team_id"] = None
    return result

# API endpoints
@app.route('/api/players')
def get_all_players():
    s = Session(self.Engine, expire_on_commit=False)
    players = s.query(Player).all()
    s.close()
    return jsonify({player_to_dict(player) for player in players})

@app.route('/api/player/{player_id}')
def get_player_by_id(player_id):
    s = Session(self.Engine, expire_on_commit=False)
    player = s.query(Player).get(player_id)
    s.close()
    return jsonify(player_to_dict(player))

@app.route('/api/player/{player_id}/season/{season_id}')
def get_player_stats_for_season(player_id, season_id):
    s = Session(self.Engine, expire_on_commit=False)
    player = s.query(Player).get(int(player_id))
    lines = s.query(StatLine).filter(StatLine.player_id == int(player_id) and StatLine.season_id == season_id).all()
    lines = map(lambda line: statline_to_dict(line), lines)
    lines = aggregateStatLines(lines, player_id, season_id)
    s.close()
    return jsonify(lines)

@app.route('/api/teams')
def get_all_teams():
    s = Session(self.Engine, expire_on_commit=False)
    teams = s.query(Team).all()
    s.close()
    return jsonify({team_to_dict(team) for team in teams})

@app.route('/api/team/{team_id}')
def get_team_by_id(team_id):
    s = Session(self.Engine, expire_on_commit=False)
    team = s.query(Team).get(team_id)
    s.close()
    return jsonify({ "team_id" : team.team_id, "name" : team.name, "abrv" : team.abrv })

@app.route('/api/team/{team_id}/season/{season_id}')
def get_team_stats_for_season(team_id, season_id):
    s = Session(self.Engine, expire_on_commit=False)
    teams = s.query(Team).get(team_id)
    seasons = s.query(StatLine).filter(StatLine.season_id == season_id and StatLine.team_id == team_id).all()
    s.close()
    return jsonify({"result" : seasons})

@app.route('/api/seasons')
def get_all_seasons():
    s = Session(self.Engine, expire_on_commit=False)
    seasons = s.query(Season).all()
    s.close()
    return jsonify({season_to_dict(season) for season in seasons})

@app.route('/api/season/{season_id}')
def get_season_by_id(season_id):
    s = Session(self.Engine, expire_on_commit=False)
    season = s.query(Season).get(season_id)
    s.close()
    return jsonify({ "season_id" : season.season_id, "year" : season.season_id + "-" + str(int(season_id)+1) })

# web endpoints
@app.route('/')
def root():
    return app.send_static_file('splash.html')

@app.route('/splash.html')
def splash():
    return app.send_static_file('splash.html')

@app.route('/about.html')
def about():
    return app.send_static_file('about.html')

@app.route('/sorttable.js')
def sorttable():
    return app.send_static_file('sorttable.js')

@app.route('/style.css')
def get_style():
    return app.send_static_file('style.css')

@app.route('/players/<player_id>')
def get_player_page(player_id):
    static_file = 'players/' + player_id
    if os.path.isfile(STATIC_FOLDER + static_file):
        return app.send_static_file(static_file)

@app.route('/seasons/<season_id>')
def get_season_page(season_id):
    static_file = 'seasons/' + season_id
    if os.path.isfile(STATIC_FOLDER + static_file):
        return app.send_static_file(static_file)

@app.route('/teams/<team_id>')
def get_team_page(team_id):
    static_file = 'teams/' + team_id
    if os.path.isfile(STATIC_FOLDER + static_file):
        return app.send_static_file(static_file)

@app.route('/photos/<photo_id>')
def get_photo(photo_id):
    static_file = 'photos/' + photo_id
    if os.path.isfile(STATIC_FOLDER + static_file):
        return app.send_static_file(static_file)

if __name__ == "__main__":
    #TODO - not test...
    global StatLine
    global Player
    global Team
    global Season
    global Engine
    Engine = Models.loadModels("/test")
    StatLine = Models.StatLine
    Player = Models.Player
    Team = Models.Team
    Season = Models.Season
    app.run('0.0.0.0')
