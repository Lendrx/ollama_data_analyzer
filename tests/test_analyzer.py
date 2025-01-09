import unittest
import os
from pathlib import Path
from src.analyzer import DataAnalyzer
from src.utils import detect_file_type, read_file_content

class TestDataAnalyzer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Wird einmal vor allen Tests ausgeführt."""
        cls.test_data_dir = Path(__file__).parent.parent / 'test_data'
        cls.analyzer = DataAnalyzer()

    def test_file_type_detection(self):
        """Testet die Erkennung verschiedener Dateitypen."""
        test_files = {
            'sample_data.csv': 'CSV',
            'config_example.json': 'JSON',
            'inventory.xml': 'XML'
        }
        
        for filename, expected_type in test_files.items():
            file_path = self.test_data_dir / filename
            detected_type = detect_file_type(str(file_path))
            self.assertEqual(
                detected_type, 
                expected_type, 
                f"Fehler bei {filename}: Erwartet {expected_type}, erkannt als {detected_type}"
            )

    def test_file_content_reading(self):
        """Testet das Lesen verschiedener Dateiformate."""
        test_files = ['sample_data.csv', 'config_example.json', 'inventory.xml']
        
        for filename in test_files:
            file_path = self.test_data_dir / filename
            try:
                content = read_file_content(str(file_path))
                self.assertIsNotNone(content)
                self.assertIsInstance(content, str)
                self.assertTrue(len(content) > 0)
            except Exception as e:
                self.fail(f"Fehler beim Lesen von {filename}: {str(e)}")

    def test_analyzer_initialization(self):
        """Testet die Initialisierung des Analyzers."""
        self.assertIsNotNone(self.analyzer)
        self.assertEqual(self.analyzer.llm.model, "mistral")

    def test_csv_analysis(self):
        """Testet die Analyse einer CSV-Datei."""
        csv_path = self.test_data_dir / 'sample_data.csv'
        try:
            results = self.analyzer.analyze_file(str(csv_path))
            
            # Prüfe Struktur der Ergebnisse
            self.assertIn('strukturierte_analyse', results)
            self.assertIn('rohe_analyse', results)
            
            # Prüfe erwartete Schlüssel in der strukturierten Analyse
            structured = results['strukturierte_analyse']
            expected_keys = ['struktur', 'qualitaet', 'transformationen', 'anwendungsfaelle']
            for key in expected_keys:
                self.assertTrue(
                    any(key in k for k in structured.keys()),
                    f"Erwarteter Schlüssel {key} nicht in Analyseergebnissen gefunden"
                )
            
        except Exception as e:
            self.fail(f"Fehler bei der Analyse der CSV-Datei: {str(e)}")

    def test_json_analysis(self):
        """Testet die Analyse einer JSON-Datei."""
        json_path = self.test_data_dir / 'config_example.json'
        try:
            results = self.analyzer.analyze_file(str(json_path))
            self.assertIn('strukturierte_analyse', results)
        except Exception as e:
            self.fail(f"Fehler bei der Analyse der JSON-Datei: {str(e)}")

    def test_xml_analysis(self):
        """Testet die Analyse einer XML-Datei."""
        xml_path = self.test_data_dir / 'inventory.xml'
        try:
            results = self.analyzer.analyze_file(str(xml_path))
            self.assertIn('strukturierte_analyse', results)
        except Exception as e:
            self.fail(f"Fehler bei der Analyse der XML-Datei: {str(e)}")

    def test_error_handling(self):
        """Testet die Fehlerbehandlung bei nicht existierenden Dateien."""
        with self.assertRaises(FileNotFoundError):
            self.analyzer.analyze_file("nicht_existierende_datei.txt")

if __name__ == '__main__':
    unittest.main()