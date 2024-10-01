# SCADA Network Topology Discovery Solution - Technical Documentation

## 1. Introduction

The SCADA Network Topology Discovery solution is an advanced, secure, and automated system designed for mapping and monitoring critical infrastructure networks. This document provides in-depth technical insights into the solution's architecture, protocols, security measures, and operational workflow.

### 1.1 Solution Overview

Our solution leverages a combination of robust networking protocols and security measures:

- **EIGRP** (Enhanced Interior Gateway Routing Protocol) for efficient and secure routing
- **SNMPv3** (Simple Network Management Protocol version 3) for secure device management and monitoring
- **Syslog with TLS** (Transport Layer Security) for encrypted event logging
- **NetFlow with IPsec** (Internet Protocol Security) for secure traffic analysis
- **Automated malicious device detection and response** using SNMP SET operations
- **QoS** (Quality of Service) for traffic prioritization

### 1.2 Key Innovations

1. **Enhanced Security**: Elimination of vulnerable protocols like CDP/LLDP in favor of more secure alternatives.
2. **Real-time Monitoring**: Integration of multiple protocols for comprehensive, up-to-the-minute network visibility.
3. **Bandwidth Optimization**: Implementation of syslog throttling and NetFlow sampling to manage network load.
4. **Automated Threat Response**: Immediate isolation of unauthorized devices to maintain network integrity.
5. **Traffic Prioritization**: QoS implementation to ensure SCADA operations remain unaffected by monitoring traffic.

## 2. Detailed Component Analysis

### 2.1 EIGRP-Based Topology Mapping

#### Technical Implementation
- **Protocol**: EIGRPv6 (for IPv6 support)
- **Authentication**: MD5 or SHA-256 for neighbor authentication
- **Stub Routing**: Implemented on edge routers to minimize routing table size
- **Route Summarization**: Configured at distribution layer for efficient routing

#### Data Collection Method
1. SNMP polling of EIGRP-specific MIB (Management Information Base)
2. Key OIDs:
   - `ciscoEigrpMIB::cEigrpTopologyEntry`
   - `ciscoEigrpMIB::cEigrpNeighborEntry`
3. Polling Frequency: Every 5 minutes (configurable)

#### Topology Construction Algorithm
1. Collect EIGRP neighbor information and topology tables from all routers
2. Build a graph representation where:
   - Nodes = Routers
   - Edges = EIGRP neighbor relationships
3. Apply Dijkstra's algorithm to determine shortest paths
4. Generate a visual representation using D3.js

### 2.2 SNMPv3 for Device Management and Monitoring

#### Configuration Details
- **Security Level**: AuthPriv (authentication and privacy)
- **Authentication Protocol**: SHA-256
- **Privacy Protocol**: AES-256
- **Context Name**: "SCADA_CONTEXT" (for logical separation of SNMP data)

#### Initial Device Identification and Data Collection
- **Trigger**: Performed when a new device is first detected on the network
- **Process**:
  1. SNMP GET operations are used to retrieve device information:
     - sysDescr (device type, OS version)
     - sysObjectID (vendor-specific identifier)
     - sysName (configured device name)
  2. Interface data collection:
     - ifTable is queried to get all interfaces
     - For each interface: ifDescr, ifType, ifPhysAddress (MAC address), ifAdminStatus, ifOperStatus
  3. IP address data collection:
     - ipAddrTable or ipAddressTable (depending on IP version support) is queried
     - Collected data includes IP addresses associated with each interface
- **Data Storage**: All collected data is stored in a centralized database for future reference and analysis

#### SNMP Polling
- **Polling Interval**: 60 seconds for critical metrics, 5 minutes for non-critical
- **Key Metrics Polled**:
  - Interface status (ifOperStatus, ifAdminStatus)
  - CPU utilization (cpmCPUTotal5minRev)
  - Memory usage (ciscoMemoryPoolUsed)
  - Error counters (ifInErrors, ifOutErrors)

#### Routing Table Polling
- **Initial Poll**: Performed once when a device is first added to the network
- **Subsequent Polls**: Triggered by specific events rather than on a regular schedule
- **Trigger Events**:
  1. Receipt of an SNMPv3 trap indicating a new device detection
  2. Receipt of an SNMPv3 trap indicating a route change
  3. Manual request by network administrator
