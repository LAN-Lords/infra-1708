import re
import json
from collections import defaultdict

def interpret_status_code(value):
    status_codes = {
        0: "Unavailable",
        1: "Active",
        2: "Static",
        3: "Dynamic"
    }
    return status_codes.get(value, "Unknown")

def interpret_integer_value(value):
    # Interpretation of values based on general meanings
    if value == 0:
        return "No Data"
    elif value > 0 and value <= 10:
        return "Low Count"
    elif value > 10 and value <= 100:
        return "Moderate Count"
    elif value > 100:
        return "High Count"
    else:
        return "Special or Error"

def interpret_subnet_mask(mask):
    subnet_masks = {
        "255.0.0.0": "Class A Network",
        "255.255.0.0": "Class B Network",
        "255.255.255.0": "Class C Network",
        "0.0.0.0": "No Mask"
    }
    return subnet_masks.get(mask, "Unknown")

def interpret_additional_status(value):
    if value == -1:
        return "Error or Not Applicable"
    else:
        return "Unknown"

# def parse_snmp_file(filename):
#     data = {}
    
#     with open(filename, 'r') as file:
#         content = file.read()

#         oid_pattern = re.compile(r'(iso\.3\.6\.1\.2\.1(?:\.\d+)+) = (IpAddress|INTEGER|STRING|Timeticks|Counter32): (.+)')
        
#         for match in oid_pattern.finditer(content):
#             oid = match.group(1)
#             value_type = match.group(2)
#             value = match.group(3).strip()

#             # # Print OID, type, and value for debugging
#             # print(f"OID: {oid}, Type: {value_type}, Value: {value}")

#             # Convert values based on type
#             if value_type == "INTEGER":
#                 value = int(value)
#                 if '1.2.1.4.21' in oid:
#                     value = interpret_integer_value(value)
#                 else:
#                     value = str(value)
#             elif value_type == "IpAddress":
#                 value = str(value)
#             elif value_type == "STRING" or value_type == "Timeticks":
#                 value = str(value)
#             elif value_type == "Counter32":
#                 value = int(value)

#             # Split the OID to get the hierarchical levels
#             oid_parts = oid.split('.')
#             if '1.2.1.4.21' in oid:
#                 key = f"{'.'.join(oid_parts[8:])}"
#                 if key not in data:
#                     data[key] = {}
#                 data[key][oid_parts[-1]] = value

#     # Generate JSON output
#     json_output = {}
#     for key, metrics in data.items():
#         json_output[key] = {
#             "status": interpret_status_code(metrics.get('1', -1)),
#             "related_ip": metrics.get('7', 'N/A'),
#             "count": metrics.get('8', 'N/A'),
#             "detailed_statistic": metrics.get('10', 'N/A'),
#             "subnet_mask": interpret_subnet_mask(metrics.get('11', '0.0.0.0')),
#             "additional_status": interpret_additional_status(metrics.get('12', -1)),
#             "classification": metrics.get('13', 'N/A')
#         }
    
#     return json.dumps(json_output, indent=4)

def parse_snmp_file(filename):
    data = {}
    
    with open(filename, 'r') as file:
        content = file.read()
        
        # Regular expression to match OID lines
        oid_pattern = re.compile(r'iso\.3\.6\.1\.2\.1\.(\d+)\.(\d+)\.(\d+)\.(\d+)\.(\d+)\.(\d+)\.(\d+)\.(\d+) = (IpAddress|INTEGER|STRING|Timeticks|Counter32): (.*)')
        
        for match in oid_pattern.finditer(content):
            oid = match.group(0).split(' = ')[0]
            value_type = match.group(8)
            value = match.group(9)
            
            # Split the OID to get the hierarchical levels
            oid_parts = oid.split('.')
            last_oid_part = oid_parts[-1]
            
            # Convert values based on type
            if value_type == "INTEGER":
                value = int(value)
                if '1.2.1.4.21' in oid:
                    value = interpret_integer_value(value)
                else:
                    value = str(value)
            elif value_type == "IpAddress":
                value = str(value)
            elif value_type == "STRING" or value_type == "Timeticks":
                value = str(value)
            elif value_type == "Counter32":
                value = int(value)
            
            # Build dictionary structure
            if '1.2.1.4.21' in oid:
                key = f"{'.'.join(oid_parts[8:])}"
                if key not in data:
                    data[key] = {}
                data[key][last_oid_part] = value
            
    # Generate JSON output
    json_output = {}
    for key, metrics in data.items():
        json_output[key] = {
            "status": interpret_status_code(metrics.get('1', -1)),
            "related_ip": metrics.get('7', 'N/A'),
            "count": metrics.get('8', 'N/A'),
            "detailed_statistic": metrics.get('10', 'N/A'),
            "subnet_mask": interpret_subnet_mask(metrics.get('11', '0.0.0.0')),
            "additional_status": interpret_additional_status(metrics.get('12', -1)),
            "classification": metrics.get('13', 'N/A')
        }
    
    return json.dumps(json_output, indent=4)

# def parse_snmp_file(filename):
#     data = defaultdict(lambda: {
#         "status": "Unknown",
#         "related_ip": "N/A",
#         "count": "N/A",
#         "detailed_statistic": "N/A",
#         "subnet_mask": "No Mask",
#         "additional_status": "Error or Not Applicable",
#         "classification": "N/A"
#     })

#     with open(filename, 'r') as file:
#         content = file.read()
        
#         # Refined regular expression to match OID lines
#         oid_pattern = re.compile(r'(iso\.3\.6\.1\.2\.1(?:\.\d+)+) = (IpAddress|INTEGER|STRING|Timeticks|Counter32): (.+)')
        
#         for match in oid_pattern.finditer(content):
#             oid = match.group(1)
#             value_type = match.group(2)
#             value = match.group(3).strip()

#             # Convert values based on type
#             if value_type == "INTEGER":
#                 value = int(value)
#                 if '1.2.1.4.21' in oid:
#                     value = interpret_integer_value(value)
#             elif value_type == "IpAddress":
#                 # Handle IP addresses correctly
#                 if re.match(r'\d+\.\d+\.\d+\.\d+', value):
#                     value = str(value)
#                 else:
#                     value = "Invalid IP"
#             elif value_type == "STRING" or value_type == "Timeticks":
#                 value = str(value)
#             elif value_type == "Counter32":
#                 value = int(value)

#             # Split the OID to get the hierarchical levels
#             oid_parts = oid.split('.')
#             prefix = f"{'.'.join(oid_parts[:4])}"  # Adjusted for more general prefix

#             if '1.2.1.4.21' in oid:
#                 metric_key = oid_parts[-1]
#                 data[prefix][metric_key] = value

#     # Consolidate results
#     consolidated_data = {}
#     for prefix, metrics in data.items():
#         consolidated_data[prefix] = {
#             "status": interpret_status_code(metrics.get('1', -1)),
#             "related_ip": metrics.get('7', 'N/A'),
#             "count": metrics.get('8', 'N/A'),
#             "detailed_statistic": metrics.get('10', 'N/A'),
#             "subnet_mask": interpret_subnet_mask(metrics.get('11', '0.0.0.0')),
#             "additional_status": interpret_additional_status(metrics.get('12', -1)),
#             "classification": metrics.get('13', 'N/A')
#         }

#     return json.dumps(consolidated_data, indent=4)

# Usage example
file_path = '/home/agarwalvivek29/sih/infra-1708/snmp_data_ip_tables.txt'
parsed_data = parse_snmp_file(file_path)
print(parsed_data)