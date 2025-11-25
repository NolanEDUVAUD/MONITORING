FROM python:3.11-alpine

WORKDIR /app

# Installation des dépendances système
RUN apk add --no-cache \
    gcc \
    musl-dev \
    linux-headers \
    bash

# Copie des fichiers de configuration des dépendances
COPY server/requirements.txt /app/

# Installation des dépendances Python
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copie de l'application
COPY server/ /app/
COPY config/ /app/config/

# Crée le répertoire data pour les logs
RUN mkdir -p /app/data

# Port API pour recevoir les données des agents
EXPOSE 8888

# Commande de démarrage
CMD ["python", "main.py"]
