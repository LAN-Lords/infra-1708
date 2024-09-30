from services.cron_netflow import process_netflow_data
from services.cron_syslog import process_syslog_data
from services.discover_eigrp import discover_network

def main():
    """Main entry point of the application."""
    # Discover network topology
    discover_network()

    # Process netflow data
    process_netflow_data()

    # Process syslog data
    process_syslog_data()

if __name__ == "__main__":
    main()