- **Polling Process**:
  1. SNMP GET operations are used to retrieve the routing table (ipRouteTable or ipCidrRouteTable)
  2. Collected data includes destination networks, next hops, and metrics
  3. The topology graph is updated with the new routing information
- **Optimization**: This event-driven approach reduces unnecessary network traffic and processing load

#### SNMP Trap Configuration
- **Trap Types**:
  - linkDown, linkUp
  - authenticationFailure
  - bgpEstablished, bgpBackwardTransition (for BGP-enabled edges)
  - eigrpAuthFailure (custom trap for EIGRP authentication failures)
  - **newDeviceDetected**: Custom trap for indicating the detection of a new device
  - **routeChanged**: Custom trap for indicating changes in the routing table
- **Trap Throttling**: Maximum 10 traps per second per device

### 2.3 Syslog for Event Logging

#### TLS Configuration
- **TLS Version**: 1.3
- **Cipher Suite**: TLS_AES_256_GCM_SHA384
- **Certificate Management**: Let's Encrypt for server certificates, with automatic renewal

#### Syslog Server Setup
- **Software**: rsyslog v8.2102.0
- **Storage**: Elasticsearch for log indexing and searching
- **Visualization**: Kibana dashboards for real-time log analysis

#### Syslog Throttling Implementation
- **Method**: Token Bucket Algorithm
- **Parameters**:
  - Bucket Size: 100 messages
  - Refill Rate: 10 tokens per second
- **Overflow Handling**: Store locally and forward when network allows

### 2.4 NetFlow for Traffic Monitoring

#### NetFlow Configuration
- **Version**: NetFlow v9
- **Sampling Rate**: 1:100 (1 packet sampled out of every 100)
- **Active Flow Timeout**: 60 seconds
- **Inactive Flow Timeout**: 15 seconds

#### IPsec Configuration for NetFlow
- **Mode**: Transport Mode
- **Protocol**: ESP (Encapsulating Security Payload)
- **Encryption**: AES-GCM-256
- **Perfect Forward Secrecy**: Enabled with DH Group 14

#### NetFlow Collection and Analysis
- **Collector**: nfdump/nfcapd
- **Analysis Tools**: 
  - nfdump for CLI-based analysis
  - NfSen for web-based visualization
- **Anomaly Detection**: Custom Python scripts using Pandas and Scikit-learn for statistical analysis

### 2.5 Automated Response to Malicious Devices

#### Detection Mechanism
1. **MAC Address Verification**:
   - Database: PostgreSQL storing authorized MAC addresses
   - Verification Frequency: Real-time for new connections, hourly for existing connections
2. **Behavioral Analysis**:
   - Analyze NetFlow data for unusual traffic patterns
   - Machine Learning Model: Isolation Forest algorithm for anomaly detection

#### Response Implementation
1. **Interface Shutdown**:
   - SNMP SET operation to ifAdminStatus.{ifIndex} with integer value 2 (down)
   - Fallback: SSH connection with Netmiko library if SNMP fails
2. **Notification**:
   - SNMP Trap: SNMPv3 trap to management station
   - Syslog: High-priority syslog message
   - Email: SMTP alert to administrator (with optional PGP encryption)

#### Safeguards
- Whitelist of critical devices that cannot be automatically shut down
- Manual override capability for administrators
- Automatic re-enable attempt after 1 hour, requiring manual confirmation

### 2.6 Quality of Service (QoS) for Traffic Management

#### QoS Model
- **Type**: Differentiated Services (DiffServ)
- **Queuing Mechanism**: Low Latency Queuing (LLQ) with Class-Based Weighted Fair Queuing (CBWFQ)

#### Traffic Classification
1. **SCADA Control Traffic**:
   - DSCP Value: EF (Expedited Forwarding)
   - Priority Queue: Strict priority with 20% bandwidth guarantee
2. **SCADA Data Traffic**:
   - DSCP Value: AF41
   - Bandwidth: 40% of available bandwidth
