import sqlite3

from MatchData import MatchData


class DB:
    def __init__(self):
        # Connect the sqllite db, if not exist it will be created
        conn = sqlite3.connect('../Cheapestticket/data.db')
        cursor = conn.cursor()

        # Creat table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS matches (
                website TEXT,
                time TEXT,
                team TEXT,
                price TEXT,
                query_time TEXT
            )
        ''')

        # Submit the modification and close the connection
        conn.commit()
        conn.close()

    def fetch(self, query_time):
        conn = sqlite3.connect('../Cheapestticket/data.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM matches
            WHERE query_time = ?
        ''', (query_time,))

        # Get the result
        results = cursor.fetchall()
        print(f"query from db {len(results)}")
        # print the result

        ms = []
        for result in results:
            data = MatchData(result[0], result[1], result[2], result[3], result[4], "db")
            ms.append(data)
        # Close connection
        conn.close()

        return ms

    def save(self, date, data_list):
        # Connect the sqllite db, if not exist it will be created
        conn = sqlite3.connect('../Cheapestticket/data.db')
        cursor = conn.cursor()

        # Insert data
        for data in data_list:
            # print(f"save db {data}")
            cursor.execute('''
                INSERT INTO matches (website, time, team, price, query_time)
                VALUES (?, ?, ?, ?, ?)
            ''', (data.website, data.time, data.team, data.price, data.query_time))

        # Submit the modification and close the connection
        conn.commit()
        conn.close()
