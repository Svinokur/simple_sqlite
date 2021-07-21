from setuptools import setup

with open('README.md') as f:
    long_description = f.read()
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

keywords = ['sqlite', 'sqlite3']
 
setup(
  name='simple_sqlite',
  version='2.0.0',
  description='This package can help you using sqlite3 library much easier and faster.',
  long_description=long_description,
  long_description_content_type='text/markdown', 
  url='https://github.com/Svinokur/simple_sqlite',  
  author='Stanislav Vinokur',
  author_email='stasvinokur@yahoo.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=keywords,
  packages=['simple_sqlite'],
  install_requires=[] 
)