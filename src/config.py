import os
from dotenv import load_dotenv

# Umgebungsvariablen laden
load_dotenv()

# Ollama-Konfiguration für lokale Installation
DEFAULT_MODEL = "mistral"  # Standard-Modell

# Optionale Konfigurationen
MAX_CONTENT_LENGTH = 1000000  # Maximale Inhaltslänge für Analyse
SUPPORTED_FILE_TYPES = ['CSV', 'JSON', 'XML', 'TXT']