import re
import json

# def parse_snmp_file(file_path):
#     interfaces = {}
    
#     with open(file_path, 'r') as file:
#         lines = file.readlines()
    
#     # Define regex patterns for different data types
#     oid_pattern = re.compile(r'iso\.3\.6\.1\.2\.1\.2\.2\.1\.(\d+)\.(\d+)')
#     int_pattern = re.compile(r'INTEGER: (\d+)')
#     string_pattern = re.compile(r'STRING: "(.*?)"')
#     gauge_pattern = re.compile(r'Gauge32: (\d+)')
#     hex_pattern = re.compile(r'Hex-STRING: (.*)')
#     timeticks_pattern = re.compile(r'Timeticks: \((\d+)\) (.*)')
#     counter_pattern = re.compile(r'Counter32: (\d+)')
    
#     for line in lines:
#         # Extract OID and value
#         match = oid_pattern.match(line)
#         if not match:
#             print(f"Invalid line: {line}")
#             continue
        
#         oid_index = int(match.group(2))
#         oid_value = line.split('=')[1].strip()
        
#         # Determine the data type and store the value
#         value = None
#         data_type = None
        
#         if 'Hex-STRING' in oid_value:
#             match = hex_pattern.search(oid_value)
#             if match:
#                 hex_value = match.group(1).replace(' ', ':')
#                 # Convert Hex-STRING to MAC address format
#                 value = hex_value
#                 data_type = 'Hex-STRING'
#         elif 'INTEGER' in oid_value:
#             match = int_pattern.search(oid_value)
#             if match:
#                 value = match.group(1)
#                 data_type = 'INTEGER'
#         elif 'STRING' in oid_value:
#             match = string_pattern.search(oid_value)
#             if match:
#                 value = match.group(1)
#                 data_type = 'STRING'
#         elif 'Gauge32' in oid_value:
#             match = gauge_pattern.search(oid_value)
#             if match:
#                 value = match.group(1)
#                 data_type = 'Gauge32'
#         elif 'Timeticks' in oid_value:
#             match = timeticks_pattern.search(oid_value)
#             if match:
#                 value = match.group(2)
#                 data_type = 'Timeticks'
#         elif 'Counter32' in oid_value:
#             match = counter_pattern.search(oid_value)
#             if match:
#                 value = match.group(1)
#                 data_type = 'Counter32'
#         else:
#             print(f"Unknown data type: {oid_value}")
#             continue

#         if value is not None and data_type is not None:
#             if oid_index not in interfaces:
#                 interfaces[oid_index] = {}
#                 print(f"OID Index: {oid_index}")
#             interfaces[oid_index][data_type] = value
#             print(f"Data Type: {data_type}, Value: {value}")
    
#     # Convert raw data to structured format
#     json_data = []
#     for idx, data in interfaces.items():
#         interface = {
#             "index": idx,
#             "description": data.get("STRING", ""),
#             "type": "Ethernet (10Mbps)" if "FastEthernet" in data.get("STRING", "") else "Unknown",
#             "mtu": int(data.get("INTEGER", 1500)),
#             "speed_bps": int(data.get("Gauge32", 10000000)),
#             "mac_address": data.get("Hex-STRING", ""),
#             "admin_status": "Up" if data.get("INTEGER") == "1" else "Down",
#             "oper_status": "Up" if data.get("INTEGER") == "1" else "Down",
#             "last_change": data.get("Timeticks", "0:00:00.00"),
#             "in_octets": int(data.get("Counter32", 0)),
#             "out_octets": int(data.get("Counter32", 0)),
#             "in_errors": int(data.get("Counter32", 0)),
#             "out_errors": int(data.get("Counter32", 0)),
#             "in_discards": int(data.get("Counter32", 0)),
#             "out_discards": int(data.get("Counter32", 0))
#         }
#         json_data.append(interface)
    
#     return json.dumps({"interfaces": json_data}, indent=4)

def parse_snmp_file(file_path):
    # Regular expressions for different data types
    oid_pattern = re.compile(r'^(\S+)\s*=\s*(\S+):\s*(.*)$')
    hex_pattern = re.compile(r'^(\S+)\s*=\s*Hex-STRING:\s*(.*)$')
    
    # Initialize data structure
    data = {
        "interfaces": []
    }
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
        oid_dict = {}

        for line in lines:
            match = oid_pattern.match(line)
            if match:
                oid, type_, value = match.groups()

                # Store value in a dictionary with OID as key
                oid_dict[oid] = value

    # Process the data to construct the final JSON structure
    interface_indexes = ['1', '2', '3', '5']  # Expected indexes based on provided example
    for index in interface_indexes:
        interface = {
            "index": int(index),
            "description": oid_dict.get(f'iso.3.6.1.2.1.2.2.1.2.{index}', ''),
            "type": "Ethernet (10Mbps)",
            "mtu": int(oid_dict.get(f'iso.3.6.1.2.1.2.2.1.4.{index}', 1)),
            "speed_bps": int(oid_dict.get(f'iso.3.6.1.2.1.2.2.1.5.{index}', 0)),
            "mac_address": parse_mac_address(oid_dict.get(f'iso.3.6.1.2.1.2.2.1.6.{index}', '')),
            "admin_status": parse_admin_status(int(oid_dict.get(f'iso.3.6.1.2.1.2.2.1.7.{index}', 1))),
            "oper_status": parse_oper_status(int(oid_dict.get(f'iso.3.6.1.2.1.2.2.1.8.{index}', 1))),
            "last_change": parse_last_change(oid_dict.get(f'iso.3.6.1.2.1.2.2.1.9.{index}', '')),
            "in_octets": int(oid_dict.get(f'iso.3.6.1.2.1.2.2.1.10.{index}', 0)),
            "out_octets": int(oid_dict.get(f'iso.3.6.1.2.1.2.2.1.11.{index}', 0)),
            "in_errors": int(oid_dict.get(f'iso.3.6.1.2.1.2.2.1.12.{index}', 0)),
            "out_errors": int(oid_dict.get(f'iso.3.6.1.2.1.2.2.1.13.{index}', 0)),
            "in_discards": int(oid_dict.get(f'iso.3.6.1.2.1.2.2.1.14.{index}', 0)),
            "out_discards": int(oid_dict.get(f'iso.3.6.1.2.1.2.2.1.15.{index}', 0)),
        }
        data["interfaces"].append(interface)

    return json.dumps(data, indent=4)

def parse_mac_address(hex_string):
    hex_string = hex_string.replace(' ', '')
    if len(hex_string) == 12:
        return ':'.join([hex_string[i:i+2] for i in range(0, 12, 2)]).upper()
    return ''

def parse_admin_status(value):
    return "Up" if value == 1 else "Down"

def parse_oper_status(value):
    return "Up" if value == 1 else "Down"

def parse_last_change(timeticks):
    if timeticks.startswith('('):
        return timeticks.split(' ')[1]
    return timeticks

file_path = '/home/agarwalvivek29/sih/infra-1708/snmp_data_interfaces.txt'
json_output = parse_snmp_file(file_path)
print(json_output)