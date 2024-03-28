import sqlite3
from sqlite3 import Error

import psycopg2


def create_sqlite_connection():
    """ create a database connection to a database that resides
        in the memory
    """
    conn = None;
    try:
        conn = sqlite3.connect('FarmMonitor.db',check_same_thread=False)
        print(sqlite3.version)
    except Error as e:
        print(e)
        return

    return conn

def create_connection():
    conn = psycopg2.connect(
        database = "farm_monitor", 
        user = "farm_user", 
        host = 'localhost',
        password = "F@rm--123789",
        port = 5432
    )

    return conn