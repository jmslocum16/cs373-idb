import json
import requests
import psycopg2

DEBUG = True

# Format strings for request urls for NBA stats api endpoints
# Arguments:
# 4-digit year, 2-digit year
TEAMS_BY_SEASON_URL = "http://stats.nba.com/stats/leaguedashteamstats?DateFrom=&DateTo=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=%04d-%02d&SeasonSegment=&SeasonType=Regular+Season&StarterBench=&VsConference=&VsDivision="
# 4-digit year, 2-digit year, team ID
PLAYERS_BY_TEAM_SEASON = "http://stats.nba.com/stats/teamplayerdashboard?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=PerGame&Period=0&PlusMinus=N&Rank=N&Season=%04d-%02d&SeasonSegment=&SeasonType=Regular+Season&TeamID=%d&VsConference=&VsDivision="
# team ID
TEAM_ABBR_URL = "http://stats.nba.com/stats/teaminfocommon?LeagueID=00&SeasonType=Regular+Season&TeamID=%s&season=2014-15"

class Stats:
  def __init__(self, row):
    self.row = row
    self.w = row[0]
    self.l = row[1]
    self.pct = row[2]
    self.mins = row[3]
    self.fgm = row[4]
    self.fga = row[5]
    self.fgpct = row[6]
    self.fg3m = row[7]
    self.fg3a = row[8]
    self.fg3pct = row[9]
    self.ftm = row[10]
    self.fta = row[11]
    self.ftpct = row[12]
    self.oreb = row[13]
    self.dreb = row[14]
    self.reb = row[15]
    self.ass = row[16]
    self.tov = row[17]
    self.stl = row[18]
    self.blk = row[19]
    self.blka = row[20]
    self.pf = row[21]
    self.pfd = row[22]
    self.pts = row[23]
    self.plusminus = row[24]

class Team:
  def __init__(self, row):
    self.stats = Stats(row[3:])
    self.id = row[0]
    self.name = row[1]
    self.gp = row[2]
    self.abbrev = None

class Player:
  def __init__(self, row):
    self.stats = Stats(row[4:])
    self.playerId = row[1]
    self.name = row[2]
    self.gp = row[3]

def extract():
  """
  return
  """
  result = {}
  """
  result[year] = { teamId1 : { ... }, teamId2 : { ... }, ... }
  result[year][teamId] = {
    "teamStats"   : Team(),   # list of team stats
    "playerStats" : [ Player(), Player(), ... ]    # list of individual stats
  }
  """
  for year in range(2014, 2015):
    result[str(year)] = {}
    teamsRequestString = TEAMS_BY_SEASON_URL % (year, (year + 1) % 100)
    if DEBUG:
      print("Teams Request: " + teamsRequestString)
    teamsBySeasonJson = requests.get(teamsRequestString).json()
    # get team Ids for use later
    teamIds = [row[0] for row in teamsBySeasonJson["resultSets"][0]["rowSet"]]
    for teamId in teamIds:
      playersRequestString = PLAYERS_BY_TEAM_SEASON % (year, (year + 1) % 100, teamId)
      if DEBUG:
        print("Player on team request: " + playersRequestString)
      playersByTeamSeasonJson = requests.get(playersRequestString).json()
      result[str(year)][str(teamId)] = {}
      result[str(year)][str(teamId)]["teamStats"] = Team(teamsBySeasonJson["resultSets"][0]["rowSet"][teamIds.index(teamId)])
      result[str(year)][str(teamId)]["playerStats"] = []
      for playerRow in playersByTeamSeasonJson["resultSets"][1]["rowSet"]:
        result[str(year)][str(teamId)]["playerStats"].append(Player(playerRow))
  teamIdSet = set()
  for year in result:
    for teamId in result[year]:
      teamIdSet.add(teamId)
  for teamId in teamIdSet:
    teamStatPageRequestString = TEAM_ABBR_URL % teamId
    if DEBUG:
      print(teamStatPageRequestString)
    teamStatPageJson = requests.get(teamStatPageRequestString).json()
    result["2014"][teamId]["teamStats"].abbrev = teamStatPageJson["resultSets"][0]["rowSet"][0][4]
  return result

