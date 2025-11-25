#!/usr/bin/env python3
"""
Script de démarrage de l'agent HyperMonitor
Utilisation: python run_agent.py [--url URL] [--token TOKEN] [--interval INTERVAL]
"""

import sys
import os

# Ajouter le répertoire parent au path pour importer agent
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import WindowsMonitorAgent
import argparse

def main():
    parser = argparse.ArgumentParser(description='HyperMonitor Agent - Service de monitoring')
    parser.add_argument('--url', type=str, default="http://192.168.1.109:8888",
                       help='URL du serveur HyperMonitor (défaut: http://192.168.1.109:8888)')
    parser.add_argument('--token', type=str, default=None,
                       help='Token d\'authentification (optionnel)')
    parser.add_argument('--interval', type=int, default=3,
                       help='Intervalle d\'envoi en secondes (défaut: 3)')
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("[*] Demarrage HyperMonitor Agent")
    print("="*60)
    print(f"[SERVER] Serveur: {args.url}")
    print(f"[TIME] Intervalle: {args.interval}s")
    if args.token:
        print(f"🔒 Authentification: Activée")
    print("="*60 + "\n")
    
    # Démarrage
    agent = WindowsMonitorAgent(args.url, args.token)
    agent.run(args.interval)

if __name__ == "__main__":
    main()
