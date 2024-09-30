# SCADA Network Topology Discovery Solution

## 1. Introduction

The SCADA Network Topology Discovery solution provides a **secure, automated method** for mapping and monitoring a critical infrastructure network, designed to meet the needs of large-scale industrial systems. This document explains the technicalities, trade-offs, and operational workflow of the solution.

The solution leverages **EIGRP routing protocol**, **SNMPv3 traps**, and **syslog** for secure, real-time network topology discovery and event monitoring. It eliminates traditional discovery methods like CDP/LLDP for enhanced security, and it integrates multiple protocols for secure data transmission.

Additionally, a **malicious device detection and response mechanism** has been implemented. When an unauthorized device is detected, the interface connecting the device is automatically disabled using **`snmpset`**, and the SCADA network administrator is informed immediately.

To address **bandwidth concerns**, the architecture implements **syslog throttling**, **NetFlow sampling**, and **QoS (Quality of Service)**, ensuring efficient use of network resources without compromising critical SCADA operations.

---

## 2. Key Components

### 2.1 EIGRP-Based Topology Mapping
- **Purpose**: EIGRP (Enhanced Interior Gateway Routing Protocol) is used as the backbone for discovering routing information across the SCADA network.
- **Reason for Choice**: CDP/LLDP are vulnerable and inefficient for critical infrastructure. EIGRP provides fast convergence, reliable transport, and security.
- **Implementation**: We collect the routing tables using SNMP polling to derive network topology dynamically.
- **Trade-off**: EIGRP, while secure and efficient, requires more configuration overhead than plug-and-play options like LLDP, but this trade-off is acceptable given the enhanced security.

### 2.2 SNMPv3 for Device Management and Monitoring
- **Purpose**: SNMPv3 is used for secure polling and trap notifications.
- **Configuration**: `noauthnopriv` mode is used for polling, while traps are configured with **privacy and authentication** to ensure data confidentiality.
- **Functionality**: We periodically poll network devices for interface status and routing table data, while SNMP traps provide asynchronous notifications of critical events (e.g., interface down, route changes).
- **Security**: Using SNMPv3 ensures authentication and encryption of SNMP messages, which is critical for protecting sensitive SCADA system data.

### 2.3 Syslog for Event Logging
- **Purpose**: Syslog is configured to capture all network device logs in real-time, with messages encrypted using **TLS**.
- **Centralized Logging**: A **rsyslog server** aggregates and stores logs from the entire network, allowing operators to monitor system events.

### **Syslog Throttling**
- **Problem**: During periods of high event generation, such as a network fault, syslog messages can overwhelm the network, leading to performance degradation.
- **Solution**: We implement **syslog throttling**, limiting the number of syslog messages sent per second. This ensures that during peak events, syslog does not flood the network.
- **Trade-off**: Throttling reduces the granularity of logs during high-traffic events but ensures that SCADA control traffic is not impacted.

### 2.4 NetFlow for Traffic Monitoring
- **Purpose**: NetFlow is used to monitor real-time traffic patterns in the SCADA network.
- **Security**: NetFlow traffic between routers and collectors is encrypted using **IPsec**.
- **Functionality**: NetFlow data is captured using **nfcapd** and processed with **nfdump** to analyze bandwidth usage, detect anomalies, and perform capacity planning.

### **NetFlow Sampling**
- **Problem**: Continuous export of full NetFlow data consumes significant bandwidth.
- **Solution**: We reduce the bandwidth requirement by implementing **NetFlow sampling**, where only a subset of traffic flows is exported. This provides sufficient visibility for anomaly detection and traffic monitoring while conserving network bandwidth.
- **Trade-off**: Sampling reduces the amount of data collected, but this is balanced against the need to preserve bandwidth.

### 2.5 Automated Response to Malicious Devices
- **Purpose**: If an unauthorized device is detected, the system automatically disables the interface that connects the device to the network.
- **Implementation**: 
    - The system performs **MAC Address Verification** by checking the device's MAC address against a central database.
    - If the device is unauthorized, **`snmpset`** is used to disable the corresponding interface on the switch or router.
    - The SCADA network administrator is notified of the action via syslog or SNMP trap, ensuring visibility and quick response.
- **Trade-off**: Automating the response can lead to unintended disconnections in rare cases of false positives, but the trade-off ensures immediate mitigation of potential threats.

