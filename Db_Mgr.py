import psycopg2
import psycopg2.extras
import creds
import json

class Db_Mgr:

    def db_connect(self):
        try:
            conn_string = f"dbname='{creds.db_name}' user='{creds.user_name}' password='{creds.password}' host='localhost' port=5432"
            self.connection = psycopg2.connect(conn_string)
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            return cursor
        except Exception as e:
            print(e)

    def execute_query(self, query):
        try:
            results = list()
            cursor = self.db_connect()
            cursor.execute(query)
            response = cursor.fetchall()

            # Create a list of results rows
            for row in response:
                results.append(row)

            print(f"The results for {query}: {results}")
            json_results = json.dumps(results)
            return json_results
        except Exception as e:
            print(e)

    def insert_update(self, query):
        try:
            cursor = self.db_connect()
            cursor.execute(query)
            self.connection.commit()
            self.connection.close()
            return {"Successful": True}
        except Exception as e:
            print(e)
            return {"Successful": False}
