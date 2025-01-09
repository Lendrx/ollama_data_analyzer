from src.analyzer import DataAnalyzer
import os
from datetime import datetime

def save_analysis(file_path: str, save_dir: str = "analysis_results"):
    """
    Analysiert eine Datei und speichert die Ergebnisse in einer Textdatei.
    
    Args:
        file_path: Pfad zur zu analysierenden Datei
        save_dir: Verzeichnis für die Analyseergebnisse
    """
    # Erstelle das Verzeichnis für die Ergebnisse, falls es nicht existiert
    os.makedirs(save_dir, exist_ok=True)
    
    # Initialisiere den Analyzer
    analyzer = DataAnalyzer()
    
    # Analysiere die Datei
    ergebnisse = analyzer.analyze_file(file_path)
    
    # Erstelle einen Dateinamen für die Ergebnisse
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.basename(file_path)
    result_file = f"{save_dir}/analyse_{base_name}_{timestamp}.txt"
    
    # Speichere die Ergebnisse
    with open(result_file, "w", encoding="utf-8") as f:
        f.write(f"Analyse für: {file_path}\n")
        f.write(f"Durchgeführt am: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*50 + "\n\n")
        
        f.write("=== Strukturanalyse ===\n")
        f.write(ergebnisse['strukturierte_analyse']['struktur'])
        f.write("\n\n")
        
        f.write("=== Qualitätsanalyse ===\n")
        f.write(ergebnisse['strukturierte_analyse']['qualitaet'])
        f.write("\n\n")
        
        f.write("=== Transformationsempfehlungen ===\n")
        f.write(ergebnisse['strukturierte_analyse']['transformationen'])
        f.write("\n\n")
        
        f.write("=== Mögliche Anwendungsfälle ===\n")
        f.write(ergebnisse['strukturierte_analyse']['anwendungsfaelle'])
        
    print(f"Analyse wurde gespeichert in: {result_file}")
    return result_file

# Beispielnutzung
if __name__ == "__main__":
    # Liste der zu analysierenden Dateien
    files_to_analyze = [
        "test_data/messy_data.csv",
        "test_data/inconsistent_data.json",
        "test_data/broken_format.xml",
        "test_data/mixed_formats.txt"
    ]
    
    for file_path in files_to_analyze:
        try:
            save_analysis(file_path)
            print(f"✓ Analyse für {file_path} abgeschlossen\n")
        except Exception as e:
            print(f"✗ Fehler bei der Analyse von {file_path}: {str(e)}\n")