# 🚀 Démarrage Rapide - HyperMonitor

## 1️⃣ Démarrer le Serveur (5 minutes)

```bash
# Sur le PC Ubuntu qui hébergera le serveur

# Cloner le projet
git clone <url>
cd Monitoring

# Démarrer Docker
docker-compose up -d

# Vérifier que c'est actif
docker-compose ps

# Accéder au dashboard
# Ouvrir le navigateur: http://localhost:8888
```

## 2️⃣ Installer un Agent (2 minutes par machine)

```bash
# Sur chaque machine Ubuntu à monitorer

# Copier le dossier agent du serveur
scp -r user@server-ip:~/Monitoring/server/agent ./

# Aller dans le dossier agent
cd agent

# Lancer l'installation
sudo bash install_linux.sh

# Quand demandé:
# - URL du serveur: http://IP_DU_SERVEUR:8888
# - Appuyer sur Entrée

# C'est fini! L'agent démarre automatiquement
```

## ✅ Vérifier que c'est OK

```bash
# L'agent apparaît dans le dashboard
# http://localhost:8888

# Les métriques se mettent à jour en temps réel
# CPU, RAM, Disk

# Vérifier le statut de l'agent:
systemctl status hypermonitor-agent

# Voir les logs:
journalctl -u hypermonitor-agent -f
```

## 🎯 Ajouter plus de machines

Répétez l'étape 2 sur chaque nouvelle machine. C'est tout!

## 🔄 Démarrage Automatique du Serveur

Pour que le serveur démarre automatiquement au boot d'Ubuntu:

```bash
# Copier le service
sudo cp server/hypermonitor-server.service /etc/systemd/system/

# Activer
sudo systemctl daemon-reload
sudo systemctl enable hypermonitor-server
sudo systemctl start hypermonitor-server

# Vérifier
systemctl status hypermonitor-server
```

## 📊 C'est prêt!

1. Allez sur `http://localhost:8888`
2. Installez l'agent sur vos autres PCs
3. Regardez vos serveurs apparaître en temps réel
4. C'est fini! 🎉

## ⚠️ Problèmes?

### L'agent ne démarre pas
```bash
sudo systemctl status hypermonitor-agent
journalctl -u hypermonitor-agent -n 20
```

### Le dashboard ne s'affiche pas
```bash
docker-compose logs -f
docker-compose restart
```

### Changer l'URL du serveur
```bash
# Éditer le service
sudo nano /etc/systemd/system/hypermonitor-agent.service

# Redémarrer
sudo systemctl restart hypermonitor-agent
```

## 🎓 Commandes Utiles

```bash
# Serveur
docker-compose up -d              # Démarrer
docker-compose down               # Arrêter
docker-compose logs -f            # Voir les logs
docker-compose restart            # Redémarrer

# Agent
sudo systemctl start hypermonitor-agent       # Démarrer
sudo systemctl stop hypermonitor-agent        # Arrêter
sudo systemctl restart hypermonitor-agent     # Redémarrer
sudo systemctl status hypermonitor-agent      # Statut
sudo journalctl -u hypermonitor-agent -f      # Logs temps réel
```
