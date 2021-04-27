import sqlite3
import sys
import os
import traceback
import logging
from typing import Tuple, Any
from sqlite3 import OperationalError
from shutil import copyfile

class SimpleSqlite():

    def __init__(self, dbfile : str):
        """Class for working with sqlite3

        Args:
            dbfile (str): Path to database
        """
        self.conn : Any = None
        self.dbFile : str = dbfile

    def __del__(self):
        if self.conn != None: 
            self.conn.close()

    def create_database(self) -> Tuple[bool, str]:
        """Creates the database (.db file) with specified name

        Returns:
            Tuple of bool and str

            result_run (bool)       : True if function passed correctly, False otherwise.
            message_run (str)       : Empty string if function passed correctly, non-empty string if error.
            
        Raises:
            Except: If unexpected error raised. 

        """

        result_run : bool = False
        message_run : str = ''
        
        try:
            if os.path.isfile(self.dbFile):
                os.remove(self.dbFile)

            result, message = self.open_database()
            if not result:
                logging.error(message)
                return result, message

            if not os.path.isfile(self.dbFile):
                message = f'Cannot create dbfile: {self.dbFile}'
                logging.error(message)
                return result_run, message    

            result_run = True

        except:
            message_run = f'Unexcepted error: {str(traceback.format_exc())}'
            logging.error(message_run)

        return result_run, message_run

    def open_database(self) -> Tuple[bool, str]:
        """Opens the database

        Returns:
            Tuple of bool and str

            result_run (bool)       : True if function passed correctly, False otherwise.
            message_run (str)       : Empty string if function passed correctly, non-empty string if error.
            
        Raises:
            Except: If unexpected error raised. 

        """

        result_run : bool = False
        message_run : str = ''

        try:
            self.conn = sqlite3.connect(self.dbFile)

            result_run = True

        except:
            message_run = f'Unexcepted error: {str(traceback.format_exc())}'
            logging.error(message_run)

        return result_run, message_run

    def create_table(self, tablename : str, strSql : str) -> Tuple[bool, str, str, list[str], list[str]]:
        """Creates the table in database with specified table name

        Args:
            tablename (str)  : Specified table name which will be used for creating table.

            strSql (str)     : Sql script for creating specified table.
            Pass as 'CREATE TABLE lessons ("lesson_number" text, "lesson_name" text)'

        Returns:
            Tuple of bool, str, str, list[str] and list[str]

            result_run (bool)       : True if function passed correctly, False otherwise.
            message_run (str)       : Empty string if function passed correctly, non-empty string if error.
            tableName (str)         : Table name of the created table
            namesFields (list[str]) : All fields of the created table
            typeFields  (list[str]) : Type of all fields of the created table
            
        Raises:
            Except: If unexpected error raised. 

        """

        result_run : bool = False
        message_run : str = ''
        tableName : str = ''
        namesFields : list[str] = []
        typeFields : list[str] = []

        try:
            logging.debug(f'create_table tablename: {tablename} strSql: {strSql}')
        
            self.conn.execute(strSql) 
            strSql = "select name from sqlite_master WHERE type='table' AND name='{}'".format(tablename)
            cur = self.conn.execute(strSql)
            tableName =  cur.fetchone()[0]
            strSql = "SELECT name, type FROM PRAGMA_TABLE_INFO('" + tablename + "')"
            cur = self.conn.execute(strSql)
            namesFields = []
            typeFields = []
            rows = cur.fetchall()
            for row in rows:
                namesFields.append(row[0])    
                typeFields.append(row[1])

            result_run = True

        except:
            message_run = f'Unexcepted error: {str(traceback.format_exc())}'
            logging.error(message_run)

        return result_run, message_run, tableName, namesFields, typeFields

    def insert_table(self, tablename : str, data : list[Any], mode : str = '', replace_symbol : bool = False) -> Tuple[bool, str]:
        """Inserts specific data to specific table in database

        Args:
            tablename (str)         : Specified table name which will be used for creating table
            data (list[Any])        : Specified data which will be used for insertion
            mode (str)              : Delete all previously created data or not. Defaults to empty string.
            replace_symbol (bool)   : Delete symbol ' and " before inserting data. Defaults to False.

        Returns:
            Tuple of bool and str

            result_run (bool)       : True if function passed correctly, False otherwise.
            message_run (str)       : Empty string if function passed correctly, non-empty string if error.
            
        Raises:
            Except: If unexpected error raised. 

        """

        result_run : bool = False
        message_run : str = ''
        rec : list[str] = []
        str_fields : str = ''

        try:
            
            if mode == "delete":
                
                strSql = "delete from " + tablename 
                self.conn.execute(strSql) 
                self.conn.commit()
                

            strSql = "SELECT name FROM PRAGMA_TABLE_INFO('" + tablename + "')"
            
            cur = self.conn.execute(strSql)
            namesFields = []
            rows = cur.fetchall()
            for row in rows:
                result, message, is_autoincrement = self.__check_autoincrement_by_field(tablename, row[0])
                if not result:
                    logging.error(message)
                    return result, message
                if not is_autoincrement:
                    namesFields.append(row[0]) 
                    str_fields = str_fields + row[0] + "," 

            self.conn.execute(strSql) 
            strIns = []
            strSql = f'insert into {tablename} ({str_fields[:-1]}) values('
            fields = ''
            for rec in data:
                fields = ''
                for name in namesFields:
                    if replace_symbol:
                        field = '"{}"'.format(str(rec[name]).replace('"', "'"))
                    else:
                        field = '"{}"'.format(rec[name])
                    fields = fields + field + ','
                fields = fields[:-1] + ')'
                fields = strSql + fields
                strIns.append(fields)

            for insData in strIns:
                self.conn.execute(insData)
            self.conn.commit()

            result_run = True 

        except OperationalError:
            message_run = f'OperationalError error: {str(traceback.format_exc())} tablename : {tablename} insData : {insData}'
            logging.error(message_run)

        except:
            message_run = f'Unexcepted error: {str(traceback.format_exc())}'
            logging.error(message_run)

        return result_run, message_run

    def select_table(self, tablename : str) -> Tuple[bool, str, list[str]]:
        """Selects data in specific table in database

        Args:
            tablename (str)  : Specific table name which will be used for getting data.

        Returns:
            Tuple of bool, str and list[str]

            result_run (bool)       : True if function passed correctly, False otherwise.
            message_run (str)       : Empty string if function passed correctly, non-empty string if error.
            rows (list[str])        : All data from the specified table.
            
        Raises:
            Except: If unexpected error raised. 

        """

        result_run : bool = False
        message_run : str = ''
        rows : list[str] = []
        strSql : str = "SELECT name FROM PRAGMA_TABLE_INFO('" + tablename + "')"

        try:

            cur = self.conn.execute(strSql)
            namesFields = []
            rows = cur.fetchall()
            for row in rows:
                namesFields.append(row[0])           

            self.conn.execute(strSql) 
            strSql = 'select '
            fields = ''
            for name in namesFields:
                field = name
                fields = fields + field + ','
            fields = fields[:-1]
            strSql = strSql + fields + ' from {}'.format(tablename)
            cur = self.conn.execute(strSql)
            rows = cur.fetchall()

            logging.debug(f'rows:{rows}')

            result_run = True 

        except:
            message_run = f'Unexcepted error: {str(traceback.format_exc())}'
            logging.error(message_run)

        return result_run, message_run, rows

    def __check_autoincrement_by_field(self, tablename : str, column_name : str) -> Tuple[bool, str, bool]:
        """Check autoincrement by field in specific table in database

        Args:
            tablename(str)      : Specified table name which will be used for checking.
            column_name(str)    : Specified column name which will be used for checking.

        Returns:
            Tuple of bool, str and bool

            result_run (bool)           : True if function passed correctly, False otherwise.
            message_run (str)           : Empty string if function passed correctly, non-empty string if error.
            is_autoincrement (bool)     : True if specified column_name is autoincrement, False otherwise
            
        Raises:
            Except: If unexpected error raised. 

        """

        result_run : bool = False
        message_run : str = ''
        is_autoincrement : bool = False

        try:
            
            strSql = f"SELECT pk FROM PRAGMA_TABLE_INFO('{tablename}') where name = '{column_name}'"
            cur = self.conn.execute(strSql)
            row = cur.fetchone()
            #pk exists
            if row[0] == 1:
                strSql = f"WITH RECURSIVE \
                            a AS (\
                                SELECT name, lower(replace(replace(sql, char(13), ' '), char(10), ' ')) AS sql\
                                FROM sqlite_master\
                                WHERE lower(sql) LIKE '%integer% autoincrement%' and type = 'table' and name='{tablename}'\
                            ),\
                            b AS (\
                                SELECT name, trim(substr(sql, instr(sql, '(') + 1)) AS sql\
                                FROM a\
                            ),\
                            c AS (\
                                SELECT b.name, sql, '' AS col\
                                FROM b\
                                UNION ALL\
                                SELECT\
                                c.name,\
                                trim(substr(c.sql, ifnull(nullif(instr(c.sql, ','), 0), instr(c.sql, ')')) + 1)) AS sql,\
                                trim(substr(c.sql, 1, ifnull(nullif(instr(c.sql, ','), 0), instr(c.sql, ')')) - 1)) AS col\
                                FROM c JOIN b ON c.name = b.name\
                                WHERE c.sql != ''\
                            ),\
                            d AS (\
                                SELECT name, substr(col, 1, instr(col, ' ') - 1) AS col\
                                FROM c\
                                WHERE col LIKE '%autoincrement%'\
                            )\
                            SELECT col\
                            FROM d\
                            ORDER BY col;"
                try:
                    cur = self.conn.execute(strSql)
                    rows = cur.fetchall()
                    for row in rows: 
                        if row[0] == column_name:
                            is_autoincrement = True
                except:
                    if str(sys.exc_info()[1]) == 'no such table: sqlite_sequence':
                        return True, message_run, is_autoincrement 
                    else:
                        raise   

            result_run = True

        except:
            message_run = f'Unexcepted error: {str(traceback.format_exc())}'
            logging.error(message_run)

        return result_run, message_run, is_autoincrement

    def select_sql_script(self, sql_script : str)  -> Tuple[bool, str, list[Any]]:
        """Selects data by specified sql script

        Args:
            sql_script(str)  : Specified sql script which will used for getting data.
            Pass as "SELECT number from numbers".

        Returns:
            Tuple of bool, str and list[Any]

            result_run (bool)       : True if function passed correctly, False otherwise.
            message_run (str)       : Empty string if function passed correctly, non-empty string if error.
            rows (list[Any])        : All data from the specified sql script.
            
        Raises:
            Except: If unexpected error raised. 

        """

        result_run : bool = False
        message_run : str = ''
        rows : list[Any] = []

        try:
            
            cur = self.conn.execute(sql_script) 
            rows = cur.fetchall()

            result_run = True 

        except:
            message_run = f'Unexcepted error: {str(traceback.format_exc())}'
            logging.error(message_run)

        return result_run, message_run, rows 

    def execute_sql_script(self, sql_script : str) -> Tuple[bool, str]:
        """Executes specified sql script in database

        Args:
            sql_script(str)  : Specified sql script which will be used for execution.

        Returns:
            Tuple of bool and str

            result_run (bool)       : True if function passed correctly, False otherwise.
            message_run (str)       : Empty string if function passed correctly, non-empty string if error.
            
        Raises:
            Except: If unexpected error raised. 

        """

        result_run : bool = False
        message_run : str = ''

        try:
            
            self.conn.execute(sql_script)
            self.conn.commit()

            result_run = True 

        except:
            message_run = f'Unexcepted error: {str(traceback.format_exc())}'
            logging.error(message_run)

        return result_run, message_run

    def replace_database(self, full_name_database_src : str, full_name_database_dst : str) -> Tuple[bool, str]:
        """Function for replacing databases

        Args:
            full_name_database_src (str): Full path of source / original database
            full_name_database_dst (str): Full path of destination database

        Returns:
            Tuple of bool and str

            result_run (bool)       : True if function passed correctly, False otherwise.
            message_run (str)       : Empty string if function passed correctly, non-empty string if error.
            
        Raises:
            Except: If unexpected error raised. 

        """
        result_run : bool = False
        message_run : str = ''
        try:

            if not os.path.exists(full_name_database_src):
                message_run = f'Source database does not exist on the given path : {full_name_database_src}'
                logging.error(message_run)
                return result_run, message_run

            if os.path.exists(full_name_database_dst):
                os.remove(full_name_database_dst)

            copyfile(full_name_database_src, full_name_database_dst)

            if not os.path.exists(full_name_database_dst):
                message_run = f'Destination database does not exists on the given path : {full_name_database_dst}'
                logging.error(message_run)
                return result_run, message_run
            
            result_run = True
    
        except:
            message_run = f'Unexcepted error: {str(traceback.format_exc())}'
            logging.error(message_run)

        return result_run, message_run

    def create_view(self, viewname : str, strSql : str) -> Tuple[bool, str, str, list[str], list[str]]:
        """Creates view in database

        Args:
            viewname (str)  : View name that will be created.
            strSql (str)    : Sql script that will be executed.
            Pass as "CREATE VIEW numbers (number text) AS SELECT number FROM all_numbers"

        Returns:
            Tuple of bool, str, str, list[str] and list[str]

            result_run (bool)       : True if function passed correctly, False otherwise.
            message_run (str)       : Empty string if function passed correctly, non-empty string if error.
            viewName (str)          : View name of the created view
            namesFields (list[str]) : All fields of the created view
            typeFields  (list[str]) : Type of all fields of the created view

        """
        result_run : bool = False
        message_run : str = ''
        viewName : str = '' 
        namesFields : list[str] = [] 
        typeFields : list[str] = []

        try:

            cur = self.conn.execute(strSql) 
            strSql = "select name from sqlite_master WHERE type='view' AND name='{}'".format(viewname)
            cur = self.conn.execute(strSql)
            viewName =  cur.fetchone()[0]
            strSql = "SELECT name, type FROM PRAGMA_TABLE_INFO('" + viewname + "')"
            cur = self.conn.execute(strSql)
            namesFields = []
            typeFields = []
            rows = cur.fetchall()

            for row in rows:
                namesFields.append(row[0])    
                typeFields.append(row[1])
                
            result_run = True
            
        except:
            message_run = f'Unexcepted error: {str(traceback.format_exc())}'
            logging.error(message_run)

        return result_run, message_run, viewName, namesFields, typeFields

    def open_view(self, viewname : str, filter = None) -> Tuple[bool, str, list[Any]]:
        """Open specific view by name

        Args:
            viewname (str)  : Specific view name that will be opened.
            filter          : Specific that will be used]. Defaults to None.

        Returns:
            Tuple of bool, str and list[Any]
        
            result_run (bool)       : True if function passed correctly, False otherwise.
            message_run (str)       : Empty string if function passed correctly, non-empty string if error.
            data (list[Any])        : All data in specific view.
        """
        result_run : bool = False
        message_run : str = ''
        data : list[Any] = []

        try:
            
            if filter == None:
                strSql = "Select * from {}".format(viewname)
            else:
                strSql = "Select * from {} {}".format(viewname, filter) 

            cur = self.conn.execute(strSql)
            data = cur.fetchall() 

            result_run = True
        except:
            message_run = f'Unexcepted error: {str(traceback.format_exc())}'
            logging.error(message_run)

        return result_run, message_run, data
        