3. **NetFlow Traffic**:
   - DSCP Value: AF21
   - Bandwidth: 10% of available bandwidth
4. **Syslog Traffic**:
   - DSCP Value: AF12
   - Bandwidth: 5% of available bandwidth
5. **Best Effort**:
   - All other traffic
   - Minimum 25% bandwidth guarantee

#### Implementation
- **Ingress**: NBAR2 (Network-Based Application Recognition) for deep packet inspection and classification
- **Egress**: MQC (Modular QoS CLI) for policy application

## 3. Workflow and Data Flow

### 3.1 Initial Network Discovery
1. EIGRP establishes neighbor relationships and exchanges routing information
2. SNMPv3 manager polls devices for interface and routing data
3. Network topology is constructed and stored in a graph database (e.g., Neo4j)

### 3.2 Continuous Monitoring
1. SNMPv3 traps provide real-time alerts for network changes
2. Syslog messages are continuously collected, encrypted, and stored
3. NetFlow data is sampled, encrypted, and sent to collectors for analysis

### 3.3 Anomaly Detection and Response
1. NetFlow data is analyzed in real-time for traffic anomalies
2. Unauthorized devices are detected through MAC address verification
3. Automatic response system isolates threats by disabling interfaces
4. Administrators are notified through multiple channels

### 3.4 Reporting and Visualization
1. Network topology is updated in real-time and visualized through a web interface
2. Customizable dashboards display key metrics, alerts, and historical data
3. Regular reports are generated summarizing network health, detected anomalies, and performance metrics

## 4. Security Considerations

### 4.1 Encryption Standards
- **SNMPv3**: AES-256 for privacy
- **Syslog**: TLS 1.3 with perfect forward secrecy
- **NetFlow**: IPsec with AES-GCM-256

### 4.2 Authentication Methods
- **EIGRP**: SHA-256 for neighbor authentication
- **SNMPv3**: HMAC-SHA-256 for message integrity
- **Management Access**: Multi-factor authentication (MFA) for all administrative access

### 4.3 Least Privilege Principle
- Role-Based Access Control (RBAC) for all system components
- Separate VLANs for management traffic
- Jump hosts for administrative access with detailed audit logging

### 4.4 Regular Security Audits
- Automated weekly vulnerability scans
- Quarterly penetration testing by third-party security firms
- Annual comprehensive security audit and review

## 5. Scalability and Performance Optimizations

### 5.1 Distributed Architecture
- Hierarchical design with core, distribution, and access layers
- Multiple collector nodes for load balancing of NetFlow and syslog data
- Distributed SNMP polling engines to reduce central manager load

### 5.2 Data Aggregation and Summarization
- EIGRP route summarization at distribution layer
- NetFlow data aggregation before long-term storage
- Syslog message deduplication and aggregation

### 5.3 Caching and In-Memory Processing
- Redis cache for frequently accessed topology data
- Apache Kafka for real-time event stream processing
- Elasticsearch for efficient log indexing and searching

### 5.4 Adaptive Polling and Sampling
- Dynamic adjustment of SNMP polling frequencies based on device criticality and network load
- Adaptive NetFlow sampling rates that increase during low traffic periods for more detailed analysis

## 6. Future Enhancements

### 6.1 Machine Learning Integration
- Predictive analytics for proactive fault detection
- Automated baseline creation and anomaly detection
- Natural Language Processing for intelligent log analysis

### 6.2 Blockchain for Secure Configuration Management
- Immutable audit trail of all configuration changes
- Smart contracts for automated policy enforcement

### 6.3 Intent-Based Networking (IBN) Integration
- Translation of business intentions into network policies
- Continuous verification of network state against declared intentions

### 6.4 5G and Edge Computing Support
- Integration with 5G networks for remote SCADA installations
- Edge computing nodes for local processing and reduced latency

## 7. Conclusion

The SCADA Network Topology Discovery solution represents a sophisticated approach to managing and securing critical infrastructure networks. By leveraging advanced protocols, implementing robust security measures, and optimizing for performance, the system provides real-time visibility, proactive threat detection, and automated response capabilities. The modular design and focus on industry standards ensure that the solution can evolve to meet future challenges in the ever-changing landscape of industrial control systems.
