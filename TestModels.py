from sqlalchemy.orm import Session

from unittest import TestCase

from Models import StatLine, Player, Team, Season, loadModels

class TestModels (TestCase) :

    # only need to do this once
    haveSetUp = False

    Engine = None

    def setUp() :
        if (haveSetUp) :
            return
        haveSetUp = True
        Engine = loadModels()


    def test() :
        print("got through setup")
