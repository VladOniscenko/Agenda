import os.path
import sqlite3
import sys


class ContextManager:
    def __init__(self):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(base_path, 'database.db')

        # Create database if doesnt exist
        if not os.path.exists(db_path):
            open(db_path, 'w').close()

        # Create connection with database
        self.__connection = sqlite3.connect(db_path)
        self.__cursor = self.__connection.cursor()
        self.create_tables()

    def execute(self, query: str, params: list | tuple = (), fetch_mode: str = 'all') -> bool | list | int:
        try:
            self.__cursor.execute(query, params)
            self.__connection.commit()
        except sqlite3.Error as e:  # Catch SQLite-specific errors
            print(f"SQLite execution error: {e}")
            return False

        lowercase_query = query.strip().upper()

        # If it's a SELECT query, fetch and return rows
        if lowercase_query.startswith("SELECT"):
            if fetch_mode == 'one':
                return self.__cursor.fetchone()
            else:
                return self.__cursor.fetchall()

        # If it's an insert query, return inserted row id
        elif lowercase_query.startswith("INSERT"):
            if self.__cursor.lastrowid:
                return self.__cursor.lastrowid
            return False

        return True

    def create_tables(self):
        self.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL
            )
            """
        )

        self.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NULL,
                date DATETIME NOT NULL,
                status TEXT NOT NULL CHECK (status IN ('Pending', 'In Progress', 'Completed', 'On Hold', 'Cancelled')),
                priority TEXT NOT NULL,
                user_id INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
