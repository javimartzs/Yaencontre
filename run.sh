#!/bin/bash

# Iniciar Xvfb y suprimir advertencias
Xvfb :99 -ac 2>/dev/null &

# Exportar DISPLAY
export DISPLAY=:99

# Cargar las variables de entorno
set -a
source /home/javi/Projects/Yaencontre/.env
set +a

# Ejecutar el script principal
python3 /home/javi/Projects/Yaencontre/src/main.py

# Detener Xvfb
kill %1

# Registrar la hora actual
time=$(date +"%y-%m-%d")

# Realizar operaciones de git
git add .
git commit -m "Extraccion terminada a $time"
git push