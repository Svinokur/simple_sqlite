import os

base_dir = os.path.dirname(os.path.abspath(__file__)) + os.path.sep

setting = dict(
    {
        "Program":
        {   
            "BaseDir"           : base_dir,
        },
        "Sqllite":
        {   
            "TestDatabase"                  : base_dir + "testDatabase.db",
            "TestDatabaseUpd"               : base_dir + "testDatabaseUpd.db",

            "TableTest"                     : 'test',
            "ViewTest"                      : "view_test",

            "SqlTableTest"                  : 'CREATE TABLE {} ("lesson_number" text, "lesson_name" text, "lesson_info" text)',

            "SqlViewTest"                   : 'CREATE VIEW {} ("lesson_number", "lesson_name", "lesson_info") AS SELECT * from test',

            'SqlScriptSelectFirstLesson'    : 'SELECT * from test where lesson_number="1"',
            'SqlScriptChangeLessonName'     : 'UPDATE test SET lesson_name="Spanish lesson" WHERE lesson_number="1"',
        }
    }
)