from collections import namedtuple
import os
import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor

DB_URI = os.getenv("DATABASE_URL")

try:
    connection = psycopg2.connect(DB_URI)
    connection.autocommit = True
except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL:", error)
    connection = None

def map_cursor(cursor):
    """Return all rows from a cursor as a list of dictionaries."""
    return [dict(row) for row in cursor.fetchall()]

def query(query_str: str):
    """Execute SQL query and return result or affected row count."""
    if connection is None:
        return "No database connection."

    try:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SET SEARCH_PATH TO petclinic;")
            cursor.execute(query_str)

            if query_str.strip().upper().startswith("SELECT"):
                return map_cursor(cursor)
            else:
                return cursor.rowcount
            
    except Exception as e:
        error_message = str(e)
        context_delimiter = "\nCONTEXT:"

        delimiter_index = error_message.find(context_delimiter)

        if delimiter_index != -1:
            cleaned_message = error_message[:delimiter_index]
        else:
            cleaned_message = error_message
        return {"status": "error", "data": cleaned_message}