#!/bin/bash

# Iniciar Xvfb y suprimir advertencias
Xvfb :99 -ac 2>/dev/null &

# Exportar DISPLAY
export DISPLAY=:99

# Ejecutar el script principal
python3 /Users/javier.martinez32/Documents/Yaencontre/src/main.py

# Detener Xvfb
kill %1

# Registrar la hora actual
time=$(date +"%y-%m-%d")

# Realizar operaciones de git
git add .
git commit -m "Extraccion terminada a $time"
git push
