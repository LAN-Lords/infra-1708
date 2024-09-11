from utils.db.main import Database

class Ingester:
    def __init__(self):
        self.db = Database()

    def ingest_syslog(self, data):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO syslog (recv_date, occur_date, ip, system, severity, event, message)
                VALUES (%(recv_date)s, %(occur_date)s, %(ip)s, %(system)s, %(severity)s, %(event)s, %(message)s)
                """,
                data
            )
            conn.commit()  # Commit the transaction
            print("Syslog entry inserted successfully.")
        except Exception as e:
            print(f"Error inserting syslog entry: {e}")
            conn.rollback()  # Rollback in case of error
        finally:
            cursor.close()  # Always close the cursor

    def ingest_netflow(self, data):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO netflow (date_first_seen, event, xevent, proto, src_ip, src_port, dst_ip, dst_port,
                    x_src_ip, x_src_port, x_dst_ip, x_dst_port, in_bytes, out_bytes)
                VALUES (%(date_first_seen)s, %(event)s, %(xevent)s, %(proto)s, %(src_ip)s, %(src_port)s, %(dst_ip)s, %(dst_port)s,
                        %(x_src_ip)s, %(x_src_port)s, %(x_dst_ip)s, %(x_dst_port)s, %(in_bytes)s, %(out_bytes)s)
                """,
                data
            )
            conn.commit()  # Commit the transaction
            print("NetFlow log inserted successfully.")
        except Exception as e:
            print(f"Error inserting netflow log: {e}")
            conn.rollback()  # Rollback in case of error
        finally:
            cursor.close()  # Always close the cursor

    def ingest_network(self, nodes, connections):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            for node in nodes:
                cursor.execute(
                    """
                    INSERT INTO nodes (host)
                    VALUES (%s)
                    ON CONFLICT (host) DO NOTHING
                    """,
                    (node["host"],)
                )
                for interface in node["interfaces"]:
                    cursor.execute(
                        """
                        INSERT INTO interfaces (node_id, interface, ip)
                        VALUES ((SELECT id FROM nodes WHERE host = %s), %s, %s)
                        """,
                        (node["host"], interface["interface"], interface["ip"])
                    )
            for connection in connections:
                cursor.execute(
                    """
                    INSERT INTO connections (ip1, ip2)
                    VALUES (%s, %s)
                    """,
                    connection
                )
            conn.commit()  # Commit the transaction
            print("Network data inserted successfully.")
        except Exception as e:
            print(f"Error inserting network data: {e}")
            conn.rollback()