# 📱 Déploiement Agent sur Clé USB + FAQ

## 1️⃣ Fichiers à Mettre sur la Clé USB

Pour déployer l'agent, tu as besoin de **4 fichiers SEULEMENT**:

```
clé_usb/
├── agent.py                          ← Agent principal
├── requirements.txt                  ← Dépendances Python
├── install_linux.sh                  ← Installation Linux
└── install_windows.bat               ← Installation Windows
```

**C'est tout! Rien d'autre.**

### Où les trouver:
```
# Sur ton serveur
server/agent/
├── agent.py
├── requirements.txt
├── install_linux.sh
└── install_windows.bat
```

### Comment les copier sur la clé USB:
```bash
# Option 1: Depuis Windows
# Copier-coller manuellement les 4 fichiers de server/agent/ vers la clé

# Option 2: Depuis Ubuntu/Linux
mkdir /media/clé_usb/hypermonitor
cp server/agent/agent.py /media/clé_usb/hypermonitor/
cp server/agent/requirements.txt /media/clé_usb/hypermonitor/
cp server/agent/install_linux.sh /media/clé_usb/hypermonitor/
cp server/agent/install_windows.bat /media/clé_usb/hypermonitor/

# Rendre executable
chmod +x /media/clé_usb/hypermonitor/install_linux.sh
```

---

## 2️⃣ Installation Windows

### Prérequis:
- Windows 10+ (ou Windows Server 2016+)
- Python 3.8+ installé (et dans PATH)
- Droits administrateur

### Installation:

```bash
# 1. Brancher la clé USB
# 2. Ouvrir l'Explorateur
# 3. Accéder à: E:\hypermonitor (ou autre lettre de drive)
# 4. Copier tous les fichiers dans C:\HyperMonitor\

# 5. Ouvrir PowerShell en tant qu'ADMINISTRATEUR
# 6. Aller dans le dossier
cd C:\HyperMonitor

# 7. Lancer l'installation
install_windows.bat

# ✅ C'est fini! L'agent démarre automatiquement au prochain redémarrage
```

### Vérifier l'installation:

```powershell
# Vérifier l'agent dans les tâches planifiées
Get-ScheduledTask -TaskName "HyperMonitorAgent" | Select-Object State

# Ou vérifier dans Registre
reg query "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run" | findstr HyperMonitor

# Redémarrer pour tester
Restart-Computer
```

**Temps:** ~2 minutes

---

## 3️⃣ Installation Linux/Ubuntu

### Prérequis:
- Ubuntu 18.04+ (ou autre distribution Linux)
- Python 3.6+
- Accès root ou sudo

### Installation:

```bash
# 1. Brancher la clé USB
# 2. Monter la clé (si nécessaire)
# 3. Copier les fichiers
cp /media/clé_usb/hypermonitor/* ./agent/

# 4. Aller dans le dossier
cd agent

# 5. Lancer l'installation
sudo bash install_linux.sh

# 6. Quand demandé:
# URL du serveur? http://IP_DE_TON_SERVEUR:8888
# Appuyer sur Entrée

# ✅ C'est fini! L'agent démarre automatiquement
```

### Vérifier l'installation:

```bash
# Vérifier le statut du service
systemctl status hypermonitor-agent

# Doit afficher: Active (running) ✓

# Voir les logs
journalctl -u hypermonitor-agent -f
```

**Temps:** ~2 minutes

---

## ❓ Question 2: Accès Dashboard Depuis N'importe Quel PC?

### ✅ OUI, MAIS avec une condition:

#### **En Local (Même Réseau)**

Si ton serveur est sur `192.168.1.100`:
```
http://192.168.1.100:8888  ← Accessible depuis n'importe quel PC du réseau!
```

#### **Configuration Requise:**

Le serveur doit écouter sur **TOUTES les interfaces** (0.0.0.0), pas juste localhost.

**Vérification:**
```bash
# Éditer docker-compose.yml
nano docker-compose.yml

# Vérifier la section ports:
# ports:
#   - "8888:8888"  ← Correct!

# Redémarrer
docker-compose down
docker-compose up -d
```

#### **Accès Externe (En dehors du réseau)**

❌ **NON facilement** - Il faudrait:
- Configurer le routeur (port forwarding)
- Utiliser un VPN
- Exposer ton serveur à Internet (risque de sécurité!)

**Je te recommande de rester en local pour la sécurité.**

#### **Tester depuis un autre PC du réseau:**

```bash
# Sur le PC client
curl http://IP_DU_SERVEUR:8888
# Doit afficher: 200 OK

# Ou depuis navigateur:
# http://192.168.1.100:8888
```

---

## ❓ Question 3: Docker sur Ubuntu?

