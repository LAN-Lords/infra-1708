import os
from utils.syslog_parser import parse_syslog
from .ingester import Ingester

ingester = Ingester()

# Path to the syslog file
SYSLOG_FILE = "/var/log/network.log"

# Path to the file where the last read position is stored
POSITION_FILE = "/home/agarwalvivek29/sih/infra-1708/utils/syslog_track"

def get_last_read_position():
    """Retrieve the last read byte position from a file."""
    if os.path.exists(POSITION_FILE):
        with open(POSITION_FILE, 'r') as file:
            return int(file.read().strip())
    return 0

def save_last_read_position(position):
    """Save the current byte position to a file."""
    with open(POSITION_FILE, 'w') as file:
        file.write(str(position))

def read_new_data():
    """Read and process new data from the syslog file."""
    # Get the last read byte position
    last_position = get_last_read_position()

    # Open the syslog file
    with open(SYSLOG_FILE, 'r') as syslog:
        # Move to the last read position
        syslog.seek(last_position)

        # Read new lines from the syslog file
        new_data = syslog.readlines()

        if new_data:
            # Process the new data (print it in this case)
            # parse_syslog(new_data)
            for line in new_data:
                parsed_syslog = parse_syslog(line)
                if parsed_syslog:
                    ingester.ingest_syslog(parsed_syslog)
                    print(parsed_syslog)

            # Update the last read position
            new_position = syslog.tell()
            save_last_read_position(new_position)
        else:
            print("No new data to read.")

read_new_data()
