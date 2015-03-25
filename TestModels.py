from sqlalchemy.orm import Session

from unittest import TestCase, main

import Models

class TestModels (TestCase) :

    @classmethod
    def setUpClass(self) :
        self.Engine = Models.loadModels()


    def test(self) :
        #print(dir(self.Engine))
	self.assertEqual(0, 0)
        pass

    def test2(self) :
        #print(self.Engine)
	self.assertTrue(True)
        pass


if __name__ == "__main__":
    main()
