from utils.db.main import Database

database = Database()


def fetch_netflow_data():
    db = database.get_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM netflow")
        data = cursor.fetchall()
        print("Fetched netflow data successfully.")
        #print(data)
        return data
    finally:
        cursor.close()

# fetch_netflow_data()
