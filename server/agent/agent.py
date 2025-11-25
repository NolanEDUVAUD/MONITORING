"""
HyperMonitor Agent - Windows
Collecte et envoie les métriques système vers le serveur central
"""

import requests
import psutil
import socket
import platform
import time
import sys
import argparse
from datetime import datetime


class WindowsMonitorAgent:
    def __init__(self, api_url: str, auth_token: str = None):
        self.api_url = api_url.rstrip('/')
        self.auth_token = auth_token
        self.hostname = socket.gethostname()
        
        # Informations système statiques
        self.os_info = f"{platform.system()} {platform.release()} {platform.version()}"
        
        print("=" * 60)
        print("[*] HyperMonitor Agent - Windows")
        print("=" * 60)
        print(f"[API] Serveur API  : {self.api_url}")
        print(f"[HOST] Hostname    : {self.hostname}")
        print(f"[OS] OS          : {self.os_info}")
        
    def get_metrics(self) -> dict:
        """Collecte les métriques système"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # RAM
            mem = psutil.virtual_memory()
            ram_percent = mem.percent
            ram_used_gb = mem.used / (1024**3)
            ram_total_gb = mem.total / (1024**3)
            
            # Disque (partition C:)
            disk = psutil.disk_usage('C:\\')
            disk_percent = disk.percent
            disk_used_gb = disk.used / (1024**3)
            disk_total_gb = disk.total / (1024**3)
            
            return {
                'hostname': self.hostname,
                'os': self.os_info,
                'status': 'online',
                'cpu': {
                    'percent': round(cpu_percent, 1)
                },
                'memory': {
                    'percent': round(ram_percent, 1),
                    'used_gb': round(ram_used_gb, 2),
                    'total_gb': round(ram_total_gb, 2)
                },
                'disks': [
                    {
                        'device': 'C:',
                        'percent': round(disk_percent, 1),
                        'used_gb': round(disk_used_gb, 2),
                        'total_gb': round(disk_total_gb, 2)
                    }
                ],
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"[ERROR] Erreur collecte metriques : {e}")
            return None
    
    def send_metrics(self, metrics: dict) -> bool:
        """Envoie les métriques au serveur"""
        try:
            headers = {'Content-Type': 'application/json'}
            
            if self.auth_token:
                headers['Authorization'] = f'Bearer {self.auth_token}'
            
            response = requests.post(
                f"{self.api_url}/api/metrics",
                json=metrics,
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200:
                return True
            else:
                print(f"[WARNING] Reponse serveur : {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            print(f"[ERROR] Impossible de joindre {self.api_url}")
            return False
        except requests.exceptions.Timeout:
            print("[ERROR] Timeout serveur")
            return False
        except Exception as e:
            print(f"[ERROR] Erreur envoi : {e}")
            return False
    
    def run(self, interval: int = 3):
        """Boucle principale d'envoi des métriques"""
        print(f"[TIME] Intervalle  : {interval}s")
        
        if self.auth_token:
            print(f"[AUTH] Auth        : Activee")
        else:
            print(f"[!] Auth        : Desactivee")
        
        print("=" * 60)
        print("\n[START] Envoi des metriques en cours...\n")
        
        while True:
            try:
                # Collecter
                metrics = self.get_metrics()
                
                if metrics:
                    # Envoyer
                    success = self.send_metrics(metrics)
                    
                    # Afficher
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    if success:
                        print(f"[OK] [{timestamp}] {self.hostname} | "
                              f"CPU: {metrics['cpu']['percent']}% | "
                              f"RAM: {metrics['memory']['percent']}% | "
                              f"Disk: {metrics['disks'][0]['percent']}%")
                    else:
                        print(f"[FAIL] [{timestamp}] Echec envoi")
                
                time.sleep(interval)
                
            except KeyboardInterrupt:
                print("\n\n[STOP] Arret de l'agent...")
                sys.exit(0)
            except Exception as e:
                print(f"[ERROR] Erreur : {e}")
                time.sleep(interval)


if __name__ == "__main__":
    # Parsing des arguments
    parser = argparse.ArgumentParser(description='HyperMonitor Agent Windows')
    parser.add_argument('--url', type=str, default="http://192.168.1.109:8888",
                       help='URL du serveur HyperMonitor (défaut: http://192.168.1.109:8888)')
    parser.add_argument('--token', type=str, default=None,
                       help='Token d\'authentification (optionnel)')
    parser.add_argument('--interval', type=int, default=3,
                       help='Intervalle d\'envoi en secondes (défaut: 3)')
    
    args = parser.parse_args()
    
    # Démarrage
    agent = WindowsMonitorAgent(args.url, args.token)
    agent.run(args.interval)
