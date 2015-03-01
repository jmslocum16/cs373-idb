import json
import requests

DEBUG = True

# Format strings for request urls for NBA stats api endpoints
# Arguments:
# 4-digit year, 2-digit year
TEAMS_BY_SEASON_URL = "http://stats.nba.com/stats/leaguedashteamstats?DateFrom=&DateTo=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=%04d-%02d&SeasonSegment=&SeasonType=Regular+Season&StarterBench=&VsConference=&VsDivision="
# 4-digit year, 2-digit year, team ID
PLAYERS_BY_TEAM_SEASON = "http://stats.nba.com/stats/teamplayerdashboard?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=PerGame&Period=0&PlusMinus=N&Rank=N&Season=%04d-%02d&SeasonSegment=&SeasonType=Regular+Season&TeamID=%d&VsConference=&VsDivision="

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
  for year in range(2005, 2006):
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
  return result

def transform(raw_data):
  """
  raw_data data from the NBA api
  """
  return raw_data

def load(data):
  """
  data extracted, transformed data to load to database
  """
  print("Dumping data...")
  print("Data dump not currently implemented")
  return

if '__main__' == __name__:
  raw_data = extract()
  res_data = transform(raw_data)
  load(res_data)
