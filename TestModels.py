from sqlalchemy.orm import Session

from unittest import TestCase, main

from Models import StatLine, Player, Team, Season, loadModels

class TestModels (TestCase) :

    # only need to do this once
    haveSetUp = False

    Engine = None

    def setUp(self) :
        if (self.haveSetUp) :
            return
        self.haveSetUp = True
        self.Engine = loadModels()


    def test(self) :
        print("got through setup")



if __name__ == "__main__":
    main()
