import psycopg2
from psycopg2.extras import RealDictCursor

class Database:
    _connection = None

    @staticmethod
    def get_connection():
        if Database._connection is None:
            Database._connection = psycopg2.connect(
                dbname="sih1708",
                user="username",
                password="QnSsviHA9e7g",
                host="ep-ancient-queen-a1nkd2pi.ap-southeast-1.aws.neon.tech",
                port="5432"
            )
        return Database._connection

    @staticmethod
    def get_cursor():
        conn = Database.get_connection()
        return conn.cursor(cursor_factory=RealDictCursor)

    @staticmethod
    def close_connection():
        if Database._connection is not None:
            Database._connection.close()
            Database._connection = None

# import pg8000

# class Database:
#     _connection = None

#     @staticmethod
#     def get_connection():
#         if Database._connection is None:
#             Database._connection = pg8000.connect(
#                 database="sih1708",
#                 user="myuser",
#                 password="mypassword",
#                 host="localhost",
#                 port=5432
#             )
#         return Database._connection

#     @staticmethod
#     def cursor():
#         conn = Database.get_connection()
#         # pg8000 uses a standard cursor, so no need for RealDictCursor
#         return conn.cursor()

#     @staticmethod
#     def close_connection():
#         if Database._connection is not None:
#             Database._connection.close()
#             Database._connection = None
