from flask import Flask, request, jsonify
import subprocess
import re

app = Flask(__name__)

def get_mac(ip):
    """Get MAC address using arp"""
    try:
        output = subprocess.check_output(['arp', '-n', ip]).decode()
        match = re.search(r'(([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]{2}))', output)
        return match.group(0) if match else None
    except:
        return None

@app.route('/')
def index():
    return app.send_static_file('network_scanner.html')

@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    network = data['network']
    ports = data['ports']
    
    # This would call your actual scanning functions
    # Here's a mock response for demonstration
    return jsonify({
        'active_hosts': [
            {
                'ip': '192.168.1.1',
                'mac': get_mac('192.168.1.1'),
                'ports': [
                    {'number': 22, 'open': True},
                    {'number': 80, 'open': True},
                    {'number': 443, 'open': False}
                ]
            },
            {
                'ip': '192.168.1.100',
                'mac': get_mac('192.168.1.100'),
                'ports': [
                    {'number': 80, 'open': True},
                    {'number': 443, 'open': True}
                ]
            }
        ]
    })

if __name__ == '__main__':
    app.run(debug=True)