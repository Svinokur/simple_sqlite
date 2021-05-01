# simple_sqlite

[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/Svinokur/simple_sqlite/master/LICENSE)
[![Downloads](https://pepy.tech/badge/simple-sqlite)](https://pepy.tech/project/simple-sqlite)
[![Downloads](https://pepy.tech/badge/simple-sqlite/month)](https://pepy.tech/project/simple-sqlite)
[![Downloads](https://pepy.tech/badge/simple-sqlite/week)](https://pepy.tech/project/simple-sqlite)
[![Donate with Ethereum](https://en.cryptobadges.io/badge/micro/0xf2691CC12a70B4589edf081E059fD4A1c457417D)](https://en.cryptobadges.io/donate/0xf2691CC12a70B4589edf081E059fD4A1c457417D)

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
