from utils.db.main import Database

database = Database()

def fetch_syslog_data():
    db = database.get_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM syslog")
        data = cursor.fetchall()
        print("Fetched syslog data successfully.")
        print(data)
        return data
    finally:
        cursor.close()