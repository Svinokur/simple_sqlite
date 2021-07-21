#Standart library imports
import unittest
import sys
import os.path
import time
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

#Local imports
from _setting import setting
from simple_sqlite import SimpleSqlite

class testSqlite(unittest.TestCase):
    """Class for unit-testing Sqllite class

    Attributes:
        sqllite (dict[str]) : Initialize class of Sqllite
        startTime (float)   : Time of starting unit-tests

    """ 
    @classmethod
    def setUpClass(cls):
        cls.setting = setting

        dbFile : str = setting['Sqllite']['TestDatabase']
        cls.sqllite = SimpleSqlite(dbfile = dbFile)

    @classmethod
    def tearDownClass(cls):
        del cls.sqllite

    def setUp(self):
        self.start_time : float = time.time()

    #@unittest.skip('Temporary not needed')  
    def tearDown(self):

        end_time = time.time() - self.start_time
        print("%.3f" % end_time)

    #@unittest.skip('Temporary not needed')
    def test01_create_database(self):
        self.sqllite.create_database()

    #@unittest.skip('Temporary not needed')
    def test02_open_database(self):
        self.sqllite.connect_to_db()

    #@unittest.skip('Temporary not needed')
    def test03_create_table_test(self):
        self.sqllite.connect_to_db()

        tablename = self.setting["Sqllite"]["TableTest"]
        strSql = self.setting["Sqllite"]["SqlTableTest"].format(tablename)
        tableName, namesFields, typeFields = self.sqllite.create_table(tablename=tablename, strSql=strSql)
        self.assertNotEqual(tableName, '')
        self.assertNotEqual(namesFields, '')
        self.assertNotEqual(typeFields, '')

        self.assertEqual(tableName, self.setting["Sqllite"]["TableTest"])
        self.assertEqual(len(namesFields), 3)
        self.assertEqual(namesFields[0], "lesson_number")
        self.assertEqual(namesFields[1], "lesson_name")
        self.assertEqual(namesFields[2], "lesson_info")

        
        self.assertEqual(len(typeFields), 3)
        self.assertEqual(typeFields[0], "text")
        self.assertEqual(typeFields[1], "text")
        self.assertEqual(typeFields[2], "text")
    

    #@unittest.skip('Temporary not needed')
    def test04_insert_table_test(self):
        self.sqllite.connect_to_db()

        tablename = self.setting["Sqllite"]["TableTest"]
        data = [{   'lesson_number'         : '1', 
                    'lesson_name'           : 'English Lesson',
                    'lesson_info'           : 'There will be no lesson',          
                }]
        self.sqllite.insert_table(tablename, data)

    #@unittest.skip('Temporary not needed')
    def test05_select_table_test(self):
        self.sqllite.connect_to_db()

        tablename = self.setting["Sqllite"]["TableTest"]
        datas = self.sqllite.select_table(tablename)
        self.assertGreater(len(datas), 0, len(datas))

        for data in datas:
            self.assertEqual(data[0], '1')
            self.assertEqual(data[1], 'English Lesson')
            self.assertEqual(data[2], 'There will be no lesson')

    #@unittest.skip('Temporary not needed')
    def test06_check_sql_script_table_test(self):
        self.sqllite.connect_to_db()

        sql_script = self.setting["Sqllite"]["SqlScriptSelectFirstLesson"]
        rows = self.sqllite.select_sql_script(sql_script=sql_script)
        self.assertGreater(len(rows), 0, len(rows))

        for data in rows:
            self.assertEqual(data[0], '1')
            self.assertEqual(data[1], 'English Lesson')
            self.assertEqual(data[2], 'There will be no lesson')

    #@unittest.skip('Temporary not needed')
    def test07_check_sql_script_execution_table_test(self):
        self.sqllite.connect_to_db()

        sql_script = self.setting["Sqllite"]["SqlScriptChangeLessonName"]
        self.sqllite.execute_sql_script(sql_script=sql_script)

        tablename = self.setting["Sqllite"]["TableTest"]
        datas = self.sqllite.select_table(tablename)
        self.assertGreater(len(datas), 0, len(datas))

        for data in datas:
            self.assertEqual(data[0], '1')
            self.assertEqual(data[1], 'Spanish lesson')
            self.assertEqual(data[2], 'There will be no lesson')

    #@unittest.skip('Temporary not needed')
    def test08_create_view_test(self):
        self.sqllite.connect_to_db()

        viewname = self.setting["Sqllite"]["ViewTest"]
        str_sql = self.setting["Sqllite"]["SqlViewTest"].format(viewname)
        tableName, namesFields, typeFields = self.sqllite.create_view(viewname, str_sql)
        self.assertEqual(tableName, viewname) 

        self.assertEqual(len(namesFields), 3)
        self.assertEqual(namesFields[0], "lesson_number")
        self.assertEqual(namesFields[1], "lesson_name")
        self.assertEqual(namesFields[2], "lesson_info")

        self.assertEqual(len(typeFields), 3)
        self.assertEqual(typeFields[0], "text")
        self.assertEqual(typeFields[1], "text")
        self.assertEqual(typeFields[2], "text")

    #@unittest.skip
    def test10_open_view_test(self):
        self.sqllite.connect_to_db()

        viewname = self.setting["Sqllite"]["ViewTest"]
        rows = self.sqllite.open_view(viewname=viewname)

        for data in rows:
            self.assertEqual(data[0], '1')
            self.assertEqual(data[1], 'Spanish lesson')
            self.assertEqual(data[2], 'There will be no lesson')

    #@unittest.skip('Temporary not needed')
    def test11_replace_database(self):
        full_name_database_src = self.setting["Sqllite"]["TestDatabase"]
        full_name_database_dst = self.setting["Sqllite"]["TestDatabaseUpd"]
        
        self.sqllite.replace_database(full_name_database_src=full_name_database_src, full_name_database_dst=full_name_database_dst)

if __name__ == '__main__':
    unittest.main(verbosity=2, failfast=True, exit=False)