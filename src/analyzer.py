import os
import json
from typing import Dict, Any, Optional
from langchain_community.llms import Ollama
from .utils import detect_file_type, read_file_content
from .config import DEFAULT_MODEL

class DataAnalyzer:
    """Hauptklasse für die Analyse von Datendateien mittels lokaler Ollama-Installation."""
    
    def __init__(self, model: str = DEFAULT_MODEL):
        """Initialisiert den DataAnalyzer mit einem Ollama-Modell."""
        try:
            self.llm = Ollama(model=model)
        except Exception as e:
            raise ConnectionError(
                f"Fehler beim Initialisieren von Ollama mit Modell {model}. "
                "Bitte stelle sicher, dass Ollama läuft und das Modell verfügbar ist."
            ) from e
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """
        Analysiert eine Datendatei mithilfe von Ollama.
        
        Args:
            file_path: Pfad zur zu analysierenden Datei
            
        Returns:
            Dictionary mit Analyseergebnissen
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Datei nicht gefunden: {file_path}")
        
        # Dateityp erkennen
        file_type = detect_file_type(file_path)
        
        # Dateiinhalt lesen
        content = read_file_content(file_path)
        
        # Prompt für Ollama vorbereiten
        prompt = self._create_analysis_prompt(content, file_type)
        
        # Analyse von Ollama abrufen
        analysis = self._query_ollama(prompt)
        
        return self._process_analysis(analysis)
    
    def _create_analysis_prompt(self, content: str, file_type: str) -> str:
        """Erstellt einen Prompt für Ollama zur Analyse der Datei."""
        return f"""Analysiere die folgende {file_type}-Datei und gib eine strukturierte Analyse zurück.
Formatiere deine Antwort in klar abgegrenzte Abschnitte mit den folgenden Überschriften:

STRUKTUR:
[Beschreibe hier die grundlegende Datenstruktur, Spalten/Felder und deren Bedeutung]

QUALITÄT:
[Bewerte hier die Datenqualität, identifiziere Probleme wie fehlende Werte, Inkonsistenzen etc.]

TRANSFORMATIONEN:
[Schlage hier mögliche Verbesserungen und Transformationen vor]

ANWENDUNGSFÄLLE:
[Liste hier potenzielle Verwendungsmöglichkeiten der Daten auf]

Hier ist der Dateiinhalt zur Analyse:
{content[:1000]}  # Nur eine Stichprobe senden, um Token-Limits zu vermeiden
"""
    
    def _query_ollama(self, prompt: str) -> str:
        """Sendet eine Anfrage an die lokale Ollama-Instanz via Langchain."""
        try:
            return self.llm.invoke(prompt)
        except Exception as e:
            raise ConnectionError(f"Fehler bei der Anfrage an Ollama: {str(e)}")
    
    def _process_analysis(self, analysis: str) -> Dict[str, Any]:
        """Verarbeitet und strukturiert die Analyseantwort."""
        try:
            sections = {
                'struktur': 'STRUKTUR:',
                'qualitaet': 'QUALITÄT:',
                'transformationen': 'TRANSFORMATIONEN:',
                'anwendungsfaelle': 'ANWENDUNGSFÄLLE:'
            }
            
            structured_analysis = {}
            
            # Extrahiere jeden Abschnitt
            for key, header in sections.items():
                start_idx = analysis.find(header)
                if start_idx != -1:
                    # Finde den nächsten Header oder das Ende des Textes
                    next_idx = float('inf')
                    for next_header in sections.values():
                        next_start = analysis.find(next_header, start_idx + len(header))
                        if next_start != -1 and next_start < next_idx:
                            next_idx = next_start
                    
                    if next_idx == float('inf'):
                        section_text = analysis[start_idx + len(header):].strip()
                    else:
                        section_text = analysis[start_idx + len(header):next_idx].strip()
                    
                    structured_analysis[key] = section_text
            
            return {
                'rohe_analyse': analysis,
                'strukturierte_analyse': structured_analysis
            }
            
        except Exception as e:
            return {
                'rohe_analyse': analysis,
                'strukturierte_analyse': {
                    'struktur': 'Fehler bei der Strukturierung der Analyse',
                    'qualitaet': 'Fehler bei der Qualitätsanalyse',
                    'transformationen': 'Fehler bei den Transformationsvorschlägen',
                    'anwendungsfaelle': 'Fehler bei den Anwendungsfällen'
                }
            }