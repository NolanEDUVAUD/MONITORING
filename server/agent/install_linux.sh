#!/bin/bash
# HyperMonitor Agent Linux Installation
# Installation rapide et simple

if [ "$EUID" -ne 0 ]; then 
  echo "Ce script doit être exécuté en tant que root (sudo)"
  exit 1
fi

INSTALL_DIR="/opt/hypermonitor"
SERVICE_FILE="/etc/systemd/system/hypermonitor-agent.service"

echo "=== Installation Agent HyperMonitor ==="

# Installer Python et dépendances
apt-get update > /dev/null 2>&1
apt-get install -y python3-pip > /dev/null 2>&1
pip3 install psutil requests > /dev/null 2>&1

# Créer le dossier et copier les fichiers
mkdir -p $INSTALL_DIR
AGENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp "$AGENT_DIR/agent.py" $INSTALL_DIR/
cp "$AGENT_DIR/requirements.txt" $INSTALL_DIR/

# Créer utilisateur hypermonitor
if ! id "hypermonitor" &>/dev/null; then
  useradd -r -s /bin/bash hypermonitor
fi

chown -R hypermonitor:hypermonitor $INSTALL_DIR

# Créer le service systemd
echo "URL du serveur? (défaut: http://localhost:8888)"
read -p "> " SERVER_URL
SERVER_URL=${SERVER_URL:-http://localhost:8888}

cat > $SERVICE_FILE << EOF
[Unit]
Description=HyperMonitor Agent
After=network.target

[Service]
Type=simple
User=hypermonitor
WorkingDirectory=$INSTALL_DIR
ExecStart=/usr/bin/python3 agent.py --url $SERVER_URL
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Activer le service
systemctl daemon-reload
systemctl enable hypermonitor-agent
systemctl start hypermonitor-agent

echo "✅ Installation terminée!"
echo "Le service démarre maintenant..."
systemctl status hypermonitor-agent
