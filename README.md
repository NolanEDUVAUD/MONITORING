# HyperMonitor

Système de monitoring distribué pour Ubuntu. Surveille tous vos serveurs depuis une interface web centralisée avec démarrage automatique au boot.

## ✨ Fonctionnalités

- Dashboard web temps réel
- Monitoring multi-machines
- Agent Python léger
- Démarrage automatique au boot
- Zéro configuration requise

## 🚀 Installation Ubuntu

### 1. Préparer le serveur

```bash
# Cloner le projet
git clone <url>
cd Monitoring

# Démarrer le serveur Docker
docker-compose up -d

# Accéder au dashboard
# http://localhost:8888
```

### 2. Installer le serveur au démarrage (optionnel)

```bash
sudo cp server/hypermonitor-server.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable hypermonitor-server
sudo systemctl start hypermonitor-server
```

### 3. Installer l'agent sur les autres machines

```bash
# Sur chaque machine à monitorer:
cd server/agent
sudo bash install_linux.sh

# URL du serveur: http://IP_DU_SERVEUR:8888
```

## 📊 Utilisation

1. Accédez à `http://localhost:8888`
2. Vous verrez automatiquement tous les serveurs connectés
3. Les métriques se mettent à jour en temps réel

## 🔄 Redémarrage Automatique

### Serveur (Docker)
```bash
systemctl status hypermonitor-server
systemctl restart hypermonitor-server
```

### Agents
```bash
systemctl status hypermonitor-agent
systemctl restart hypermonitor-agent
journalctl -u hypermonitor-agent -f  # Voir les logs
```

## 📂 Structure

```
server/
  ├── main.py                      # Serveur Flask
  ├── hypermonitor-server.service  # Service systemd
  ├── docker-compose.yml           # Docker config
  ├── agent/
  │   ├── agent.py               # Agent de collecte
  │   ├── install_linux.sh        # Installation agent
  │   └── hypermonitor-agent.service
  ├── api/
  │   └── collector.py            # API Flask
  └── templates/
      └── admin.html              # Dashboard
```

## 🎯 Ajouter une machine

1. Copier `server/agent/` sur la nouvelle machine
2. Exécuter: `sudo bash install_linux.sh`
3. Entrer l'URL du serveur
4. La machine apparaît automatiquement après 10 secondes

## 🔧 Commandes Utiles

```bash
# Voir le statut du serveur
systemctl status hypermonitor-server

# Redémarrer le serveur
systemctl restart hypermonitor-server

# Voir les logs du serveur
docker-compose logs -f

# Voir le statut d'un agent
systemctl status hypermonitor-agent

# Redémarrer un agent
systemctl restart hypermonitor-agent

# Voir les logs d'un agent
journalctl -u hypermonitor-agent -f
```

## 📋 Métriques

Chaque serveur affiche:
- CPU (%)
- RAM (%)
- Disk (%)

## 📝 Notes

- Les agents se connectent toutes les 5 secondes
- Aucune configuration du serveur n'est nécessaire
- Les agents s'enregistrent automatiquement
- Démarrage automatique sur tous les systèmes

## License

MIT
