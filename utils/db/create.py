from utils.db.main import Database

create_syslog_table = """
CREATE TABLE IF NOT EXISTS syslog (
    id SERIAL PRIMARY KEY,
    recv_date TIMESTAMP,
    occur_date TIMESTAMP,
    ip VARCHAR(45),
    system VARCHAR(255),
    severity VARCHAR(50),
    event VARCHAR(255),
    message TEXT
);
"""

create_netflow_table = """
CREATE TABLE IF NOT EXISTS netflow (
    id SERIAL PRIMARY KEY,
    date_first_seen TIMESTAMP,
    event VARCHAR(255),
    xevent VARCHAR(255),
    proto VARCHAR(50),
    src_ip VARCHAR(45),
    src_port INTEGER,
    dst_ip VARCHAR(45),
    dst_port INTEGER,
    x_src_ip VARCHAR(45),
    x_src_port INTEGER,
    x_dst_ip VARCHAR(45),
    x_dst_port INTEGER,
    in_bytes BIGINT,
    out_bytes BIGINT
);
"""

create_nodes_table = """
CREATE TABLE IF NOT EXISTS nodes (
    id SERIAL PRIMARY KEY,
    host VARCHAR(255) NOT NULL UNIQUE
);
"""

create_interfaces_table = """
CREATE TABLE IF NOT EXISTS interfaces (
    id SERIAL PRIMARY KEY,
    node_id INTEGER REFERENCES nodes(id),
    interface VARCHAR(255),
    ip VARCHAR(15) UNIQUE
);
"""

create_connections_table = """
CREATE TABLE IF NOT EXISTS connections (
    id SERIAL PRIMARY KEY,
    ip1 VARCHAR(15) NOT NULL,
    ip2 VARCHAR(15) NOT NULL
);
"""

create_status_table = """
CREATE TABLE IF NOT EXISTS status (
    id SERIAL PRIMARY KEY,
    status VARCHAR(255) NOT NULL,
    message TEXT,
    node_id INTEGER REFERENCES nodes(id)
);
"""

def create_tables():
    conn = Database.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(create_syslog_table)
        cursor.execute(create_netflow_table)
        cursor.execute(create_nodes_table)
        cursor.execute(create_interfaces_table)
        cursor.execute(create_connections_table)
        cursor.execute(create_status_table)
        conn.commit()
        print("Tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")
        conn.rollback()
    finally:
        cursor.close()

create_tables()