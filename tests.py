from sqlalchemy.orm import Session

import json
import serve

from unittest import TestCase, main

import Models

class TestModels (TestCase):

    @classmethod
    def setUpClass(self):
        serve.init("/test")

    def setUp(self):
        serve.app.config['Testing'] = True

        self.baseStatId = 1024*1024
        self.testSeason = "1000"
        self.testPlayerId = -5
        self.testTeamId = -10
        self.testPlayerName = "Test Player"
        self.testTeamName = "Test Team"
        self.testTeamAbbrev = "TTT"

        self.season_1 = serve.Season(season_id=self.testSeason)
        self.stat_1 =     serve.StatLine(stat_id = self.baseStatId+1, player_id = self.testPlayerId, team_id = self.testTeamId, season = self.testSeason, gp = 1, wins = 1, losses = 1, pct = 1, mins = 1, fgm = 1, fga = 1, fg3m = 1, fg3a = 1, fg3pct = 1, ftm = 1, fta = 1, ftpct = 1, oreb = 1, dreb = 1, reb = 1, ass = 1, tov = 1, stl = 1, blk = 1, blka = 1, pf = 1, pfd = 1, pts = 1, plusminus = 1)
        self.stat_2 =     serve.StatLine(stat_id = self.baseStatId+2, player_id = None, team_id = self.testTeamId, season = self.testSeason, gp = 2, wins = 2, losses = 2, pct = 2, mins = 2, fgm = 2, fga = 2, fg3m = 2, fg3a = 2, fg3pct = 2, ftm = 2, fta = 2, ftpct = 2, oreb = 2, dreb = 2, reb = 2, ass = 2, tov = 2, stl = 2, blk = 2, blka = 2, pf = 2, pfd = 2, pts = 2, plusminus = 2)
        self.player_1 = serve.Player(player_id = self.testPlayerId, name = self.testPlayerName)
        self.team_1 =     serve.Team(team_id = self.testTeamId, name = self.testTeamName, abrv = self.testTeamAbbrev)

        s = Session(serve.Engine, expire_on_commit=False)
        s.query(serve.Season).filter(serve.Season.season_id == self.testSeason).delete()
        s.query(serve.StatLine).filter(serve.StatLine.stat_id > self.baseStatId).delete()
        s.query(serve.Player).filter(serve.Player.player_id == self.testPlayerId).delete()
        s.query(serve.Team).filter(serve.Team.team_id == self.testTeamId).delete()
        s.commit()
        s.close()

        s = Session(serve.Engine, expire_on_commit=False)
        s.add(self.player_1)
        s.add(self.team_1)
        s.add(self.stat_1)
        s.add(self.stat_2)
        s.add(self.season_1)
        s.commit()
        s.close()

    def tearDown(self):
        s = Session(serve.Engine, expire_on_commit=False)
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

    def test_season_1(self):
        s = Session(serve.Engine, expire_on_commit=False)
        result = s.query(serve.Season).get(self.testSeason)
        self.assertEqual(result.season_id, self.season_1.season_id)
        self.assertEqual(result.season_id, self.testSeason)
        s.commit()
        s.close()

    """
    Tests for Player data model
    """

    def test_player_1(self):
        s = Session(serve.Engine, expire_on_commit=False)
        result = s.query(serve.Player).get(self.testPlayerId)
        s.close()
        self.assertEqual(result.player_id, self.player_1.player_id)
        self.assertEqual(result.player_id, self.testPlayerId)
        self.assertEqual(result.name, self.player_1.name)
        self.assertEqual(result.name, self.testPlayerName)

    def test_player_2(self):
        s = Session(serve.Engine, expire_on_commit=False)
        result = s.query(serve.Player).filter(serve.Player.player_id == self.testPlayerId)
        s.close()
        for row in result:
            self.assertEqual(row.player_id, self.player_1.player_id)
            self.assertEqual(row.player_id, self.testPlayerId)
            self.assertEqual(row.name, self.player_1.name)
            self.assertEqual(row.name, self.testPlayerName)

    """
        Tests for StatLine data model
    """

    def test_stat_1(self):
        expected_id = self.baseStatId + 1
        s = Session(serve.Engine, expire_on_commit=False)
        result = s.query(serve.StatLine).get(expected_id)
        s.close()
        self.assertEqual(result.stat_id, expected_id)
        self.assertEqual(result.stat_id, self.stat_1.stat_id)
        self.assertEqual(result.player_id, self.testPlayerId)
        self.assertEqual(result.team_id, self.testTeamId)
        self.assertEqual(result.gp, 1)

    def test_stat_2(self):
        expected_id = self.baseStatId + 2
        s = Session(serve.Engine, expire_on_commit=False)
        result = s.query(serve.StatLine).get(expected_id)
        s.close()
        self.assertEqual(result.stat_id, expected_id)
        self.assertEqual(result.stat_id, self.stat_2.stat_id)
        self.assertEqual(result.player_id, None)
        self.assertEqual(result.team_id, self.testTeamId)
        self.assertEqual(result.gp, 2)

    def test_stat_3(self):
        s = Session(serve.Engine, expire_on_commit=False)
        result = s.query(serve.StatLine).filter(serve.StatLine.stat_id > self.baseStatId).all()
        s.close()
        for row in result:
            self.assertTrue(row.stat_id > self.baseStatId)

    """
        Tests for Team data model
    """

    def test_team_1(self):
        s = Session(serve.Engine, expire_on_commit=False)
        result = s.query(serve.Team).get(self.testTeamId)
        s.close()
        self.assertEqual(result.team_id, self.testTeamId)
        self.assertEqual(result.team_id, self.team_1.team_id)
        self.assertEqual(result.name, self.testTeamName)


    """
        Test player to dict
    """
    def test_player_to_dict1(self):
        p = serve.Player(player_id = 1, name = "testname")
        d = serve.player_to_dict(p)
        self.assertEqual(d["player_id"], 1)
        self.assertEqual(d["name"], "testname")

    def test_player_to_dict2(self):
        p = serve.Player(player_id = 2, name = None)
        d = serve.player_to_dict(p)
        self.assertEqual(d["player_id"], 2)
        self.assertEqual(d["name"], None)

    def test_player_to_dict3(self):
        p = serve.Player(player_id = 0, name = "redundant")
        d = serve.player_to_dict(p)
        self.assertEqual(d["player_id"], 0)
        self.assertEqual(d["name"], "redundant")

    """
        Test season to dict
    """

    def test_season_to_dict_1 (self):
        result = serve.season_to_dict(self.season_1)
        self.assertEqual(self.testSeason, result["season_id"])


    def test_season_to_dict_2 (self):
        id = "1"
        season = serve.Season(season_id = id)
        result = serve.season_to_dict(season)
        self.assertEqual(id, result["season_id"])


    def test_season_to_dict_3 (self):
        id = "3"
        season = serve.Season(season_id = id)
        result = serve.season_to_dict(season)
        self.assertEqual(id, result["season_id"])


    """
        Test team to dict
    """

    def test_team_to_dict_1 (self):
        team = serve.Team(team_id=10, name = "Houston", abrv="HOU")
        result = serve.team_to_dict(team)
        self.assertEqual(result["team_id"], 10)
        self.assertEqual(result["name"], "Houston")


    def test_team_to_dict_2 (self):
        result = serve.team_to_dict(self.team_1)
        self.assertEqual(result["team_id"], -10)
        self.assertEqual(result["name"], "Test Team")
        self.assertEqual(result["abrv"], "TTT")


    def test_team_to_dict_3 (self):
        team = serve.Team(team_id=0, name = "Test", abrv="T")
        result = serve.team_to_dict(team)
        self.assertEqual(result["team_id"], 0)
        self.assertEqual(result["name"], "Test")
        self.assertEqual(result["abrv"], "T")


    """
        Test statline to dict
    """
    def test_statline_to_dict_1(self):
        d = serve.statline_to_dict(self.stat_1)
        self.assertEqual(d["stat_id"], self.stat_1.stat_id)
        self.assertEqual(d["player_id"], self.stat_1.player_id)
        self.assertEqual(d["team_id"], self.stat_1.team_id)
        self.assertEqual(d["season"], self.stat_1.season)
        self.assertEqual(d["gp"], self.stat_1.gp)
        self.assertEqual(d["wins"], self.stat_1.wins)
        self.assertEqual(d["losses"], self.stat_1.losses)
        self.assertEqual(d["pct"], self.stat_1.pct)
        self.assertEqual(d["mins"], self.stat_1.mins)
        self.assertEqual(d["fgm"], self.stat_1.fgm)
        self.assertEqual(d["fga"], self.stat_1.fga)
        self.assertEqual(d["fg3m"], self.stat_1.fg3m)
        self.assertEqual(d["fg3a"], self.stat_1.fg3a)
        self.assertEqual(d["fg3pct"], self.stat_1.fg3pct)
        self.assertEqual(d["ftm"], self.stat_1.ftm)
        self.assertEqual(d["fta"], self.stat_1.fta)
        self.assertEqual(d["ftpct"], self.stat_1.ftpct)
        self.assertEqual(d["oreb"], self.stat_1.oreb)
        self.assertEqual(d["dreb"], self.stat_1.dreb)
        self.assertEqual(d["reb"], self.stat_1.reb)
        self.assertEqual(d["ass"], self.stat_1.ass)
        self.assertEqual(d["tov"], self.stat_1.tov)
        self.assertEqual(d["stl"], self.stat_1.stl)
        self.assertEqual(d["blk"], self.stat_1.blk)
        self.assertEqual(d["blka"], self.stat_1.blka)
        self.assertEqual(d["pf"], self.stat_1.pf)
        self.assertEqual(d["pfd"], self.stat_1.pfd)
        self.assertEqual(d["pts"], self.stat_1.pts)
        self.assertEqual(d["plusminus"], self.stat_1.plusminus)
    
    def test_statline_to_dict_2(self):
        d = serve.statline_to_dict(self.stat_2)
        self.assertEqual(d["stat_id"], self.stat_2.stat_id)
        self.assertEqual(d["player_id"], self.stat_2.player_id)
        self.assertEqual(d["team_id"], self.stat_2.team_id)
        self.assertEqual(d["season"], self.stat_2.season)
        self.assertEqual(d["gp"], self.stat_2.gp)
        self.assertEqual(d["wins"], self.stat_2.wins)
        self.assertEqual(d["losses"], self.stat_2.losses)
        self.assertEqual(d["pct"], self.stat_2.pct)
        self.assertEqual(d["mins"], self.stat_2.mins)
        self.assertEqual(d["fgm"], self.stat_2.fgm)
        self.assertEqual(d["fga"], self.stat_2.fga)
        self.assertEqual(d["fg3m"], self.stat_2.fg3m)
        self.assertEqual(d["fg3a"], self.stat_2.fg3a)
        self.assertEqual(d["fg3pct"], self.stat_2.fg3pct)
        self.assertEqual(d["ftm"], self.stat_2.ftm)
        self.assertEqual(d["fta"], self.stat_2.fta)
        self.assertEqual(d["ftpct"], self.stat_2.ftpct)
        self.assertEqual(d["oreb"], self.stat_2.oreb)
        self.assertEqual(d["dreb"], self.stat_2.dreb)
        self.assertEqual(d["reb"], self.stat_2.reb)
        self.assertEqual(d["ass"], self.stat_2.ass)
        self.assertEqual(d["tov"], self.stat_2.tov)
        self.assertEqual(d["stl"], self.stat_2.stl)
        self.assertEqual(d["blk"], self.stat_2.blk)
        self.assertEqual(d["blka"], self.stat_2.blka)
        self.assertEqual(d["pf"], self.stat_2.pf)
        self.assertEqual(d["pfd"], self.stat_2.pfd)
        self.assertEqual(d["pts"], self.stat_2.pts)
        self.assertEqual(d["plusminus"], self.stat_2.plusminus)

    """
        test aggregateStatLines
    """
    def test_aggregateStatLines_1(self):
        d = serve.aggregateStatLines([serve.statline_to_dict(self.stat_1)], self.stat_1.player_id, self.stat_1.team_id, self.stat_1.season)

        self.assertEqual(d["player_id"], self.stat_1.player_id)
        self.assertEqual(d["team_id"], self.stat_1.team_id)
        self.assertEqual(d["season"], self.stat_1.season)
        self.assertEqual(d["gp"], self.stat_1.gp)
        self.assertEqual(d["wins"], self.stat_1.wins)
        self.assertEqual(d["losses"], self.stat_1.losses)
        self.assertEqual(d["pct"], 100*self.stat_1.pct)
        self.assertEqual(d["mins"], self.stat_1.mins)
        self.assertEqual(d["fgm"], self.stat_1.fgm)
        self.assertEqual(d["fga"], self.stat_1.fga)
        self.assertEqual(d["fg3m"], self.stat_1.fg3m)
        self.assertEqual(d["fg3a"], self.stat_1.fg3a)
        self.assertEqual(d["fg3pct"], 100*self.stat_1.fg3pct)
        self.assertEqual(d["ftm"], self.stat_1.ftm)
        self.assertEqual(d["fta"], self.stat_1.fta)
        self.assertEqual(d["ftpct"], 100*self.stat_1.ftpct)
        self.assertEqual(d["oreb"], self.stat_1.oreb)
        self.assertEqual(d["dreb"], self.stat_1.dreb)
        self.assertEqual(d["reb"], self.stat_1.reb)
        self.assertEqual(d["ass"], self.stat_1.ass)
        self.assertEqual(d["tov"], self.stat_1.tov)
        self.assertEqual(d["stl"], self.stat_1.stl)
        self.assertEqual(d["blk"], self.stat_1.blk)
        self.assertEqual(d["blka"], self.stat_1.blka)
        self.assertEqual(d["pf"], self.stat_1.pf)
        self.assertEqual(d["pfd"], self.stat_1.pfd)
        self.assertEqual(d["pts"], self.stat_1.pts)
        self.assertEqual(d["plusminus"], self.stat_1.plusminus)

    
    def test_aggregateStatLines_2(self):
        d1 = serve.statline_to_dict(self.stat_1)
        d2 = serve.statline_to_dict(self.stat_2)
        d = serve.aggregateStatLines([d1, d2], d1["player_id"], d1["team_id"], d1["season"])

        self.assertEqual(d["player_id"], d1["player_id"])
        self.assertEqual(d["team_id"], d1["team_id"])
        self.assertEqual(d["season"], d1["season"])
        self.assertEqual(d["gp"], d1["gp"] + d2["gp"])
        self.assertEqual(d["wins"],  d1["wins"] + d2["wins"])
        self.assertEqual(d["losses"],  d1["losses"] + d2["losses"])


    def test_aggregateStatLines_Commutative(self):
        d1 = serve.statline_to_dict(self.stat_1)
        d2 = serve.statline_to_dict(self.stat_2)
        d12 = serve.aggregateStatLines([d1, d2], d1["player_id"], d1["team_id"], d1["season"])
        d21 = serve.aggregateStatLines([d2, d1], d2["player_id"], d2["team_id"], d2["season"])


        self.assertEqual(d12["gp"], d21["gp"])
        self.assertEqual(d12["wins"], d21["wins"])
        self.assertEqual(d12["losses"], d21["losses"])
        self.assertEqual(d12["pct"], d21["pct"])
        self.assertEqual(d12["mins"], d21["mins"])
        self.assertEqual(d12["fgm"], d21["fgm"])
        self.assertEqual(d12["fga"], d21["fga"])
        self.assertEqual(d12["fg3m"], d21["fg3m"])
        self.assertEqual(d12["fg3a"], d21["fg3a"])
        self.assertEqual(d12["fg3pct"], d21["fg3pct"])
        self.assertEqual(d12["ftm"], d21["ftm"])
        self.assertEqual(d12["fta"], d21["fta"])
        self.assertEqual(d12["ftpct"], d21["ftpct"])
        self.assertEqual(d12["oreb"], d21["oreb"])
        self.assertEqual(d12["dreb"], d21["dreb"])
        self.assertEqual(d12["reb"], d21["reb"])
        self.assertEqual(d12["ass"], d21["ass"])
        self.assertEqual(d12["tov"], d21["tov"])
        self.assertEqual(d12["stl"], d21["stl"])
        self.assertEqual(d12["blk"], d21["blk"])
        self.assertEqual(d12["blka"], d21["blka"])
        self.assertEqual(d12["pf"], d21["pf"])
        self.assertEqual(d12["pfd"], d21["pfd"])
        self.assertEqual(d12["pts"], d21["pts"])
        self.assertEqual(d12["plusminus"], d21["plusminus"])


    """
        JSON API tests
    """

    def getJSON(self, url):
        with serve.app.test_client() as a:
            resp = a.get(url)
            datastr = resp.get_data(as_text=True)
            data = json.loads(datastr)
            return data["response"]
        return None
        

    """
        Get all players Test
    """
    def test_get_all_players_1 (self):
        players = self.getJSON("/api/players")
        player_1_dict = serve.player_to_dict(self.player_1)
        self.assertTrue(player_1_dict in players)


    def test_get_all_players_2 (self):
        players = self.getJSON("/api/players")
        player = serve.Player(name="Tim Duncan", player_id=1495)
        player_dict = serve.player_to_dict(player)
        self.assertTrue(player_dict in players)


    def test_get_all_players_3 (self):
        players = self.getJSON("/api/players")
        player = serve.Player(name="James Harden", player_id=201935)
        player_dict = serve.player_to_dict(player)
        self.assertTrue(player_dict in players)


    """
        Get individual player test
    """
    def test_get_player_by_id_1 (self):
        player = self.getJSON("/api/player/-5")
        self.assertNotEqual(player, None)
        self.assertEqual(player["player_id"], -5)
        self.assertEqual(player["name"], "Test Player")


    def test_get_player_by_id_2 (self):
        player = self.getJSON("/api/player/-20")
        self.assertEqual(player, None)
   
    def test_get_player_by_id_3 (self):
        player = self.getJSON("/api/player/201935")
        self.assertNotEqual(player, None)
        self.assertEqual(player["player_id"], 201935)
        self.assertEqual(player["name"], "James Harden")


    """
        Get all player stats for season
    """

    def test_get_player_stats_for_season_1 (self):
        result = self.getJSON("/api/player/-5/season/1000")
        self.assertNotEqual(result, None)
        self.assertEqual(result["player_id"], self.testPlayerId)
        self.assertEqual(result["losses"], 1)


    def test_get_player_stats_for_season_2 (self):
        result = self.getJSON("/api/player/-5/season/1000")
        self.assertNotEqual(result, None)
        self.assertEqual(result["plusminus"], 1)
        self.assertEqual(result["dreb"], 1)
        self.assertEqual(result["team_id"], self.testTeamId)


    def test_get_player_stats_for_season_3 (self):
        result = self.getJSON("/api/player/201935/season/2013")
        self.assertNotEqual(result, None)
        self.assertEqual(result["gp"], 73)

    """
        Get all teams
    """

    def test_get_all_teams_1 (self):
        teams = self.getJSON("/api/teams")
        team_dict = serve.team_to_dict(self.team_1)
        self.assertTrue(team_dict in teams)


    def test_get_all_teams_2 (self):
        teams = self.getJSON("/api/teams")
        team = serve.Team(team_id = 1610612745, name = "Houston Rockets", abrv = "HOU")
        team_dict = serve.team_to_dict(team)
        self.assertTrue(team_dict in teams)
    
    def test_get_all_teams_3 (self):
        teams = self.getJSON("/api/teams")
        team = serve.Team(team_id = 1610612759, name = "San Antonio Spurs", abrv = "SAS")
        team_dict = serve.team_to_dict(team)
        self.assertTrue(team_dict in teams)
    
    """
        Get Team By Id
    """
    def test_get_team_by_id_1 (self):
        team = self.getJSON("/api/team/" + str(self.team_1.team_id))
        self.assertNotEqual(team, None)
        self.assertEqual(team["team_id"], self.team_1.team_id)
        self.assertEqual(team["name"], self.team_1.name)
        self.assertEqual(team["abrv"], self.team_1.abrv)

    def test_get_team_by_id_2 (self):
        team = self.getJSON("/api/team/-1")
        self.assertEqual(team, None)

    def test_get_team_by_id_3 (self):
        team = self.getJSON("/api/team/1610612759")
        self.assertNotEqual(team, None)
        self.assertEqual(team["team_id"], 1610612759)
        self.assertEqual(team["name"], "San Antonio Spurs")
        self.assertEqual(team["abrv"], "SAS")

    """
        Get team stats for season
    """

    def test_get_team_stats_for_season_1(self):
        result = self.getJSON("/api/team/" + str(self.testTeamId) + "/season/" + self.testSeason)
        self.assertNotEqual(result, None)
        self.assertEqual(result["season"], self.testSeason)
        self.assertEqual(result["team_id"], self.testTeamId)
        self.assertEqual(result["plusminus"], self.stat_2.plusminus)

    def test_get_team_stats_for_season_2(self):
        result = self.getJSON("/api/team/" + str(self.testTeamId) + "/season/0")
        self.assertEqual(result, None)

    def test_get_team_stats_for_season_3(self):
        result = self.getJSON("/api/team/1610612759/season/2013")
        self.assertNotEqual(result, None)
        self.assertEqual(result["season"], "2013")
        self.assertEqual(result["team_id"], 1610612759)
        self.assertEqual(result["wins"], 62)
        self.assertEqual(result["gp"], 82)


    """
        Get all seasons
    """
    def test_get_all_seasons_1(self):
        seasons = self.getJSON("/api/seasons")
        self.assertNotEqual(seasons, None)
        season = serve.season_to_dict(serve.Season(season_id=self.testSeason))
        self.assertTrue(season in seasons)

    def test_get_all_seasons_2(self):
        seasons = self.getJSON("/api/seasons")
        self.assertNotEqual(seasons, None)
        season = serve.season_to_dict(serve.Season(season_id="12"))
        self.assertFalse(season in seasons)

    def test_get_all_seasons_3(self):
        seasons = self.getJSON("/api/seasons")
        self.assertNotEqual(seasons, None)
        season = serve.season_to_dict(serve.Season(season_id="2013"))
        self.assertTrue(season in seasons)

    """
        Get stats for season
    """
    def test_get_season_1(self):
        season = self.getJSON("/api/season/" + str(self.testSeason))
        season = serve.season_to_dict(serve.Season(season_id=self.testSeason))
        self.assertNotEqual(season, None)
        self.assertTrue(self.stat_1 not in season)

    def test_get_season_2(self):
        season = self.getJSON("/api/season/" + str(self.testSeason))
        self.assertFalse(self.stat_2 in season)

    def test_get_season_3(self):
        season = self.getJSON("/api/season/2013")
        self.assertNotEqual(season, None)
        found = False
        for s in season:
          for line in s:
            found |= line["team_id"] == 1610612759
        self.assertTrue(found)

    """
        Player Search Tests
    """
    def test_player_search_1 (self):
       result = serve.player_search("Test Player")
       self.assertTrue(len(result) == 1)
       self.assertTrue(result[0][0] == -5)
       self.assertTrue(result[0][1] == "Test Player")

    def test_player_search_2 (self):
        result = serve.player_search("sfdgsdgsdfkjgfdskjghafdjhadfljo")
        self.assertTrue(len(result) == 0)

    def test_player_search_3 (self):
        result = serve.player_search("James")
        self.assertTrue(any (r[0] == 201935 and r[1] == "James Harden" for r in result))

    """
        Team Search Tests
    """

    def test_team_search_1 (self):
       result = serve.team_search("Test Team")
       self.assertTrue(len(result) == 1)
       self.assertTrue(result[0][0] == -10)
       self.assertTrue(result[0][1] == "Test Team")

    def test_team_search_2 (self):
        result = serve.team_search("sfdgsdgsdfkjgfdskjghafdjhadfljo")
        self.assertTrue(len(result) == 0)

    def test_team_search_3 (self):
        result = serve.team_search("Spurs")
        self.assertTrue(len(result) == 1)
        self.assertEqual(r[0][0], 1610612759)
        self.assertEqual(r[0][1],"San Antonio Spurs")

    """
        Season Search Tests
    """

    def test_season_search_1 (self):
       result = serve.season_search("1000")
       self.assertTrue(len(result) == 1)
       self.assertTrue(result[0][0] == "1000")
       self.assertTrue(result[0][1] == "1000")

    def test_team_search_2 (self):
        result = serve.season_search("sfdgsdgsdfkjgfdskjghafdjhadfljo")
        self.assertTrue(len(result) == 0)

    def test_team_search_3 (self):
        result = serve.season_search("20")
        self.assertTrue(len(result) > 0)
        self.assertTrue(any (r[0] == "2014" and r[1] == "2014" for r in result))


if __name__ == "__main__":
    main()
