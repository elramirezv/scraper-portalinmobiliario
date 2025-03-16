#!/bin/bash

# Configuración
# Get SERVER_IP from .env file if it exists
if [ -f ".env" ]; then
  source .env
else
  echo -e "${RED}Error: .env file not found. SERVER_IP is required.${NC}"
  exit 1
fi

# Verify SERVER_IP is set
if [ -z "$SERVER_IP" ]; then
  echo -e "${RED}Error: SERVER_IP not defined in .env file${NC}"
  exit 1
fi

SERVER_USER="root"  # Cambia esto por tu usuario en el servidor
REMOTE_DIR="/app"   # Directorio en el servidor donde se copiarán los archivos

# Colores para mensajes
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Iniciando despliegue en $SERVER_IP...${NC}"

# Verificar que existan los archivos necesarios
echo "Verificando archivos locales..."
missing_files=false

if [ ! -d "services" ]; then
    echo -e "${RED}Error: Carpeta 'services' no encontrada${NC}"
    missing_files=true
fi

if [ ! -f "main.py" ]; then
    echo -e "${RED}Error: Archivo 'main.py' no encontrado${NC}"
    missing_files=true
fi

if [ ! -f "Dockerfile" ]; then
    echo -e "${RED}Error: Archivo 'Dockerfile' no encontrado${NC}"
    missing_files=true
fi

if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}Error: Archivo 'docker-compose.yml' no encontrado${NC}"
    missing_files=true
fi

if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}Error: Archivo 'requirements.txt' no encontrado${NC}"
    missing_files=true
fi

if [ ! -f ".env" ]; then
    echo -e "${RED}Advertencia: Archivo '.env' no encontrado${NC}"
    read -p "¿Continuar sin el archivo .env? (s/n): " continue_without_env
    if [[ $continue_without_env != "s" && $continue_without_env != "S" ]]; then
        echo -e "${RED}Aborting: Falta archivo .env${NC}"
        exit 1
    fi
fi

if [ "$missing_files" = true ]; then
    echo -e "${RED}Aborting: Faltan archivos necesarios${NC}"
    exit 1
fi

# Crear directorio temporal para empaquetar archivos
echo "Preparando archivos para transferencia..."
temp_dir=$(mktemp -d)
cp -r services main.py Dockerfile docker-compose.yml requirements.txt "$temp_dir"
# Copiar .env si existe
if [ -f ".env" ]; then
    cp .env "$temp_dir"
    echo "Archivo .env incluido en la transferencia."
fi

# Copiar archivos al servidor
echo "Copiando archivos al servidor..."
scp -r "$temp_dir"/* "$SERVER_USER@$SERVER_IP:$REMOTE_DIR"

if [ $? -ne 0 ]; then
    echo -e "${RED}Error: No se pudieron copiar los archivos al servidor${NC}"
    rm -rf "$temp_dir"
    exit 1
fi

# Limpiar directorio temporal
rm -rf "$temp_dir"

# Entrar al servidor y ejecutar Docker Compose
echo "Conectando al servidor para desplegar con Docker Compose..."
ssh "$SERVER_USER@$SERVER_IP" << 'EOC'
cd /app

# Verificar que Docker Compose esté instalado
if ! command -v docker compose &> /dev/null; then
    echo "Docker Compose no está instalado. Intentando instalar..."
    if command -v apt-get &> /dev/null; then
        apt-get update && apt-get install -y docker-compose-plugin
    else
        echo "No se pudo instalar Docker Compose automáticamente. Por favor, instálelo manualmente."
        exit 1
    fi
fi

# Verificar que el directorio de datos existe
mkdir -p $(dirname $(grep -o '/app/already_seen.json' docker-compose.yml | head -1))
touch $(grep -o '/app/already_seen.json' docker-compose.yml | head -1)
chmod 666 $(grep -o '/app/already_seen.json' docker-compose.yml | head -1)

# Detener y eliminar contenedores existentes
echo "Deteniendo servicios existentes..."
docker compose down

# Construir y ejecutar con Docker Compose
echo "Construyendo y ejecutando con Docker Compose..."
docker compose up -d --build

if [ $? -ne 0 ]; then
    echo "Error: No se pudo desplegar con Docker Compose"
    exit 1
fi

# Verificar que los contenedores estén en ejecución
echo "Verificando que los servicios estén en ejecución..."
if docker compose ps | grep -q "Up"; then
    echo "Servicios ejecutándose correctamente"
else
    echo "Error: Los servicios no están en ejecución"
    exit 1
fi

# Limpiar recursos no utilizados
echo "Eliminando recursos no utilizados con docker system prune -a..."
docker system prune -a -f
EOC

if [ $? -ne 0 ]; then
    echo -e "${RED}Error durante la ejecución de comandos en el servidor${NC}"
    exit 1
fi

echo -e "${GREEN}¡Despliegue completado exitosamente!${NC}"