### ✅ OUI, Docker DOIT être installé!

Le serveur s'exécute en Docker. Tu dois l'installer.

### Installation Docker sur Ubuntu:

```bash
# 1. Mettre à jour
sudo apt update

# 2. Installer Docker
sudo apt install -y docker.io

# 3. Installer Docker Compose
sudo apt install -y docker-compose

# 4. Vérifier
docker --version
docker-compose --version

# 5. Ajouter ton utilisateur au groupe docker (optionnel, évite sudo)
sudo usermod -aG docker $USER
newgrp docker

# 6. Tester
docker run hello-world
```

**Temps:** ~5 minutes

---

## 📊 Résumé Architecture

```
Windows PC 1
   └─ Agent Python (Registry auto-start)
       └─ POST http://192.168.1.100:8888/api/metrics
            ↓
      ┌─────────────────────────┐
      │ Serveur Ubuntu (Docker) │
      │ ┌─────────────────────┐ │
      │ │ Flask Container     │ │
      │ │ Port 8888           │ │
      │ └─────────────────────┘ │
      └─────────────────────────┘
            ↓        ↓         ↓         ↓
      Dashboard accessible depuis:
      - http://192.168.1.100:8888  (même réseau) ✅
      - http://localhost:8888       (serveur lui-même) ✅

Linux PC 1
   └─ Agent Python (systemd auto-start)
       └─ POST http://192.168.1.100:8888/api/metrics

Linux PC 2
   └─ Agent Python (systemd auto-start)
       └─ POST http://192.168.1.100:8888/api/metrics

Windows PC 2
   └─ Agent Python (Registry auto-start)
       └─ POST http://192.168.1.100:8888/api/metrics
```

---

## 🎯 Checklist Installation

### Sur le Serveur (Une fois):
- [ ] Ubuntu 18.04+ installé
- [ ] `sudo apt install docker.io docker-compose`
- [ ] Cloner le projet
- [ ] `docker-compose up -d`
- [ ] Vérifier: `http://localhost:8888`

### Sur Chaque Client Windows:
- [ ] Python 3.8+ installé
- [ ] 4 fichiers copiés sur clé USB
- [ ] Clé branchée sur le PC Windows
- [ ] PowerShell ouvert en ADMINISTRATEUR
- [ ] `install_windows.bat` exécuté
- [ ] Redémarrer le PC
- [ ] Vérifier sur dashboard: PC apparaît en ~10s

### Sur Chaque Client Linux:
- [ ] 4 fichiers copiés sur clé USB
- [ ] Clé branchée sur le PC Linux
- [ ] `sudo bash install_linux.sh`
- [ ] URL du serveur: `http://IP_DU_SERVEUR:8888`
- [ ] Vérifier sur dashboard: PC apparaît en ~10s

### Accès Dashboard:
- [ ] Depuis le serveur: `http://localhost:8888`
- [ ] Depuis autre PC (même réseau): `http://192.168.1.100:8888`
- [ ] Rafraîchir la page pour voir les mises à jour

---

## 🔧 Commandes Utiles

### Sur le Serveur:
```bash
# Démarrer
docker-compose up -d

# Arrêter
docker-compose down

# Voir les logs
docker-compose logs -f

# Vérifier le port
netstat -tlnp | grep 8888
```

### Sur les Clients:
```bash
# Vérifier l'agent
systemctl status hypermonitor-agent

# Redémarrer
sudo systemctl restart hypermonitor-agent

# Voir les logs
journalctl -u hypermonitor-agent -f

# Tester la connexion
curl http://192.168.1.100:8888/api/servers/json
```

---

## 💡 Conseils Pratiques

### 1. Trouve l'IP du Serveur:
```bash
# Sur le serveur
hostname -I
# Affiche: 192.168.1.100
```

### 2. Clé USB Bootable (optionnel):
Tu peux aussi créer une clé USB avec un installateur Ubuntu + les fichiers.

### 3. Sécurité:
- Les agents et serveur communiquent en HTTP (pas HTTPS en local)
- En local sur LAN, c'est OK
- Ne pas exposer à Internet sans sécuriser!

### 4. Nombreux Clients:
Pas de limite! Tu peux avoir 100+ agents qui envoient des métriques.

---

## 📝 Résumé Rapide

| Question | Réponse |
|----------|---------|
| Fichiers sur clé USB? | `agent.py`, `requirements.txt`, `install_linux.sh` (3 fichiers) |
| Accessible depuis autre PC? | OUI (même réseau), via `http://IP:8888` |
| Docker obligatoire? | OUI, sur le serveur uniquement |
| Temps par PC client? | 2-3 minutes |
| Nombre de clients? | Illimité |

---

**C'est prêt! Tu peux start!** 🚀
