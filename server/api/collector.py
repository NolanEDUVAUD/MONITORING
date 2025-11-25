"""
API Flask pour collecter les métriques des agents
"""

from flask import Flask, request, jsonify, render_template
from datetime import datetime
import threading
import time
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'))

class MonitorAPI:
    def __init__(self, config: dict = None):
        """Initialise l'API avec la configuration"""
        if config is None:
            config = {}
        
        # Configuration depuis le fichier de config ou paramètres par défaut
        api_config = config.get('api', {})
        self.port = api_config.get('port', 8888)
        self.auth_token = api_config.get('token')
        self.servers = {}
        self.lock = threading.Lock()
        
    def start(self):
        """Démarre l'API Flask"""
        print(f"[*] HyperMonitor API demarree sur le port {self.port}")
        if self.auth_token:
            print(f"[AUTH] Authentification activee")
        else:
            print(f"[!] Mode sans authentification (developpement)")
        print(f"\n[WAIT] En attente des agents...\n")
        
        app.run(host='0.0.0.0', port=self.port, debug=False, use_reloader=False)
    
    def check_auth(self, request) -> bool:
        """Vérifie l'authentification si activée"""
        if not self.auth_token:
            return True  # Pas d'auth requise
        
        token = request.headers.get('Authorization')
        if token and token.replace('Bearer ', '') == self.auth_token:
            return True
        return False
    
    def add_or_update_server(self, data: dict):
        """Ajoute ou met à jour un serveur"""
        with self.lock:
            hostname = data.get('hostname', 'unknown')
            data['last_update'] = time.time()
            self.servers[hostname] = data
            
            # Log simplifié
            cpu = data.get('cpu', {}).get('percent', 0)
            ram = data.get('memory', {}).get('percent', 0)
            print(f"[DATA] {hostname} | CPU: {cpu}% | RAM: {ram}%")
    
    def get_servers(self) -> dict:
        """Retourne tous les serveurs avec nettoyage des serveurs inactifs"""
        with self.lock:
            current_time = time.time()
            timeout = 10  # Serveur considéré offline après 10s
            
            # Nettoyer les serveurs inactifs
            inactive = []
            for hostname, data in self.servers.items():
                last_seen = data.get('last_update', 0)
                if current_time - last_seen > timeout:
                    data['status'] = 'offline'
                    # Optionnel : supprimer après 60s
                    if current_time - last_seen > 60:
                        inactive.append(hostname)
            
            # Supprimer les serveurs totalement inactifs
            for hostname in inactive:
                del self.servers[hostname]
            
            return dict(self.servers)


# Instance globale de l'API
api_instance = None

def init_api(port: int = 8888, auth_token: str = None):
    """Initialise l'API"""
    global api_instance
    api_instance = MonitorAPI({'api': {'port': port, 'token': auth_token}})
    return api_instance


# ===== ROUTES FLASK =====

@app.route('/api/metrics', methods=['POST'])
def receive_metrics():
    """Endpoint pour recevoir les métriques"""
    if not api_instance:
        return jsonify({'error': 'API not initialized'}), 500
    
    # Vérifier l'authentification
    if not api_instance.check_auth(request):
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Récupérer les données
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Ajouter/mettre à jour le serveur
    api_instance.add_or_update_server(data)
    
    return jsonify({'status': 'ok'}), 200


@app.route('/api/servers', methods=['GET'])
def get_servers():
    """Endpoint pour récupérer la liste des serveurs"""
    if not api_instance:
        return jsonify({'error': 'API not initialized'}), 500
    
    servers = api_instance.get_servers()
    return jsonify(servers), 200


@app.route('/health', methods=['GET'])
def health():
    """Endpoint de santé"""
    return jsonify({
        'status': 'ok',
        'servers_count': len(api_instance.servers) if api_instance else 0
    }), 200


# ===== ROUTES WEB DASHBOARD =====

@app.route('/')
def index():
    """Page principale du dashboard"""
    return render_template('dashboard.html')

@app.route('/admin')
def admin():
    """Page d'administration"""
    return render_template('admin.html')

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
