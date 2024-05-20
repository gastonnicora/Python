#!/bin/bash

# Detener y eliminar todos los contenedores
echo "Deteniendo todos los contenedores..."
docker stop $(docker ps -aq)

echo "Eliminando todos los contenedores..."
docker rm $(docker ps -aq)

# Eliminar todas las imágenes
echo "Eliminando todas las imágenes..."
docker rmi $(docker images -q)

# Eliminar todos los volúmenes
echo "Eliminando todos los volúmenes..."
docker volume rm $(docker volume ls -q)

# Eliminar todas las redes no utilizadas
echo "Eliminando todas las redes no utilizadas..."
docker network rm $(docker network ls -q)

# Eliminar caché de construcción
echo "Eliminando caché de construcción..."
docker builder prune -f

# Reconstruir y reiniciar contenedores usando Docker Compose
echo "Reconstruyendo y reiniciando contenedores..."
docker-compose up 
