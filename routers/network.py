from utils.db.main import Database

database = Database()

def fetch_network_data():
    db = database.get_connection()
    cursor = db.cursor()
    try:
        get_nodes_query = """
            SELECT 
                n.host,
                json_agg(
                    json_build_object(
                        'interface', i.interface,
                        'ip', i.ip
                    )
                ) AS interfaces
            FROM nodes n
            JOIN interfaces i ON n.id = i.node_id
            GROUP BY n.host;
        """

        cursor.execute(get_nodes_query)
        nodes_pre = cursor.fetchall()

        get_connections_query = """
            SELECT * FROM connections
        """

        cursor.execute(get_connections_query)
        connections = cursor.fetchall()

        print("Fetched network data successfully.")

        print(f'Nodes: {nodes_pre}')
        print(f'Connections: {connections}')

        return {
            "nodes": nodes_pre,
            "connections": connections
        }
    finally:
        cursor.close()

# fetch_network_data()
