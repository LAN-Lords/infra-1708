from utils.db.main import Database

database = Database()


def fetch_network_data():
    db = database.get_connection()
    cursor = db.cursor()
    try:
        # Fetching node and interface details
        get_nodes_query = """
            SELECT n.id AS node_id, n.host, i.interface, i.ip
            FROM nodes n
            JOIN interfaces i ON n.id = i.node_id
            ORDER BY n.id;
        """
        cursor.execute(get_nodes_query)
        nodes_pre = cursor.fetchall()

        # Fetching connections data
        get_connections_query = """
            SELECT id, ip1, ip2 FROM connections;
        """
        cursor.execute(get_connections_query)
        connections_pre = cursor.fetchall()

        print("Fetched network data successfully.")

        # Dictionary to group interfaces by node
        nodes_dict = {}

        # Process node/interface data
        for row in nodes_pre:
            node_id, host, interface, ip = row
            if node_id not in nodes_dict:
                nodes_dict[node_id] = {
                    "id": node_id,
                    "type": "pc",  # Assuming type is "pc" for all, adjust if necessary
                    "name": host,  # Host as the name of the node
                    "interfaces": []
                }

            # Append each interface to the corresponding node
            nodes_dict[node_id]["interfaces"].append({
                "ip": ip,
                "name": interface
            })

        # Convert dictionary to list of nodes
        nodes = list(nodes_dict.values())

        # Process connections data and format into JSON
        connections = []
        for conn in connections_pre:
            conn_id, ip1, ip2 = conn
            connections.append({
                "id": conn_id,
                "ip1": ip1,
                "ip2": ip2
            })

        # For debugging purposes
        print(f'Nodes: {nodes}')
        print(f'Connections: {connections}')

        # Return the structured data
        return {
            "nodes": nodes,
            "connections": connections
        }
    finally:
        cursor.close()