### 2.6 Quality of Service (QoS) for Traffic Management
- **Problem**: SCADA traffic is time-sensitive, and syslog or NetFlow data can potentially interfere with critical control messages.
- **Solution**: We implement **QoS** to prioritize SCADA control traffic over syslog and NetFlow data.
  - **SCADA Traffic Priority**: SCADA control and data messages are assigned **high priority** to ensure uninterrupted operation.
  - **Syslog and NetFlow Priority**: These monitoring and logging services are marked with **lower priority**, ensuring that they do not interfere with critical operations during network congestion.
- **Trade-off**: Lowering the priority of syslog and NetFlow traffic may delay non-critical monitoring data, but this is necessary to guarantee the performance of SCADA operations.

---

## 3. Workflow Overview

### Step 1: Topology Discovery
1. **EIGRP** exchanges routing information between network devices.
2. **SNMP Polling** extracts routing table and interface data from each device.
3. Data is used to dynamically map the network, ensuring real-time updates.

### Step 2: Event Monitoring
1. Devices send real-time event notifications via **SNMPv3 traps** to alert about changes (e.g., link failure, unauthorized device detected).
2. **Syslog** collects and stores device logs, which are monitored for unusual activity or critical events.
3. **Syslog Throttling** ensures that only a limited number of syslog messages are sent per second, preventing syslog traffic from overwhelming the network.
4. **NetFlow Sampling** reduces the amount of traffic generated by exporting only a subset of the total flows, conserving bandwidth without losing visibility.

### Step 3: Security & Anomaly Detection
1. **MAC Address Verification**: The system checks if devices connecting to the network have authorized MAC addresses stored in the central database.
2. **Unauthorized Device Detection & Response**: 
    - If a device is not in the database, it is flagged as unauthorized. 
    - The interface to which the device is connected is **automatically disabled** using `snmpset`, and the network administrator is immediately informed.
3. **NetFlow Monitoring**: Monitors real-time traffic for any abnormal patterns that may indicate security threats.

---

## 4. Security Considerations

### 4.1 SNMPv3 Security
- **SNMPv3** is used with `authPriv` for traps, ensuring both message integrity and encryption.
- Trade-off: Increased security with SNMPv3 comes at the cost of higher overhead compared to older versions like SNMPv1.

### 4.2 Syslog Security with TLS
- **TLS-encrypted syslog** ensures that event logs are protected against tampering or eavesdropping.
- Trade-off: TLS adds computational overhead but is necessary for securing log data.

### 4.3 NetFlow Security with IPsec
- **IPsec** ensures NetFlow traffic is encrypted end-to-end between routers and the flow collector.
- Trade-off: IPsec requires proper key management and can introduce slight delays, but these are acceptable given the security gains.

### 4.4 Interface Disable Mechanism with `snmpset`
- **Automatic Interface Shutdown**: When an unauthorized device is detected, the **`snmpset`** command is used to turn off the interface.
- **Network Admin Alert**: Syslog or SNMP trap notifications are sent to the administrator, ensuring awareness.
- **Trade-off**: While this provides rapid mitigation of potential threats, care must be taken to avoid false positives leading to unnecessary interface shutdowns.

---

## 5. Design Trade-offs

### 5.1 Performance vs. Security
- While SNMPv3, TLS, and IPsec introduce some performance overhead, they are necessary to ensure that sensitive data in the SCADA network is protected.
- **Justification**: Given the critical nature of SCADA systems, security takes precedence over minimal performance loss.

### 5.2 EIGRP vs. LLDP/CDP
- **EIGRP** was chosen due to its efficiency in secure routing without exposing topology data as LLDP/CDP do, which can be exploited by attackers.
- **Trade-off**: While CDP/LLDP provide easier plug-and-play functionality, they are less secure and vulnerable in critical infrastructures like SCADA.

### 5.3 Syslog Throttling
- **Trade-off**: Throttling syslog traffic reduces the amount of event data transmitted during high-volume periods, but this ensures that syslog messages do not overwhelm the network during critical moments.

### 5.4 NetFlow Sampling
- **Trade-off**: Sampling NetFlow data reduces the amount of detailed traffic data collected but preserves bandwidth for more critical operations.

### 5.5 QoS for SCADA Traffic
- **Trade-off**: By assigning lower priority to syslog and NetFlow traffic, there may be delays in receiving log and flow data, but this ensures that SCADA control traffic is never interrupted.

---

## 6. Conclusion

This SCADA Network Topology Discovery solution combines **security**, **real-time monitoring**, and **bandwidth optimization** to provide a robust framework for critical infrastructure networks. The inclusion of **syslog throttling**, **NetFlow sampling**, and **QoS prioritization** ensures that the network can handle high-volume events without sacrificing performance in SCADA operations. Security measures like **SNMPv3**, **TLS**, and **IPsec** further ensure the integrity and confidentiality of data transmissions in the system.
