import sqlite3

class ContextManager:
    def __init__(self):
        self.__connection = sqlite3.connect('database.db')
        self.__cursor = self.__connection.cursor()
        self.create_tables()

    def execute(self, query: str, params: list | tuple = ()) -> bool | list | int:
        lowercase_query = query.strip().lower()
        try:
            self.__cursor.execute(query, params)
            self.__connection.commit()

            # If it's a SELECT query, fetch and return rows
            if lowercase_query.startswith("select"):
                return self.__cursor.fetchall()

            elif lowercase_query.startswith("insert"):
                return self.__cursor.lastrowid

            return True
        except sqlite3.Error as e:  # Catch SQLite-specific errors
            print(f"SQLite execution error: {e}")
            return False

    def create_tables(self):
        self.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NULL,
                date DATETIME NOT NULL,
                status TEXT NOT NULL CHECK (status IN ('Pending', 'In Progress', 'Completed', 'On Hold', 'Cancelled')),
                priority INTEGER NOT NULL
            )
        """)
