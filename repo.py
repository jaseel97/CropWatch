import sqlite3
from sqlite3 import Error

import psycopg2
from psycopg2.extras import LoggingConnection

from config import get_config

#FarmMonitor.db
def create_sqlite_connection():
    db = 'DBFarmMonitor.db'
    config = get_config()
    if config["mode"] == "test":
        db = "DBTest.db"
    conn = None;
    try:
        conn = sqlite3.connect(db,check_same_thread=False)
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
        port = 5432,
        connection_factory=LoggingConnection
    )

    return conn