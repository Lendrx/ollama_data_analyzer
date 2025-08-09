# Ollama Data Analyzer

Dieses Projekt implementiert einen RAG-basierten Chatbot, der auf einer Sammlung von Finanzberichten trainiert wurde. Er kann Fragen zu Jahresabschlüssen beantworten und bietet genaue und kontextbezogene Informationen.

![Demo GIF](assets/demo.gif)

Ein Python-Tool - Analyse von Dateistrukturen und Datenqualität.

*Ollama LLMs*

## Features
- Automatische Erkennung von Dateiformaten (CSV, JSON, XML)
- Qualitätsanalyse von Datensätzen
- Transformationsempfehlungen
- Speicherung von Analyseergebnissen
- Unterstützung für unstrukturierte und problematische Daten

## Voraussetzungen
- Python 3.10+
- Ollama ([Installation](https://ollama.ai/))
- Mistral Modell für Ollama

## Schnellstart
```bash
# Ollama starten (in separatem Terminal)
ollama run mistral

# Beispielanalyse durchführen
python analyze_data.py
```

## Beispiel
```python
from src.analyzer import DataAnalyzer

# Analyzer initialisieren
analyzer = DataAnalyzer()

# Datei analysieren
ergebnisse = analyzer.analyze_file("pfad/zur/datei.csv")
```

## Struktur
```
ollama-data-analyzer/
├── src/               # Quellcode
├── tests/             # Tests
├── test_data/         # Testdateien
├── analysis_results/  # Gespeicherte Analysen
├── requirements.txt   # Abhängigkeiten
└── analyze_data.py    # Beispielskript
```
