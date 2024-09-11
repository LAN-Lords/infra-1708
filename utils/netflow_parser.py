import re

netflow_pattern = re.compile(
    r'(?P<date_first_seen>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})\s+'
    r'(?P<event>\w+)\s+'
    r'(?P<xevent>\w+)\s+'
    r'(?P<proto>\w+)\s+'
    r'(?P<src_ip>\d{1,3}(?:\.\d{1,3}){3}):(?P<src_port>\d+)\s+->\s+'
    r'(?P<dst_ip>\d{1,3}(?:\.\d{1,3}){3}):(?P<dst_port>\d+)\s+'
    r'(?P<x_src_ip>\d{1,3}(?:\.\d{1,3}){3}):(?P<x_src_port>\d+)\s+->\s+'
    r'(?P<x_dst_ip>\d{1,3}(?:\.\d{1,3}){3}):(?P<x_dst_port>\d+)\s+'
    r'(?P<in_bytes>\d+)\s+(?P<out_bytes>\d+)'
)

def parse_netflow(log):
    match = netflow_pattern.match(log)
    if match:
        log_entry = {
            'date_first_seen': match.group('date_first_seen'),
            'event': match.group('event'),
            'xevent': match.group('xevent'),
            'proto': match.group('proto'),
            'src_ip': match.group('src_ip'),
            'src_port': int(match.group('src_port')),
            'dst_ip': match.group('dst_ip'),
            'dst_port': int(match.group('dst_port')),
            'x_src_ip': match.group('x_src_ip'),
            'x_src_port': int(match.group('x_src_port')),
            'x_dst_ip': match.group('x_dst_ip'),
            'x_dst_port': int(match.group('x_dst_port')),
            'in_bytes': int(match.group('in_bytes')),
            'out_bytes': int(match.group('out_bytes'))
        }
        print(log_entry)
        return log_entry
    else:
        print("No match found")
        return None
