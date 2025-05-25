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
BACKUP_DIR="/app/backups"  # Directorio para backups

# Colores para mensajes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para logging
log() {
    echo -e "${2:-$GREEN}$1${NC}"
}

# Función para manejar errores
handle_error() {
    log "Error: $1" "$RED"
    exit 1
}

log "Iniciando despliegue en $SERVER_IP..."

# Verificar que existan los archivos necesarios
log "Verificando archivos locales..."
missing_files=false

required_files=(
    "services"
    "main.py"
    "Dockerfile"
    "docker-compose.yml"
    "requirements.txt"
)

for file in "${required_files[@]}"; do
    if [ ! -e "$file" ]; then
        log "Error: '$file' no encontrado" "$RED"
        missing_files=true
    fi
done

if [ "$missing_files" = true ]; then
    handle_error "Faltan archivos necesarios"
fi

# Crear directorio temporal para empaquetar archivos
log "Preparando archivos para transferencia..."
temp_dir=$(mktemp -d)
cp -r services main.py Dockerfile docker-compose.yml requirements.txt "$temp_dir"

# Copiar .env si existe
if [ -f ".env" ]; then
    cp .env "$temp_dir"
    log "Archivo .env incluido en la transferencia."
fi

# Copiar archivos al servidor
log "Copiando archivos al servidor..."
scp -r "$temp_dir"/* "$SERVER_USER@$SERVER_IP:$REMOTE_DIR" || handle_error "No se pudieron copiar los archivos al servidor"

# Limpiar directorio temporal
rm -rf "$temp_dir"

# Entrar al servidor y ejecutar Docker Compose
log "Conectando al servidor para desplegar con Docker Compose..."
ssh "$SERVER_USER@$SERVER_IP" << 'EOC'
cd /app

# Función para logging en el servidor
log() {
    echo -e "\033[0;32m$1\033[0m"
}

# Función para manejar errores en el servidor
handle_error() {
    echo -e "\033[0;31mError: $1\033[0m"
    exit 1
}

# Verificar que Docker esté instalado
if ! command -v docker &> /dev/null; then
    log "Docker no está instalado. Intentando instalar..."
    if command -v apt-get &> /dev/null; then
        apt-get update && apt-get install -y docker.io || handle_error "No se pudo instalar Docker"
    else
        handle_error "No se pudo instalar Docker automáticamente"
    fi
fi

# Verificar que Docker Compose esté instalado
if ! command -v docker compose &> /dev/null; then
    log "Docker Compose no está instalado. Intentando instalar..."
    if command -v apt-get &> /dev/null; then
        apt-get update && apt-get install -y docker-compose-plugin || handle_error "No se pudo instalar Docker Compose"
    else
        handle_error "No se pudo instalar Docker Compose automáticamente"
    fi
fi

# Crear directorios necesarios
log "Creando directorios necesarios..."
mkdir -p /app/data
mkdir -p /app/logs
mkdir -p /app/backups

# Crear archivo de datos si no existe
touch /app/already_seen.json
chmod 666 /app/already_seen.json

# Detener y eliminar contenedores existentes
log "Deteniendo servicios existentes..."
docker compose down

# Limpiar imágenes no utilizadas
log "Limpiando imágenes no utilizadas..."
docker system prune -f

# Construir y ejecutar con Docker Compose
log "Construyendo y ejecutando con Docker Compose..."
docker compose up -d --build || handle_error "No se pudo desplegar con Docker Compose"

# Esperar a que los servicios estén listos
log "Esperando a que los servicios estén listos..."
sleep 10

# Verificar que los contenedores estén en ejecución
log "Verificando que los servicios estén en ejecución..."
if ! docker compose ps | grep -q "Up"; then
    handle_error "Los servicios no están en ejecución"
fi

# Verificar logs de los contenedores
log "Verificando logs de los contenedores..."
docker compose logs --tail=50

# Limpiar recursos no utilizados
log "Eliminando recursos no utilizados..."
docker system prune -a -f

log "¡Despliegue completado exitosamente!"
EOC

if [ $? -ne 0 ]; then
    handle_error "Error durante la ejecución de comandos en el servidor"
fi

log "¡Despliegue completado exitosamente!"
