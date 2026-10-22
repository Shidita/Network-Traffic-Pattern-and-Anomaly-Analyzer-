import csv
import sqlite3
from pathlib import Path

DB = Path(__file__).with_name("network_traffic.db")

def connect():
    connection = sqlite3.connect(DB)
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    connection = connect()
    connection.executescript("""
    CREATE TABLE IF NOT EXISTS traffic(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        source_ip TEXT NOT NULL,
        destination_ip TEXT NOT NULL,
        port INTEGER NOT NULL,
        packets INTEGER NOT NULL,
        bytes INTEGER NOT NULL,
        protocol TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS anomalies(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        traffic_id INTEGER,
        timestamp TEXT,
        source_ip TEXT,
        packets INTEGER,
        bytes INTEGER,
        score REAL,
        severity TEXT,
        reason TEXT
    );
    """)
    connection.commit()
    connection.close()

def load_csv(path):
    connection = connect()
    connection.execute("DELETE FROM traffic")
    connection.execute("DELETE FROM anomalies")

    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        required = {"timestamp","source_ip","destination_ip","port","packets","bytes","protocol"}
        if not required.issubset(reader.fieldnames or set()):
            raise ValueError("CSV must contain: timestamp, source_ip, destination_ip, port, packets, bytes, protocol")

        for row in reader:
            connection.execute(
                """INSERT INTO traffic
                   (timestamp,source_ip,destination_ip,port,packets,bytes,protocol)
                   VALUES (?,?,?,?,?,?,?)""",
                (row["timestamp"], row["source_ip"], row["destination_ip"],
                 int(row["port"]), int(row["packets"]), int(row["bytes"]), row["protocol"])
            )
    connection.commit()
    connection.close()

def query(sql, params=()):
    connection = connect()
    result = connection.execute(sql, params).fetchall()
    connection.close()
    return result
