import socket
import subprocess
import ipaddress
from concurrent.futures import ThreadPoolExecutor

def ping(host):
    """Check if host is reachable"""
    try:
        subprocess.check_output(['ping', '-c', '1', '-W', '1', str(host)], 
                              stderr=subprocess.PIPE)
        return True
    except:
        return False

def scan_port(host, port):
    """Scan a single port on a host"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((str(host), port))
            return port, True
    except:
        return port, False

def network_scan(network, ports=[21, 22, 80, 443, 3389]):
    """Scan a network range"""
    active_hosts = []
    
    # Convert network string to IP network
    net = ipaddress.ip_network(network, strict=False)
    
    print(f"🔍 Scanning {network} network...")
    
    # Ping sweep with threading
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(ping, net.hosts())
        
        for host, is_alive in zip(net.hosts(), results):
            if is_alive:
                print(f"🟢 Host alive: {host}")
                active_hosts.append(host)
    
    # Port scan active hosts
    for host in active_hosts:
        print(f"\n🔎 Scanning ports on {host}")
        with ThreadPoolExecutor(max_workers=20) as executor:
            port_results = executor.map(lambda p: scan_port(host, p), ports)
            
            for port, is_open in port_results:
                status = "🟢 OPEN" if is_open else "🔴 CLOSED"
                print(f"Port {port}: {status}")

if __name__ == "__main__":
    # Example: Scan 192.168.1.0/24 network
    network_scan("192.168.1.0/24")