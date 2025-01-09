import os
import json
import csv
from typing import Optional

def detect_file_type(file_path: str) -> str:
    """Erkennt den Dateityp basierend auf Erweiterung und Inhalt."""
    extension = os.path.splitext(file_path)[1].lower()
    
    if extension == '.csv':
        return 'CSV'
    elif extension == '.json':
        return 'JSON'
    elif extension == '.xml':
        return 'XML'
    elif extension in ['.txt', '']:
        # Versuche Format aus Inhalt zu erkennen
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read(1000)  # Erste 1000 Zeichen lesen
            if content.strip().startswith('{'):
                return 'JSON'
            elif content.strip().startswith('<'):
                return 'XML'
            elif ',' in content and '\n' in content:
                return 'CSV'
    
    return 'Unbekannt'

def read_file_content(file_path: str) -> str:
    """Liest und gibt Dateiinhalt basierend auf Typ zurück."""
    file_type = detect_file_type(file_path)
    
    try:
        if file_type == 'CSV':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        elif file_type == 'JSON':
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.dumps(json.load(f), indent=2)
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
    except Exception as e:
        raise IOError(f"Fehler beim Lesen der Datei: {str(e)}")