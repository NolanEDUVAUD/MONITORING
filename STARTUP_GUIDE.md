# 📖 Guide d'Installation - HyperMonitor

## Architecture

```
┌─────────────────────────────────────┐
│     Serveur Central (Ubuntu)        │
│  Docker Container (Flask + API)     │
│  http://localhost:8888              │
└─────────────────────────────────────┘
           ▲         ▲         ▲
           │         │         │
      POST /api/metrics (5s)
           │         │         │
┌──────────┴────┐ ┌──────────┴────┐
│  Agent PC #1  │ │  Agent PC #2  │
│  (systemd)    │ │  (systemd)    │
│  Ubuntu       │ │  Ubuntu       │
└───────────────┘ └───────────────┘
```

## Installation Serveur Ubuntu

### Prérequis
- Ubuntu 18.04 ou plus récent
- Docker et Docker Compose installés
- Accès root ou sudo

### Étape 1: Préparer le serveur

```bash
# Cloner le projet
git clone <url>
cd Monitoring

# Vérifier que Docker fonctionne
docker --version
docker-compose --version

# Démarrer le serveur
docker-compose up -d

# Vérifier le statut
docker-compose ps

# Voir les logs (Ctrl+C pour quitter)
docker-compose logs -f
```

### Étape 2: Configurer le démarrage automatique (optionnel)

```bash
# Copier le service systemd
sudo cp server/hypermonitor-server.service /etc/systemd/system/

# Modifier les chemins (si nécessaire)
sudo nano /etc/systemd/system/hypermonitor-server.service
# Vérifier: WorkingDirectory=/path/to/Monitoring

# Activer le service
sudo systemctl daemon-reload
sudo systemctl enable hypermonitor-server
sudo systemctl start hypermonitor-server

# Vérifier
systemctl status hypermonitor-server

# Voir les logs
docker-compose logs -f
```

### Étape 3: Vérifier le serveur

```bash
# Accéder au dashboard
# http://IP_DU_SERVEUR:8888

# Ou localement
# http://localhost:8888

# Vérifier l'API
curl http://localhost:8888/api/servers/json
```

---

## Installation Agent Ubuntu

### Prérequis
- Ubuntu 18.04 ou plus récent
- Python 3.6+
- Accès root ou sudo
- URL du serveur HyperMonitor

### Étape 1: Copier l'agent

```bash
# Depuis le serveur ou depuis Git
# Option 1: Copier via SSH
scp -r user@server:/Monitoring/server/agent ./

# Option 2: Cloner et naviguer
git clone <url>
cd Monitoring/server/agent

# Vérifier les fichiers
ls -la
# Doit afficher: agent.py, requirements.txt, install_linux.sh, hypermonitor-agent.service
```

### Étape 2: Lancer l'installation

```bash
# Donner les permissions
chmod +x install_linux.sh

# Lancer l'installation (IMPORTANT: en root)
sudo bash install_linux.sh

# Vous serez demandé:
# "URL du serveur? (défaut: http://localhost:8888)"
# Entrez: http://IP_DU_SERVEUR:8888

# Appuyez sur Entrée
```

### Étape 3: Vérifier l'installation

```bash
# Vérifier le statut du service
systemctl status hypermonitor-agent

# Doit afficher: Active (running) ✓

# Voir les logs en temps réel
journalctl -u hypermonitor-agent -f

# Doit afficher: [OK] Metrics sent to server

# Vérifier dans le dashboard
# http://IP_DU_SERVEUR:8888
# Votre machine doit apparaître!
```

---

## Ajouter d'autres machines

Répétez les étapes de l'Installation Agent sur chaque machine Ubuntu.

Chaque agent:
1. S'enregistre automatiquement
2. Envoie des métriques toutes les 5 secondes
3. Apparaît dans le dashboard en moins de 10 secondes

---

## Gestion des Services

### Serveur

```bash
# Démarrer
docker-compose up -d

# Arrêter
docker-compose down

# Redémarrer
docker-compose restart

# Voir les logs
docker-compose logs -f

# Voir les logs des 20 dernières lignes
docker-compose logs --tail 20
```

### Agent

