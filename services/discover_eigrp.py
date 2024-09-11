from netmiko import ConnectHandler
import re
from .ingester import Ingester

global nodes 
global connections 
global visited 
global queue 

ingester = Ingester()

def bfs():
    nodes = []
    connections = set()
    visited = []
    queue = {'192.168.100.5'}

    count = 0
    while len(queue)> 0:
        node, links, eigrp_ips, visited_ips = get_adjacent_nodes(queue.pop())
        nodes.append(node)
        connections = set(connections.union(links))
        visited = set(visited).union(visited_ips)
        queue = set(queue).union(eigrp_ips) - visited

        print(f"Iteration {count}")
        print(f'Visited: {visited}\n')
        print(f'Queue: {queue}\n')
        count += 1
    
    ingester.ingest_network(nodes, connections)
    print(f'\n\nNodes: {nodes}\n')
    print(f'Connections: {connections}\n')

def parse_eigrp_neighbors(telnet_output):
    # Regex pattern to match only lines with valid IP and interface
    pattern = r"(\d+\.\d+\.\d+\.\d+)\s+(\S+)"

    # Find all matches using regex
    matches = re.findall(pattern, telnet_output)

    # Convert matches to the required list of dictionaries
    result = [{"interface": interface, "ip": ip} for ip, interface in matches]

    for node in result:
        node["interface"] = node["interface"].replace("Fa", "FastEthernet")

    return result

def parse_ip_brief(telnet_output):
    # Regex pattern to match interfaces with valid IP addresses
    pattern = r"(\S+)\s+(\d+\.\d+\.\d+\.\d+)\s+YES"

    # Find all matches using regex
    matches = re.findall(pattern, telnet_output)

    # Convert matches to the required list of dictionaries
    result = [{"interface": interface, "ip": ip} for interface, ip in matches]

    return result

def get_adjacent_nodes(IP):
    device = {
        'device_type': 'cisco_ios_telnet',
        'port': 23,
        'host': IP,
        'password': 'password',
        'secret': 'password'
    }

    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()
        print(f'Connected to {IP}')

        host = net_connect.send_command('show running-config | include hostname')
        interfaces = net_connect.send_command('show ip interface brief')
        eigrp_neighbors = net_connect.send_command('show ip eigrp neighbors')

        hostname = host.split(' ')[1]
        print(f'Host: {hostname}')

        parsed_interfaces = parse_ip_brief(interfaces)
        print('Parsed Interfaces')
        print(parsed_interfaces, '\n')

        parsed_eigrp_neighbors = parse_eigrp_neighbors(eigrp_neighbors)
        print('Parsed EIGRP Neighbors')
        print(parsed_eigrp_neighbors, '\n')
        net_connect.disconnect()

        links = set()
        for node1 in parsed_eigrp_neighbors:
            for node2 in parsed_interfaces:
                if node1["interface"] == node2["interface"]:
                    links.add((min(node1["ip"],node2["ip"]), max(node1["ip"],node2["ip"])))

        neighboring_eigrp_ips = [node["ip"] for node in parsed_eigrp_neighbors]
        visited_ips = [node["ip"] for node in parsed_interfaces]
        
        print(f'Connections: {links}\n')
        
        return {
            "host": hostname,
            "interfaces" : parsed_interfaces
        }, links, neighboring_eigrp_ips, visited_ips
    except Exception as e:
        print(e)
        return []
    
bfs()