#!/bin/bash

# Script pour gérer les opérations Docker Compose

# Couleurs pour les messages
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Fonction d'aide
show_help() {
    echo -e "${YELLOW}Usage:${NC}"
    echo -e "  $0 [option]"
    echo
    echo -e "${YELLOW}Options:${NC}"
    echo -e "  ${GREEN}dev${NC}       Démarrer en mode développement (avec volumes montés)"
    echo -e "  ${GREEN}prod${NC}      Démarrer en mode production"
    echo -e "  ${GREEN}stop-dev${NC}  Arrêter le mode développement"
    echo -e "  ${GREEN}stop-prod${NC} Arrêter le mode production"
    echo -e "  ${GREEN}logs${NC}      Afficher les logs (mode production)"
    echo -e "  ${GREEN}help${NC}      Afficher cette aide"
}

# Vérifier si un argument a été fourni
if [ $# -eq 0 ]; then
    show_help
    exit 1
fi

# Traiter l'argument
case "$1" in
    dev)
        echo -e "${YELLOW}Démarrage en mode développement...${NC}"
        echo -e "${GREEN}L'application sera accessible à l'adresse: http://localhost:8501${NC}"
        docker-compose up
        ;;
    prod)
        echo -e "${YELLOW}Démarrage en mode production...${NC}"
        echo -e "${GREEN}L'application sera accessible à l'adresse: http://localhost:8501${NC}"
        docker-compose -f docker-compose-prod.yml up -d
        ;;
    stop-dev)
        echo -e "${YELLOW}Arrêt du mode développement...${NC}"
        docker-compose down
        ;;
    stop-prod)
        echo -e "${YELLOW}Arrêt du mode production...${NC}"
        docker-compose -f docker-compose-prod.yml down
        ;;
    logs)
        echo -e "${YELLOW}Affichage des logs (mode production)...${NC}"
        docker-compose -f docker-compose-prod.yml logs -f
        ;;
    help)
        show_help
        ;;
    *)
        echo -e "${RED}Option non reconnue: $1${NC}"
        show_help
        exit 1
        ;;
esac
