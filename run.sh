#!/bin/bash
Xvfb :99 -ac &
export DISPLAY=:99

# Carga las variables de entorno
set -a  # automáticamente exporta variables
source /home/javi/Projects/Yaencontre/.env
set +a  # deja de exportar automáticamente

python3 /home/javi/Projects/Yaencontre/src/main.py
kill %1

time=$(date +"%y-%m-%d")

git add .
git commit -m "Extraccion terminada a $time"

git push
