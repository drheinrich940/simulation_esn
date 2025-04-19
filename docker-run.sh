#!/bin/bash

# Script pour construire et exécuter l'application dans Docker

# Couleurs pour les messages
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Construire l'image Docker...${NC}"
docker build -t simulation-esn .

echo -e "${YELLOW}Démarrer le conteneur...${NC}"
echo -e "${GREEN}L'application sera accessible à l'adresse: http://localhost:8501${NC}"
docker run --rm -p 8501:8501 simulation-esn
