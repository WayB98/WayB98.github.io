
###Import section###
from flask import Flask, render_template, request, jsonify, send_file
import socket
import ipaddress
import threading
import subprocess
import pandas as pd
import os
import datetime

#Purpose is to Import Modules
#Flask - Web app framework
#Socket - TCP Connections (Port Scanning)
#ipaddress - Subnet iteration (like 192.168.0.0)
#Threading - fast, parallel scans
#Subprocess - pinging IPs
#Pandas - save scan to Excel
#os & datetime - file handling and timestamps
#############################################################################

###App Initialization###
app = Flask(__name__)
scan_results = []

#Sets up your flask app
#scan_results holds scan results to be used later for download/export
##############################################################################


###Discover Host Function###
def discover_hosts(network):
    alive = []
    for ip in ipaddress.IPv4Network(network, strict=False):
        result = subprocess.run(['ping', '-n', '1', '-w', '500', str(ip)],
                                stdout=subprocess.DEVNULL)
        if result.returncode == 0:
            alive.append(str(ip))
    return alive

#pings every IP in the give subnet
#adds IPs that respond to the alive list
#################################################################################

###Get Service Name Function###
def get_service_name(port):
    try:
        return socket.getservbyport(port)
    except:
        return "Unknown"
    
#maps port numbers to service names (e.g., 80 -> HTTP)
#if unknown or uncommon port, labels it unknown
##################################################################################

###Port Scanning For One Host###
def scan_ports_for_host(host, port_range):
    port_statuses = []
    threads = []

    def scan_and_log(port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.3)
                result = s.connect_ex((host, port))
                status = "OPEN" if result == 0 else "CLOSED"
                if status == "OPEN":
                    print(f"[OPEN] {host}:{port}")
                port_statuses.append((port, status))
        except:
            port_statuses.append((port, "ERROR"))

    for port in range(*port_range):
        t = threading.Thread(target=scan_and_log, args=(port,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    scan_results.append({'host': host, 'ports': port_statuses})

#scans one device across a range of ports
#uses one thread per port
#saves each port's result to scan_results
######################################################################################

###Homepage Route###
@app.route('/')
def index():
    return render_template('index.html')

#loads the front-end dashboard UI (index.html)
#allows users to input a subnet and run scans
######################################################################################

###Scan Execution Route###
@app.route('/scan', methods=['POST'])
def scan():
    global scan_results
    scan_results = []
    network = request.form['network']
    port_range = (1, 65536)
    hosts = discover_hosts(network)
    for host in hosts:
        scan_ports_for_host(host, port_range)

#accepts user input from the web form
#runs discover_hosts() to find alive devices
#scans each device on all TCP ports (1 - 65535)
#generates a timestamped excel file with results
########################################################################################


###Excel Export Block###
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    excel_filename = f"scan_results_{timestamp}.xlsx"

    # Save all port statuses with service name
    rows = []
    for result in scan_results:
        host = result['host']
        for port, status in result['ports']:
            rows.append({
                'Host': host,
                'Port': port,
                'Status': status,
                'Service': get_service_name(port)
            })

    df = pd.DataFrame(rows)
    df.to_excel(excel_filename, index=False)

    app.config['last_excel'] = excel_filename  # Save path for download
    return jsonify(scan_results)

#saves the scan to excel with columns; Host, Port, Status, Service
#stores the filename in memory (app.config) so it can be downloaded later
#########################################################################################


###Download Route###
@app.route('/download')
def download():
    filepath = app.config.get('last_excel')
    if filepath and os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return "No scan results available to download.", 404

#lets the user download the most recent scan result
###########################################################################################



###Run The App###
if __name__ == '__main__':
    app.run(debug=True)

#starts the flask server on http://127.0.0.1:5000
############################################################################################