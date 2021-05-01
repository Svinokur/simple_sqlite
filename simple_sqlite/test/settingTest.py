import unittest
import sys
import time
import os.path
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from _setting import setting

base_dir = os.path.dirname(os.path.abspath(__file__))[:-5] + os.path.sep

class testSetting(unittest.TestCase): 
    """Class for unit-testing settings

    Attributes:
        setting (dict[str]) : Dict of all additional parametres
        startTime (float)   : Time of starting unit-tests
    """

    def setUp(self):
        self.setting = setting
        
        self.startTime : float = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print("%.3f" % t)

    #@unittest.skip('Temporary not needed')
    def test01_checkCountMainParam(self):
        self.assertEqual(len(self.setting), 2)

    #@unittest.skip('Temporary not needed')
    def test02_checkCountParams(self):
        self.assertEqual(len(self.setting["Program"]), 1)
        self.assertEqual(len(self.setting["Sqllite"]), 8)
    
    #@unittest.skip('Temporary not needed')
    def test03_checkValuesParams(self):

        self.assertEqual(self.setting["Program"]["BaseDir"], base_dir)

        self.assertEqual(self.setting["Sqllite"]["TestDatabase"], base_dir + "testDatabase.db")
        self.assertEqual(self.setting["Sqllite"]["TestDatabaseUpd"], base_dir + "testDatabaseUpd.db")

        self.assertEqual(self.setting["Sqllite"]["TableTest"], 'test')
        self.assertEqual(self.setting["Sqllite"]["ViewTest"], 'view_test')

        self.assertEqual(self.setting["Sqllite"]["SqlTableTest"], 'CREATE TABLE {} ("lesson_number" text, "lesson_name" text, "lesson_info" text)')
        self.assertEqual(self.setting["Sqllite"]["SqlViewTest"], 'CREATE VIEW {} ("lesson_number", "lesson_name", "lesson_info") AS SELECT * from test')

        self.assertEqual(self.setting["Sqllite"]["SqlScriptSelectFirstLesson"], 'SELECT * from test where lesson_number="1"')
        self.assertEqual(self.setting["Sqllite"]["SqlScriptChangeLessonName"], 'UPDATE test SET lesson_name="Spanish lesson" WHERE lesson_number="1"')

if __name__ == '__main__':
    unittest.main(verbosity=2, failfast=True, exit=False)