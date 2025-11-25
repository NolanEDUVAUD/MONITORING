"""
Dashboard Web pour HyperMonitor
Interface web pour visualiser les métriques des serveurs
"""

from flask import render_template, jsonify
from api.collector import app, api_instance
import json
from datetime import datetime

@app.route('/')
def index():
    """Page principale du dashboard"""
    return render_template('dashboard.html')

@app.route('/api/servers/json')
def get_servers_json():
    """Retourne les serveurs au format JSON pour le dashboard"""
    if not api_instance:
        return jsonify({'servers': []}), 500
    
    servers = api_instance.get_servers()
    servers_list = []
    
    for hostname, data in servers.items():
        servers_list.append({
            'hostname': hostname,
            'os': data.get('os', 'Unknown'),
            'status': data.get('status', 'unknown'),
            'cpu': data.get('cpu', {}).get('percent', 0),
            'ram': data.get('memory', {}).get('percent', 0),
            'ram_used': data.get('memory', {}).get('used_gb', 0),
            'ram_total': data.get('memory', {}).get('total_gb', 0),
            'disks': data.get('disks', []),
            'last_update': data.get('last_update', 0),
            'timestamp': datetime.fromtimestamp(data.get('last_update', 0)).strftime('%H:%M:%S') if data.get('last_update') else 'N/A'
        })
    
    return jsonify({'servers': servers_list}), 200
