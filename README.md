# Infra SCADA_Network_Topology_Discovery_Tool

## FastAPI Server

- Start the virtual env
  `source venv\Scripts\activate`

- Run the fast api server
  `uvicorn main:app --reload`


# Router Commands Documentation

## Enabling Telnet on a Router

```bash
   config t
   line vty 0 4
   password password
   login
   exit
   enable secret password
   exit
   write memory
```

## Netflow

### reciever server

```bash
sudo nfcapd -w -D -l /var/cache/nfdump/
```
- default port - 9995

### Enabling data-capture on router

```bash
configure terminal
ip flow-export version 9
ip flow-export destination 192.168.100.1 9995
ip flow-cache timeout active 1
ip flow-cache timeout inactive 15
interface FastEthernet 0/0
ip flow ingress
ip flow egress
exit
interface FastEthernet 0/1
ip flow ingress
ip flow egress
exit
interface FastEthernet 1/0
ip flow ingress
ip flow egress
exit
exit
write memory
```

## snmpv3

### snmpwalk querying

```bash
snmpwalk -v3 -u username -A password -X password -l authPriv -a SHA -x DES <ip/> <oid/>
```

### router-setup

```bash
configure terminal
snmp-server group my_group v3 noauth
snmp-server user my_user my_group v3
exit
write memory
```

### snmpwalk OID's

```plaintext
Interfaces info - iso.3.6.1.2.1.2.2.1
System info - iso.1.3.6.1.2.1.1
IP-Tables info - iso.1.3.6.1.2.1.4.21
```
### verification

```bash
show snmp group
show snmp user
```

### debugging

```bash
debug snmp packets
debug snmp requests
debug snmp headers
```

## misc

### tcpdump listener

```bash
sudo tcpdump -i <interface> udp port <port>
```

### tap interface

```plaintext
interface - tap1
ip - 192.168.100.1
mask - 255.255.255.0
```

### recievers

```plaintext
rsyslog - syslog
nfcapd - netflow
snmptrapd - snmpv3
```

