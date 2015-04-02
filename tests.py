from sqlalchemy.orm import Session

from unittest import TestCase, main

import Models

StatLine = None
Player = None
Team = None
Season = None

class TestModels (TestCase) :

    @classmethod
    def setUpClass(self) :
        self.Engine = Models.loadModels("/test")
    	global StatLine
    	global Player
    	global Team
    	global Season
	StatLine = Models.StatLine
	Player = Models.Player
	Team = Models.Team
	Season = Models.Season

    def setUp(self):
        self.baseStatId = 1024*1024
	self.testSeason = "1000"
	self.testPlayerId = -5
	self.testTeamId = -10
        self.testPlayerName = "Test Player"
	self.testTeamName = "Test Team"
	self.testTeamAbbrev = "TTT"

	self.season_1 = Season(season_id=self.testSeason)
	self.stat_1 = 	StatLine(stat_id = self.baseStatId+1, player_id = self.testPlayerId, team_id = self.testTeamId, season = self.testSeason, gp = 1, wins = 1, losses = 1, pct = 1, mins = 1, fgm = 1, fga = 1, fg3m = 1, fg3a = 1, fg3pct = 1, ftm = 1, fta = 1, ftpct = 1, oreb = 1, dreb = 1, reb = 1, ass = 1, tov = 1, stl = 1, blk = 1, blka = 1, pf = 1, pfd = 1, pts = 1, plusminus = 1)
	self.stat_2 = 	StatLine(stat_id = self.baseStatId+2, player_id = None, team_id = self.testTeamId, season = self.testSeason, gp = 2, wins = 2, losses = 2, pct = 2, mins = 2, fgm = 2, fga = 2, fg3m = 2, fg3a = 2, fg3pct = 2, ftm = 2, fta = 2, ftpct = 2, oreb = 2, dreb = 2, reb = 2, ass = 2, tov = 2, stl = 2, blk = 2, blka = 2, pf = 2, pfd = 2, pts = 2, plusminus = 2)
	self.player_1 = Player(player_id = self.testPlayerId, name = self.testPlayerName)
	self.team_1 = 	Team(team_id = self.testTeamId, name = self.testTeamName, abrv = self.testTeamAbbrev)

        s = Session(self.Engine, expire_on_commit=False)
        s.query(Season).filter(Season.season_id == self.testSeason).delete()
        s.query(StatLine).filter(StatLine.stat_id > self.baseStatId).delete()
        s.query(Player).filter(Player.player_id == self.testPlayerId).delete()
        s.query(Team).filter(Team.team_id == self.testTeamId).all()
	s.commit()
	s.close()

	s = Session(self.Engine, expire_on_commit=False)
	s.add(self.player_1)
	s.add(self.team_1)
	s.add(self.stat_1)
	s.add(self.stat_2)
        s.add(self.season_1)
	s.commit()
	s.close()

    def tearDown(self) :
        s = Session(self.Engine, expire_on_commit=False)
	s.delete(self.season_1)
	s.delete(self.team_1)
	s.delete(self.stat_1)
	s.delete(self.stat_2)
	s.delete(self.player_1)
	s.commit()
	s.close()

    """
	Tests for Season data model
    """

    def test_season_1(self) :
    	s = Session(self.Engine, expire_on_commit=False)
	result = s.query(Season).get(self.testSeason)
	self.assertEqual(result.season_id, self.season_1.season_id)
	self.assertEqual(result.season_id, self.testSeason)
	s.commit()
	s.close()

    """
	Tests for Player data model
    """

    def test_player_1(self) :
    	s = Session(self.Engine, expire_on_commit=False)
	result = s.query(Player).get(self.testPlayerId)
	s.close()
	self.assertEqual(result.player_id, self.player_1.player_id)
	self.assertEqual(result.player_id, self.testPlayerId)
	self.assertEqual(result.name, self.player_1.name)
	self.assertEqual(result.name, self.testPlayerName)

    def test_player_2(self) :
    	s = Session(self.Engine, expire_on_commit=False)
	result = s.query(Player).filter(Player.player_id == self.testPlayerId)
	s.close()
	for row in result:
		self.assertEqual(row.player_id, self.player_1.player_id)
		self.assertEqual(row.player_id, self.testPlayerId)
		self.assertEqual(row.name, self.player_1.name)
		self.assertEqual(row.name, self.testPlayerName)

    """
        Tests for StatLine data model
    """

    def test_stat_1(self) :
    	expected_id = self.baseStatId + 1
    	s = Session(self.Engine, expire_on_commit=False)
	result = s.query(StatLine).get(expected_id)
	s.close()
	self.assertEqual(result.stat_id, expected_id)
	self.assertEqual(result.stat_id, self.stat_1.stat_id)
	self.assertEqual(result.player_id, self.testPlayerId)
	self.assertEqual(result.team_id, self.testTeamId)
	self.assertEqual(result.gp, 1)

    def test_stat_2(self) :
    	expected_id = self.baseStatId + 2
    	s = Session(self.Engine, expire_on_commit=False)
	result = s.query(StatLine).get(expected_id)
	s.close()
	self.assertEqual(result.stat_id, expected_id)
	self.assertEqual(result.stat_id, self.stat_2.stat_id)
	self.assertEqual(result.player_id, None)
	self.assertEqual(result.team_id, self.testTeamId)
	self.assertEqual(result.gp, 2)

    def test_stat_3(self) :
    	s = Session(self.Engine, expire_on_commit=False)
	result = s.query(StatLine).filter(StatLine.stat_id > self.baseStatId).all()
	s.close()
	for row in result:
		self.assertTrue(row.stat_id > self.baseStatId)

    """
        Tests for Team data model
    """

    def test_team_1(self) :
    	s = Session(self.Engine, expire_on_commit=False)
	result = s.query(Team).get(self.testTeamId)
	s.close()
	self.assertEqual(result.team_id, self.testTeamId)
	self.assertEqual(result.team_id, self.team_1.team_id)
	self.assertEqual(result.name, self.testTeamName)


if __name__ == "__main__":
    main()
