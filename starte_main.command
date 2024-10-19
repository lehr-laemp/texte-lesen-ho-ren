#!/bin/bash

# ins Verzeichnis wechseln
cd "$(dirname "$0")"

# virtuelle Umgebung aktivieren
source ./venv/bin/activate

# Script starten
python ./main.py
