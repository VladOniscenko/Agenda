if __name__ == '__main__':
    import sqlite3
    from datetime import datetime, timedelta
    import random
    import faker

    # Initialize Faker to generate random data
    fake = faker.Faker()

    # Generate 100 random tasks
    tasks = []
    for _ in range(1000):
        name = fake.word().capitalize()
        description = fake.sentence()

        # Generate random date between 2024-01-01 and 2025-12-31
        start_date = datetime(2024, 1, 1)
        random_date = start_date + timedelta(days=random.randint(0, 730))

        # Format the random date as a string in 'YYYY-MM-DD HH:MM:SS'
        random_date_str = random_date.strftime('%Y-%m-%d %H:%M:%S')

        # Random priority (1-3), status (1 = Pending, 2 = In Progress, 3 = Completed), user_id = 1
        priority = random.randint(1, 3)
        status = random.choice(['Pending', 'In Progress', 'Completed', 'On Hold', 'Cancelled'])  # 1 = Pending, 2 = In Progress, 3 = Completed, etc.
        user_id = 1

        tasks.append((name, description, random_date_str, priority, status, user_id))

    # Connect to the SQLite database (or create it)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create the tasks table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        date TEXT,
        priority INTEGER,
        status INTEGER,
        user_id INTEGER
    )
    """)

    # Insert the generated tasks into the database
    for task in tasks:
        cursor.execute("""
        INSERT INTO tasks (name, description, date, priority, status, user_id)
        VALUES (?, ?, ?, ?, ?, ?)
        """, task)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()