```bash
# Démarrer
sudo systemctl start hypermonitor-agent

# Arrêter
sudo systemctl stop hypermonitor-agent

# Redémarrer
sudo systemctl restart hypermonitor-agent

# Vérifier le statut
systemctl status hypermonitor-agent

# Voir les logs
journalctl -u hypermonitor-agent -f

# Voir les 20 derniers logs
journalctl -u hypermonitor-agent -n 20

# Désactiver au démarrage
sudo systemctl disable hypermonitor-agent

# Réactiver au démarrage
sudo systemctl enable hypermonitor-agent
```

---

## Désinstallation

### Désinstaller un agent

```bash
# Arrêter l'agent
sudo systemctl stop hypermonitor-agent

# Désactiver au démarrage
sudo systemctl disable hypermonitor-agent

# Supprimer le service
sudo rm /etc/systemd/system/hypermonitor-agent.service

# Recharger systemd
sudo systemctl daemon-reload

# Nettoyer
rm -rf /opt/hypermonitor
```

### Désinstaller le serveur

```bash
# Arrêter Docker
docker-compose down

# Supprimer les volumes (données)
docker-compose down -v

# Supprimer le service (si configuré)
sudo systemctl stop hypermonitor-server
sudo systemctl disable hypermonitor-server
sudo rm /etc/systemd/system/hypermonitor-server.service
sudo systemctl daemon-reload
```

---

## Troubleshooting

### L'agent ne démarre pas

```bash
# Vérifier le service
systemctl status hypermonitor-agent

# Voir les erreurs
journalctl -u hypermonitor-agent -n 50

# Vérifier les permissions
ls -la /opt/hypermonitor

# Vérifier que Python est installé
python3 --version

# Vérifier les dépendances
pip3 list | grep -E "psutil|requests"
```

### L'agent ne se connecte pas au serveur

```bash
# Vérifier l'URL du serveur
sudo nano /etc/systemd/system/hypermonitor-agent.service
# Vérifier la ligne: ExecStart

# Vérifier la connectivité réseau
ping IP_DU_SERVEUR

# Vérifier le port
nc -zv IP_DU_SERVEUR 8888

# Redémarrer l'agent
sudo systemctl restart hypermonitor-agent

# Voir les logs
journalctl -u hypermonitor-agent -f
```

### Le serveur ne démarre pas

```bash
# Vérifier Docker
docker ps

# Voir les erreurs
docker-compose logs -f

# Vérifier les ports
netstat -tlnp | grep 8888

# Redémarrer Docker
sudo systemctl restart docker
docker-compose up -d
```

### La machine n'apparaît pas dans le dashboard

1. Attendre 10 secondes (premier enregistrement)
2. Rafraîchir la page web (F5)
3. Vérifier que l'agent envoie des données:
   ```bash
   journalctl -u hypermonitor-agent -f
   ```
4. Vérifier que le serveur les reçoit:
   ```bash
   docker-compose logs -f
   ```

---

## Configuration Avancée

### Changer l'URL du serveur après installation

```bash
# Éditer le service
sudo nano /etc/systemd/system/hypermonitor-agent.service

# Modifier la ligne ExecStart:
# ExecStart=/usr/bin/python3 /opt/hypermonitor/agent.py --url http://NOUVEAU_IP:8888

# Recharger et redémarrer
sudo systemctl daemon-reload
sudo systemctl restart hypermonitor-agent
```

### Utiliser un port différent pour le serveur

```bash
# Éditer docker-compose.yml
nano server/docker-compose.yml

# Modifier la section ports:
# ports:
#   - "9999:8888"  ← Utiliser le port 9999 au lieu de 8888

# Redémarrer
docker-compose down
docker-compose up -d
```

---

## Métriques Collectées

Chaque agent envoie:
- **CPU**: Pourcentage d'utilisation moyenne
- **RAM**: Pourcentage d'utilisation
- **Disk**: Pourcentage d'utilisation de la partition racine
- **Intervalle**: Toutes les 5 secondes par défaut

---

## Support

Pour toute question:
1. Vérifier les logs: `journalctl -u hypermonitor-agent -f`
2. Vérifier la connectivité: `nc -zv SERVER_IP 8888`
3. Redémarrer les services: `systemctl restart hypermonitor-agent`
