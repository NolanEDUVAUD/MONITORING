#!/usr/bin/env python3
"""
Test des composants HyperMonitor
Vérifie que tout est correctement installé et configuré
"""

import sys
import subprocess
from pathlib import Path

def test_imports():
    """Teste les imports principaux"""
    print("\n" + "="*60)
    print("🔍 Test des imports...")
    print("="*60)
    
    tests = {
        "Flask": "flask",
        "Textual": "textual",
        "Rich": "rich",
        "psutil": "psutil",
        "requests": "requests",
        "PyYAML": "yaml"
    }
    
    all_ok = True
    for name, module in tests.items():
        try:
            __import__(module)
            print(f"[OK] {name}")
        except ImportError:
            print(f"[FAIL] {name} - manquant")
            all_ok = False
    
    return all_ok

def test_config():
    """Teste la configuration"""
    print("\n" + "="*60)
    print("🔍 Test de la configuration...")
    print("="*60)
    
    config_path = Path("config/servers.yaml")
    if config_path.exists():
        print(f"[OK] Fichier config trouve: {config_path}")
        try:
            import yaml
            with open(config_path) as f:
                config = yaml.safe_load(f)
            print(f"[OK] Config valide")
            print(f"   - {len(config.get('servers', []))} serveur(s) configure(s)")
            print(f"   - Port API: {config.get('api', {}).get('port', 8888)}")
            return True
        except Exception as e:
            print(f"[FAIL] Config invalide: {e}")
            return False
    else:
        print(f"[FAIL] Fichier config manquant: {config_path}")
        return False

def test_agent():
    """Teste l'agent"""
    print("\n" + "="*60)
    print("🔍 Test de l'agent...")
    print("="*60)
    
    agent_path = Path("server/agent/agent.py")
    if agent_path.exists():
        print(f"[OK] Agent trouve: {agent_path}")
        try:
            result = subprocess.run(
                [sys.executable, str(agent_path), "--help"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                print(f"[OK] Agent fonctionnel (aide affichee)")
                return True
        except Exception as e:
            print(f"[!] Impossible de tester l'agent: {e}")
            return False
    else:
        print(f"[FAIL] Agent manquant: {agent_path}")
        return False

def test_api():
    """Teste l'API"""
    print("\n" + "="*60)
    print("🔍 Test de l'API...")
    print("="*60)
    
    api_path = Path("server/api/collector.py")
    if api_path.exists():
        print(f"[OK] API trouvee: {api_path}")
        try:
            import server.api.collector
            print(f"[OK] API importable")
            return True
        except Exception as e:
            print(f"[FAIL] Erreur API: {e}")
            return False
    else:
        print(f"[FAIL] API manquante: {api_path}")
        return False

def main():
    print("\n" + "="*60)
    print("🧪 Test HyperMonitor")
    print("="*60)
    
    results = {
        "Imports": test_imports(),
        "Config": test_config(),
        "Agent": test_agent(),
        "API": test_api(),
    }
    
    print("\n" + "="*60)
    print("Resume des tests")
    print("="*60)
    
    for test, result in results.items():
        status = "[OK]" if result else "[FAIL]"
        print(f"{status} {test}")
    
    all_ok = all(results.values())
    
    print("\n" + "="*60)
    if all_ok:
        print("[OK] Tous les tests sont passes!")
        print("\nPour demarrer:")
        print("  Serveur:  docker-compose up")
        print("  Agent:    python server/agent/agent.py --url http://<IP>:8888")
    else:
        print("[FAIL] Certains tests ont echoue")
        print("\nVerifiez les fichiers manquants et les imports")
    print("="*60 + "\n")
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
