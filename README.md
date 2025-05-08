# WayB98.github.io
TCP Port Scanner

Overview:
This project involved the development and deployment of a TCP-based port scanning utility to perform active network reconnaissance and assess surface-level exposure of hosts within a controlled enterprise environment. The tool was designed with cybersecurity operations in mind, offering insight into potential attack vectors, network hygiene, and misconfigured services.

Objective:
To build a lightweight and modular TCP scanner capable of identifying open ports, live hosts, and service banners, aiding in the detection of unauthorized services, shadow IT infrastructure, or policy-violating applications within the organization.


Tools & Technologies Used:

1. Python with socket, concurrent.futures, and ipaddress

2. pandas for reporting and result formatting

3. PowerShell wrapper for Windows automation

4. Logging support with timestamped outputs

5. CSV and Excel exports for audit documentation


Key Features:

1. Multithreaded scanning using Python's ThreadPoolExecutor for high-speed execution

2. Scans specified TCP port ranges (default: 1–1024 or custom-defined)

3. Detects TCP handshake success (SYN-ACK) to confirm open ports

4. Performs reverse DNS lookups for hostnames

5. Exportable results to .xlsx for compliance documentation and reporting


Use Cases:

1. Internal compliance auditing (e.g., CMMC, NIST 800-171)

2. Purple teaming for visibility validation

3. SOC/IR support tool for rapid host triage

4. Asset inventory validation


Lessons Learned:

1. Importance of stealth vs. speed trade-offs in scanning

2. Interpreting firewall behavior and filtering responses

3. Techniques for scan detection evasion (future enhancement)

4. Challenges in differentiating between legitimate vs. unauthorized services
