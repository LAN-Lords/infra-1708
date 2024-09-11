# write a cron-job to fetch data from logs and netflow dump files and ingest

import os
import subprocess
from utils.netflow_parser import parse_netflow

# Define the directory where the nfcapd files are stored
DIRECTORY = "/var/cache/nfdump"

# Define the file that stores the last processed timestamp
LAST_PROCESSED_FILE = "/home/agarwalvivek29/sih/infra-1708/utils/netflow_track"

def get_last_processed_timestamp():
    """Reads the last processed timestamp from a file."""
    if os.path.exists(LAST_PROCESSED_FILE):
        with open(LAST_PROCESSED_FILE, 'r') as file:
            return file.read().strip()
    return "0"

def set_last_processed_timestamp(timestamp):
    """Writes the last processed timestamp to a file."""
    with open(LAST_PROCESSED_FILE, 'w') as file:
        file.write(timestamp)

def parse_nfdump_file(file_path):
    """Parses and prints the contents of the nfdump file."""
    try:
        # Run the nfdump command to parse the file
        output = subprocess.check_output(["nfdump", "-r", file_path], universal_newlines=True)
        for line in output.splitlines():
            parse_netflow(line)
    except subprocess.CalledProcessError as e:
        print(f"Error parsing file {file_path}: {e}")

def process_new_files():
    """Finds and processes new nfcapd files."""
    # Get the last processed timestamp
    last_processed_timestamp = get_last_processed_timestamp()

    # Get the list of files in the directory, sorted by timestamp
    files = sorted([f for f in os.listdir(DIRECTORY) if f.startswith('nfcapd.')])

    for file in files:
        # Extract the timestamp from the file name (e.g., nfcapd.202409080610 -> 202409080610)
        timestamp = file.split('.')[1]

        # Process the file only if its timestamp is greater than the last processed one
        if timestamp > last_processed_timestamp and timestamp != 'current':
            file_path = os.path.join(DIRECTORY, file)
            print(f"Processing new file: {file_path}")
            parse_nfdump_file(file_path)

            # Update the last processed timestamp
            set_last_processed_timestamp(timestamp)

# process_new_files()
