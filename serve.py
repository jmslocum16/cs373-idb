import os.path

import Models

from flask import Flask, jsonify, render_template
from sqlalchemy.orm import Session

app = Flask(__name__, static_folder='static_html')
app.debug = True

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
        "season" : line.season,
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

def aggregateStatLines(lines, player_id = None, team_id = None, season_id = None):
    """
    Aggregate one or more stat line dictionaries into one stat line dictionary, for players who were traded during a season
    lines an iterable of stat line dictionaries
    player_id a player_id to overwrite the result
    """
    result = {}
    lines = list(lines)
    if len(lines) == 0:
      return result
    for line in lines:
      games_played = line["gp"]
      for stat in line:
        if stat[-3:] == "pct" or stat == "stat_id" or stat == "player_id" or stat == "team_id" or stat == "season":
          # ignore percent stats and non-numeric static
          continue
        if stat not in result and line[stat] != None:
          result[stat] = line[stat]
          if (stat != "gp" and stat != "wins" and stat != "losses") :
            result[stat] *= games_played
        elif stat == "gp" or stat == "wins" or stat == "losses":
          # just add non-per game stats
          result[stat] += line[stat]
        else:
          # do weighted average of per-game stats by games played
          result[stat] += (line[stat] * games_played)
    for stat in result:
      if stat[-3:] == "pct" or stat == "stat_id" or stat == "player_id" or stat == "team_id" or stat == "season" or stat == "gp" or stat == "wins" or stat == "losses":
        # ignore percents, non-numeric, and non per-game stats
        continue
      # divide by total games played to convert to per-game average
      result[stat] /= result["gp"]
      result[stat] = round(result[stat], 2)

    # manually set new percentages and non-numeric stats
    result["pct"] = round(float(result["wins"]) / float(result["gp"]), 2) * 100 if result["gp"] > 0 else 0
    result["ftpct"] = round(float(result["ftm"]) / float(result["fta"]), 2) * 100 if result["fta"] > 0 else 0
    result["fgpct"] = round(float(result["fgm"]) / float(result["fga"]), 2) * 100 if result["fga"] > 0 else 0
    result["fg3pct"] = round(float(result["fg3m"]) / float(result["fg3a"]), 2) * 100 if result["fg3a"] > 0 else 0
    if player_id != None:
      result["player_id"] = player_id
    if team_id != None :
      result["team_id"] = team_id
    if season_id != None:
      result["season"] = season_id
    return result

# API endpoints
@app.route('/api/players')
def get_all_players():
    s = Session(Engine, expire_on_commit=False)
    players = s.query(Player).all()
    s.close()
    return jsonify({player_to_dict(player) for player in players})

@app.route('/api/player/{player_id}')
def get_player_by_id(player_id):
    s = Session(Engine, expire_on_commit=False)
    player = s.query(Player).get(player_id)
    s.close()
    return jsonify(player_to_dict(player))

@app.route('/api/player/{player_id}/season/{season_id}')
def get_player_stats_for_season(player_id, season_id):
    s = Session(Engine, expire_on_commit=False)
    player = s.query(Player).get(int(player_id))
    lines = s.query(StatLine).filter(StatLine.player_id == int(player_id) and StatLine.season_id == season_id).all()
    lines = map(lambda line: statline_to_dict(line), lines)
    lines = aggregateStatLines(lines, player_id, season_id)
    s.close()
    return jsonify(lines)

@app.route('/api/teams')
def get_all_teams():
    s = Session(Engine, expire_on_commit=False)
    teams = s.query(Team).all()
    s.close()
    return jsonify({team_to_dict(team) for team in teams})

@app.route('/api/team/{team_id}')
def get_team_by_id(team_id):
    s = Session(Engine, expire_on_commit=False)
    team = s.query(Team).get(team_id)
    s.close()
    return jsonify({ "team_id" : team.team_id, "name" : team.name, "abrv" : team.abrv })

