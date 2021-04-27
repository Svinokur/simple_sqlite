# simple_sqlite

[![PyPI version](https://badge.fury.io/py/selenium-driver-updater.svg)](https://badge.fury.io/py/simple_sqlite)
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/Svinokur/simple_sqlite/master/LICENSE)

It is a fast and convenience package that can help you using sqlite3 library much easier and faster.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install simple_sqlite.

```
pip install simple-sqlite
```

## Usage
This example shows how you can use this library to create database.
```python
from simple_sqlite import SimpleSqlite

ssql = SimpleSqlite('basic.db')
result, message = ssql.create_database()

```

## Contributing
Always suggest creating new methods. Open an issue first to discuss what you would like to add.