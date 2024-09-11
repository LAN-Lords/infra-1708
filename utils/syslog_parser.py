import re
from datetime import datetime

log_pattern = re.compile(
    r'(?P<recv_date>\w{3} +\d{1,2} +\d{2}:\d{2}:\d{2}) (?P<ip>\d{3}\.\d{3}\.\d{3}\.\d{1,3}) \d+: \*(?P<occur_date>\w{3} +\d{1,2} +\d{2}:\d{2}:\d{2}\.\d+): %(?P<system>[\w-]+)-(?P<severity>\d+)-(?P<event>\w+): (?P<message>.+)'
)

def parse_syslog(log):
    match = log_pattern.match(log)
    if not match:
        print(f"Failed to parse log: {log}")
        return None

    recv_date = datetime.strptime(match.group('recv_date'), '%b %d %H:%M:%S')
    occur_date = datetime.strptime(match.group('occur_date'), '%b %d %H:%M:%S.%f')
    severity = int(match.group('severity'))
    event = match.group('event')
    message = match.group('message').strip()
    ip = match.group('ip')

    log_entry = {
        'recv_date': recv_date,
        'occur_date': occur_date,
        'ip': ip,
        'system': match.group('system'),
        'severity': severity,
        'event': event,
        'message': message
    }
    print(log_entry)
    return log_entry