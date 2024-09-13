import re
import json

# Function to parse system description
def parse_system_description(data):
    match = re.search(r'iso\.3\.6\.1\.2\.1\.1\.1\.0 = STRING: "(.*?)"', data, re.DOTALL)
    return match.group(1).strip() if match else "Not found"

# Function to parse system object ID
def parse_system_object_id(data):
    match = re.search(r'iso\.3\.6\.1\.2\.1\.1\.2\.0 = OID: (iso\.\d+(\.\d+)*)', data)
    return match.group(1) if match else "Not found"

# Function to parse system uptime
def parse_system_uptime(data):
    match = re.search(r'iso\.3\.6\.1\.2\.1\.1\.3\.0 = Timeticks: \((\d+)\) (\d+ day[s]?, \d+:\d+:\d+\.\d+)', data)
    if match:
        return {
            "uptime_ticks": match.group(1),
            "uptime_formatted": match.group(2)
        }
    return {"uptime_ticks": "Not found", "uptime_formatted": "Not found"}

# Function to parse system contact
def parse_system_contact(data):
    match = re.search(r'iso\.3\.6\.1\.2\.1\.1\.4\.0 = "(.*?)"', data)
    return match.group(1).strip() if match else "Not found"

# Function to parse system name
def parse_system_name(data):
    match = re.search(r'iso\.3\.6\.1\.2\.1\.1\.5\.0 = STRING: "(.*?)"', data)
    return match.group(1).strip() if match else "Not found"

# Function to parse system location
def parse_system_location(data):
    match = re.search(r'iso\.3\.6\.1\.2\.1\.1\.6\.0 = "(.*?)"', data)
    return match.group(1).strip() if match else "Not found"

# Function to parse system services
def parse_system_services(data):
    match = re.search(r'iso\.3\.6\.1\.2\.1\.1\.7\.0 = INTEGER: (\d+)', data)
    return match.group(1) if match else "Not found"

# Function to parse system performance
def parse_system_performance(data):
    match = re.search(r'iso\.3\.6\.1\.2\.1\.1\.8\.0 = Timeticks: \((\d+)\) (\d+:\d+:\d+\.\d+)', data)
    if match:
        return {
            "performance_ticks": match.group(1),
            "performance_formatted": match.group(2)
        }
    return {"performance_ticks": "Not found", "performance_formatted": "Not found"}

# Function to read SNMP data from a file
def read_snmp_data(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Main function to parse SNMP data and generate JSON output
def parse_snmp_system_data(file_path):
    # Read SNMP data from file
    snmp_data = read_snmp_data(file_path)
    
    # Parse data
    data = {
        "system_description": parse_system_description(snmp_data),
        "system_object_id": parse_system_object_id(snmp_data),
        "system_uptime": parse_system_uptime(snmp_data),
        "system_contact": parse_system_contact(snmp_data),
        "system_name": parse_system_name(snmp_data),
        "system_location": parse_system_location(snmp_data),
        "system_services": parse_system_services(snmp_data),
        "system_performance": parse_system_performance(snmp_data)
    }
    
    # Output JSON
    return json.dumps(data, indent=4)

# Path to the file containing SNMP data
file_path = '/home/agarwalvivek29/sih/infra-1708/snmp_data_system.txt'

# Generate and print JSON output
json_output = parse_snmp_system_data(file_path)
print(json_output)