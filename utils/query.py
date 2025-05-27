from collections import namedtuple
import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor

DB_URI = "postgresql://neondb_owner:npg_37AbPhHWjLup@ep-tiny-base-a4t3tbvu-pooler.us-east-1.aws.neon.tech/pet-shop?sslmode=require"

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
        return e