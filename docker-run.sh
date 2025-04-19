#!/bin/bash
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Build docker image...${NC}"
docker build -t simulation-esn .

echo -e "${YELLOW}Run docker container...${NC}"
echo -e "${GREEN}The application will be available at: http://localhost:8501${NC}"
docker run --rm -p 8501:8501 simulation-esn
