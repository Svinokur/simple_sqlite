import unittest
import os
import sys
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from test import settingTest
from test import sqliteTest

import logging

import traceback

#refresh logger sometimes issue with writing log file
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

base_dir = os.path.dirname(os.path.abspath(__file__)) + os.path.sep

level=logging.DEBUG
format='%(asctime)s %(name)s %(levelname)s [%(module)s %(funcName)s %(lineno)d] %(message)s '
filename=f'{base_dir}log_test.log' 
filemode='w'
encoding='utf-8'

logging.basicConfig(level=level, format=format, filename=filename, filemode=filemode, encoding=encoding)

#define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)

# add the handler to the root logger
logging.getLogger('').addHandler(console)

try:

    testSuite = unittest.TestSuite()
    testSuite.addTest(unittest.makeSuite(settingTest.testSetting))
    testSuite.addTest(unittest.makeSuite(sqliteTest.testSqlite))

    runner = unittest.TextTestRunner(verbosity=2, failfast=True)
    result = runner.run(testSuite)

    if result.wasSuccessful():

        logging.debug('OK')
   
    else:

        for failures in result.failures:
            failures = str(failures) + "\n"
            logging.error(failures)

        for errors in result.errors:
            errors = str(errors) + "\n"
            logging.error(errors)

except:
    message_run = f'Unexcepted error: {str(traceback.format_exc())}'
    logging.error(message_run)