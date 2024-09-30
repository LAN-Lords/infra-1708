FROM debian:latest

# Install snmptrapd and required tools
RUN apt-get update && apt-get install -y snmpd snmptrapd postgresql-client

# Expose SNMP trap port
EXPOSE 162/udp

# Set up snmptrapd config
RUN echo "authCommunity log public" >> /etc/snmp/snmptrapd.conf

# Start snmptrapd as the entrypoint
CMD ["snmptrapd", "-f", "-Lo", "-C", "-c", "/etc/snmp/snmptrapd.conf"]