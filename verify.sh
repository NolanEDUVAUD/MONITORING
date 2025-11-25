#!/bin/bash
# Vérification de l'installation HyperMonitor

echo "=== Vérification HyperMonitor Ubuntu ==="
echo ""

# Vérifier Docker
echo "🐳 Docker:"
if command -v docker &> /dev/null; then
  echo "  ✅ Docker installé"
  docker --version
else
  echo "  ❌ Docker non installé"
fi

echo ""
echo "🐳 Docker Compose:"
if command -v docker-compose &> /dev/null; then
  echo "  ✅ Docker Compose installé"
  docker-compose --version
else
  echo "  ❌ Docker Compose non installé"
fi

echo ""
echo "🐍 Python:"
if command -v python3 &> /dev/null; then
  echo "  ✅ Python 3 installé"
  python3 --version
else
  echo "  ❌ Python 3 non installé"
fi

echo ""
echo "📦 Vérification du serveur:"
if [ -f "docker-compose.yml" ]; then
  echo "  ✅ docker-compose.yml trouvé"
else
  echo "  ❌ docker-compose.yml manquant"
fi

if [ -f "Dockerfile" ]; then
  echo "  ✅ Dockerfile trouvé"
else
  echo "  ❌ Dockerfile manquant"
fi

if [ -d "server" ]; then
  echo "  ✅ Dossier server trouvé"
else
  echo "  ❌ Dossier server manquant"
fi

echo ""
echo "📦 Vérification de l'agent:"
if [ -f "server/agent/agent.py" ]; then
  echo "  ✅ agent.py trouvé"
else
  echo "  ❌ agent.py manquant"
fi

if [ -f "server/agent/install_linux.sh" ]; then
  echo "  ✅ install_linux.sh trouvé"
else
  echo "  ❌ install_linux.sh manquant"
fi

if [ -f "server/agent/hypermonitor-agent.service" ]; then
  echo "  ✅ hypermonitor-agent.service trouvé"
else
  echo "  ❌ hypermonitor-agent.service manquant"
fi

echo ""
echo "📚 Vérification de la documentation:"
for file in README.md QUICK_START.md STARTUP_GUIDE.md; do
  if [ -f "$file" ]; then
    echo "  ✅ $file trouvé"
  else
    echo "  ❌ $file manquant"
  fi
done

echo ""
echo "🎉 Vérification terminée!"
echo ""
echo "Prochaines étapes:"
echo "  1. Lire README.md"
echo "  2. Lire QUICK_START.md"
echo "  3. Exécuter: docker-compose up -d"
echo "  4. Accéder à: http://localhost:8888"
