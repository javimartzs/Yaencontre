#!/bin/bash

# Iniciar Xvfb y suprimir advertencias
Xvfb :99 -ac 2>/dev/null &

# Exportar DISPLAY
export DISPLAY=:99

# Especificar la ruta completa del intérprete de Python
PYTHON_INTERPRETER="/usr/bin/python3"  # Cambia esta ruta si es diferente en tu sistema

# Especificar la ruta completa del script .py
SCRIPT_PATH="/Users/javier.martinez32/Documents/Yaencontre/src/main.py"  # Cambia esta ruta si es diferente

# Cargar las variables de entorno
source /Users/javier.martinez32/Documents/Yaencontre/.env

# Ejecutar el script principal
$PYTHON_INTERPRETER $SCRIPT_PATH

# Detener Xvfb
kill %1

# Registrar la hora actual
time=$(date +"%y-%m-%d")

# Realizar operaciones de git
git add .
git commit -m "Extraccion terminada a $time"
git push
