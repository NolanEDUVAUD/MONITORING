#!/usr/bin/env python3
"""
HyperMonitor - Serveur Central
Monitoring multi-plateformes style Cyberpunk/Gruvbox
"""

import yaml
from pathlib import Path
from api.collector import MonitorAPI, init_api

class HyperMonitor:
    def __init__(self):
        self.config = self.load_config()
        self.api = init_api(
            port=self.config.get('api', {}).get('port', 8888),
            auth_token=self.config.get('api', {}).get('token')
        )
        
    def load_config(self):
        config_path = Path("/app/config/servers.yaml")
        if not config_path.exists():
            config_path = Path("config/servers.yaml")
        
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def start(self):
        # Démarrage de l'API
        print("[*] HyperMonitor API demarree sur le port 8888")
        print("[WAIT] En attente des agents...")
        print("\nL'API est maintenant active!")
        print("Lancez un agent avec: python agent.py --url http://localhost:8888\n")
        
        # Lancer l'API (bloquant)
        self.api.start()

if __name__ == "__main__":
    monitor = HyperMonitor()
    monitor.start()