@app.route('/api/team/{team_id}/season/{season_id}')
def get_team_stats_for_season(team_id, season_id):
    s = Session(Engine, expire_on_commit=False)
    teams = s.query(Team).get(team_id)
    seasons = s.query(StatLine).filter(StatLine.season_id == season_id and StatLine.team_id == team_id).all()
    s.close()
    return jsonify({"result" : seasons})

@app.route('/api/seasons')
def get_all_seasons():
    s = Session(Engine, expire_on_commit=False)
    seasons = s.query(Season).all()
    s.close()
    return jsonify({season_to_dict(season) for season in seasons})

@app.route('/api/season/{season_id}')
def get_season_by_id(season_id):
    s = Session(Engine, expire_on_commit=False)
    season = s.query(Season).get(season_id)
    s.close()
    return jsonify({ "season_id" : season.season_id, "year" : season.season_id + "-" + str(int(season_id)+1) })

# web endpoints

@app.route('/')
@app.route('/splash.html')
def splash():
    s = Session(Engine, expire_on_commit=False)
    players = s.query(Player).all()
    teams = s.query(Team).all()
    seasons = s.query(Season).all()
    s.close()
    player_by_alphabet = {}
    for player in players:
      letter = player.name.split(' ')[-1][0].lower()
      if letter not in player_by_alphabet:
        player_by_alphabet[letter] = []
      player_by_alphabet[letter].append(player)
    alphabet = sorted(player_by_alphabet.keys())
    teams = sorted(teams, key=lambda x: x.name)
    return render_template('splash.html', alphabet=alphabet, player_by_alphabet=player_by_alphabet, teams=teams, seasons=seasons)

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
    if (player_id.endswith('.html')):
      player_id = player_id[:-5]
    s = Session(Engine, expire_on_commit=False)
    player = s.query(Player).get(player_id)
    stats = s.query(StatLine).filter(StatLine.player_id == player_id).all()
    team_id = max(stats, key=lambda x: int(x.season)).team_id
    team = s.query(Team).get(team_id)
    seasons = s.query(Season).all()
    s.close()
    seasons = sorted(list(seasons), key=lambda x: int(x.season_id), reverse=True)
    season_to_stat = { season : aggregateStatLines(filter(lambda x: x['season'] == season, map(lambda x: statline_to_dict(x), stats)), player_id, team_id, season) for season in map(lambda x: x.season_id, seasons) }
    season_to_stat = { k : season_to_stat[k] for k in season_to_stat if season_to_stat[k] }
    seasons = filter(lambda x: x.season_id in season_to_stat, seasons)
    return render_template('player.html', player=player, seasons=seasons, season_to_stat=season_to_stat, lower_abrv=team.abrv.lower(), upper_abrv=team.abrv.upper())

@app.route('/seasons/<season_id>')
def get_season_page(season_id):
    if (season_id.endswith('.html')):
      season_id = season_id[:-5]
# TODO - test when the database works again
#    s = Session(Engine, expire_on_commit=False)
#    stats = s.query(StatLine).filter(StatLine.season_id == season_id and StatLine.team_id != None).all()
#    teams = s.query(Team).all()
#    s.close()
    stats = []
    return render_template('season.html', stats=stats, season_id=int(season_id))

@app.route('/teams/<team_id>')
def get_team_page(team_id):
    if (team_id.endswith('.html')):
      team_id = team_id[:-5]
# TODO - test when the database works again
#    s = Session(Engine, expire_on_commit=False)
#    team = s.query(Team).get(team_id)
#    stats = s.query(StatLine).filter(StatLine.team_id == team_id).all()
#    seasons = s.query(Season).all()
#    s.close()
    total_wins = 0
    total_losses = 0
    return render_template('team.html', total_wins=total_wins, total_losses=total_losses)

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
    Engine = Models.loadModels("/nba")
    StatLine = Models.StatLine
    Player = Models.Player
    Team = Models.Team
    Season = Models.Season
    app.run('0.0.0.0')
