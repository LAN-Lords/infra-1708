# Infra SCADA_Network_Topology_Discovery_Tool

## FastAPI Server

- Start the virtual env
  `venv\Scripts\activate`

- Run the fast api server
  `uvicorn main:app --reload`

# Router Commands Documentation

## 1. `username newuser privilege 15 secret your_secure_password`
Used in Cisco IOS to create a new user account with specific privileges and a password. Here's a breakdown of what each part of this command means:

### **Command Breakdown**

1. **`username newuser`**:
   - **`username`**: This keyword is used to create or modify a user account on the router.
   - **`newuser`**: This is the username for the new account. Replace `newuser` with the actual username you want to create.

2. **`privilege 15`**:
   - **`privilege`**: This keyword sets the privilege level for the user account.
   - **`15`**: This is the highest privilege level on a Cisco router. Users with privilege level 15 have full administrative rights, which means they can execute all commands, including configuration commands and view sensitive system information. Privilege levels range from 0 to 15, where 15 provides the highest level of access.

3. **`secret your_secure_password`**:
   - **`secret`**: This keyword specifies that the password should be hashed using a more secure method (MD5 hashing) rather than being stored in plain text. This is more secure than using `password`, which stores passwords in plain text.
   - **`your_secure_password`**: Replace this with the actual password you want to set for the user. Ensure it is a strong and complex password for security purposes.

### **Purpose and Usage**

- **Create or Modify User Accounts**: This command is used to create a new user or modify an existing user’s password and privilege level. If the username `newuser` does not already exist, the command will create it. If it does exist, the command will update the password and privilege level for that user.
  
- **Access Control**: By assigning a privilege level of 15, the user `newuser` is granted full administrative access to the router. This allows them to execute all commands and access all features of the router.

## 2. `snmp-server user username v3 auth md5 password priv aes 128 password` 
Used in Cisco IOS to configure an SNMPv3 user with authentication and privacy settings. Here's a detailed breakdown of each part of this command:

### **Command Breakdown**

1. **`snmp-server user snmpuser`**:
   - **`snmp-server user`**: This keyword is used to create or configure an SNMP user account on the router.
   - **`snmpuser`**: This is the username for the SNMPv3 account. Replace `snmpuser` with the actual username you want to create.

2. **`v3`**:
   - **`v3`**: Specifies that the user is being configured for SNMP version 3, which supports enhanced security features compared to earlier versions (SNMPv1 and SNMPv2c).

3. **`auth md5 your_auth_password`**:
   - **`auth`**: Indicates that the user account will use authentication.
   - **`md5`**: Specifies the authentication protocol to be used. MD5 (Message Digest Algorithm 5) is used to hash the authentication password. While MD5 is supported, for stronger security, SHA (Secure Hash Algorithm) is recommended.
   - **`your_auth_password`**: Replace this with the actual authentication password. This password is hashed and used for authenticating SNMP requests.

4. **`priv aes 128 your_priv_password`**:
   - **`priv`**: Indicates that privacy (encryption) is enabled for this user.
   - **`aes 128`**: Specifies the encryption protocol and key length. AES (Advanced Encryption Standard) with a key length of 128 bits is used for encrypting SNMP messages to ensure their confidentiality.
   - **`your_priv_password`**: Replace this with the actual privacy (encryption) password. This password is used for encrypting and decrypting SNMP messages.

### **Purpose and Usage**

- **SNMPv3 Security**: SNMPv3 provides more robust security features compared to earlier SNMP versions. By configuring SNMPv3 with both authentication and privacy, you ensure that SNMP messages are not only authenticated (to verify the sender) but also encrypted (to protect the content).

- **Authentication**: With the `auth` keyword, SNMPv3 users must provide a valid authentication password. This prevents unauthorized users from sending SNMP requests.

- **Privacy**: With the `priv` keyword, SNMPv3 users must provide a valid privacy password for encrypting SNMP messages. This protects the data from being intercepted and read by unauthorized users.

### **Verification Commands**

After configuring SNMPv3, you can verify the settings with the following commands:

1. **Verify SNMPv3 User Configuration:**
   ```bash
   show snmp user
   ```
   This command lists all SNMPv3 users and their configuration details.

2. **Verify SNMPv3 Group Configuration:**
   ```bash
   show snmp group
   ```
   This command shows SNMP groups and their associated users and permissions.

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

## Turning on the Netflow reciever server

```bash
sudo nfcapd -w -D -l /var/cache/nfdump/
```
- default port - 9995


## Enabling Netflow data-capture on router

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