def transform(raw_data):
  """
  raw_data data from the NBA api
  """
  return raw_data

def load(data, conn):
  """
  data extracted, transformed data to load to database
  """
  cur = conn.cursor()

  print("Dumping data...")
  teamIds = {}
  for season in data:
    for teamId in data[season]:
      teamIds[teamId] = (data[season][teamId]["teamStats"].name, data[season][teamId]["teamStats"].abbrev)
  
  for teamId in teamIds:
    try:
      cur.execute("""INSERT INTO nba_team (TEAM_ID, NAME, ABRV)
		     SELECT %s, %s, %s
		     WHERE NOT EXISTS (SELECT 1 FROM nba_team WHERE team_id = %s);""", [teamId, teamIds[teamId][0], teamIds[teamId][1], teamId])
    except psycopg2.IntegrityError:
      pass

  playerIds = set()
  for season in data:
    for teamId in data[season]:
      players = data[season][teamId]["playerStats"]
      for player in players:
        if player.playerId not in playerIds:
          playerIds.add(player.playerId)
          try:
            cur.execute("""INSERT INTO nba_player (PLAYER_ID, NAME)
                         SELECT %s, %s
                         WHERE NOT EXISTS (SELECT 1 FROM nba_player WHERE player_id = %s);""", [player.playerId, player.name, player.playerId])
          except psycopg2.IntegrityError:
            pass

  conn.commit()
  for season in data:
    for teamId in data[season]:
      teamStats = data[season][teamId]["teamStats"]
      try:
        s = teamStats.stats
        cur.execute("""INSERT INTO nba_stats (player_id, team_id, season, gp, wins, losses, pct,
			 mins, fgm, fga, fg3m, fg3a, fg3pct, ftm, fta, ftpct, oreb, dreb, reb,
			 ass, tov, stl, blk, blka, pf, pfd, pts, plusmins)
			SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
			WHERE NOT EXISTS (SELECT 1 FROM nba_stats WHERE player_id = NULL AND team_id = %s AND season = %s);""",
			["NULL", teamId, season, s.gp, s.w, s.l, s.pct, s.mins, s.fgm, s.fga, s.fg3m, s.fg3a,
			 s.fg3pct, s.ftm, s.fta, s.ftpct, s.oreb, s.dreb, s.reb, s.ass, s.tov, s.stl, s.blk, s.blka, s.pf, s.pfd, s.pts, s.plusmins, teamId, season])
      except psycopg2.IntegrityError:
        pass
      playerStatsList = data[season][teamId]["playerStats"]
      for player in playerStatsList:
      	try:
      	  s = player.stats
      	  cur.execute("""INSERT INTO nba_stats (player_id, team_id, season, gp, wins, losses, pct,
	  		mins, fgm, fga, fg3m, fg3a, fg3pct, ftm, fta, ftpct, oreb, dreb, reb,
      	  		 ass, tov, stl, blk, blka, pf, pfd, pts, plusmins)
      	  		SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
      	  		WHERE NOT EXISTS (SELECT 1 FROM nba_stats WHERE player_id = %s AND team_id = %s AND season = %s);""",
			[player.playerId, teamId, season, s.gp, s.w, s.l, s.pct, s.mins, s.fgm, s.fga, s.fg3m, s.fg3a,
      	  		s.fg3pct, s.ftm, s.fta, s.ftpct, s.oreb, s.dreb, s.reb, s.ass, s.tov, s.stl, s.blk,
			s.blka, s.pf, s.pfd, s.pts, s.plusmins, player.playerId, teamId, season])
      	except psycopg2.IntegrityError:
      	  pass
      
  print("Data dump not currently implemented")
  cur.close()
  return

if '__main__' == __name__:

  try :
    connection = psycopg2.connect(database="nba", user="postgres", password="nbaproject", host="localhost")
  except psycopg2.Error as e :
    print (":(")
  raw_data = extract()
  res_data = transform(raw_data)
  load(res_data, connection)
  connection.close()

  
