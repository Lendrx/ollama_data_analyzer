import unittest
from pathlib import Path
from src.analyzer import DataAnalyzer

class TestProblematicData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Wird einmal vor allen Tests ausgeführt."""
        cls.test_data_dir = Path(__file__).parent.parent / 'test_data'
        cls.analyzer = DataAnalyzer()

    def analyze_file(self, filename):
        """Hilfsmethode zur Analyse einer Datei."""
        file_path = self.test_data_dir / filename
        return self.analyzer.analyze_file(str(file_path))

    def check_analysis_quality(self, results):
        """Überprüft die Qualität der Analyse."""
        self.assertIn('strukturierte_analyse', results)
        analysis = results['strukturierte_analyse']
        
        # Prüfe auf erwartete Schlüssel
        expected_keys = ['struktur', 'qualitaet', 'transformationen', 'anwendungsfaelle']
        for key in expected_keys:
            self.assertTrue(
                any(key in k for k in analysis.keys()),
                f"Erwarteter Schlüssel {key} nicht gefunden"
            )
        
        # Prüfe auf nicht-leere Analysen
        for key, value in analysis.items():
            self.assertTrue(
                value and len(value.strip()) > 0,
                f"Leere Analyse für {key}"
            )

    def test_messy_csv(self):
        """Testet die Analyse von unordentlichen CSV-Daten."""
        results = self.analyze_file('messy_data.csv')
        self.check_analysis_quality(results)
        # Prüfe, ob Datenqualitätsprobleme erkannt wurden
        quality = results['strukturierte_analyse'].get('qualitaet', '').lower()
        issues = ['leer', 'fehlt', 'ungültig', 'format']
        self.assertTrue(
            any(issue in quality for issue in issues),
            "Datenqualitätsprobleme wurden nicht erkannt"
        )

    def test_inconsistent_json(self):
        """Testet die Analyse von inkonsistenten JSON-Daten."""
        results = self.analyze_file('inconsistent_data.json')
        self.check_analysis_quality(results)
        # Prüfe auf erkannte Inkonsistenzen
        analysis = results['strukturierte_analyse']
        self.assertTrue(
            any('konsistent' in str(v).lower() for v in analysis.values()),
            "Inkonsistenzen wurden nicht erkannt"
        )

    def test_broken_xml(self):
        """Testet die Analyse von fehlerhaftem XML."""
        results = self.analyze_file('broken_format.xml')
        self.check_analysis_quality(results)
        # Prüfe auf erkannte XML-Probleme
        structure = results['strukturierte_analyse'].get('struktur', '').lower()
        self.assertTrue(
            any(issue in structure for issue in ['fehler', 'ungültig', 'struktur']),
            "XML-Strukturprobleme wurden nicht erkannt"
        )

    def test_mixed_formats(self):
        """Testet die Analyse von gemischten Datenformaten."""
        results = self.analyze_file('mixed_formats.txt')
        self.check_analysis_quality(results)
        # Prüfe auf Erkennung verschiedener Formate
        analysis = results['strukturierte_analyse']
        formats = ['csv', 'json', 'xml', 'text']
        self.assertTrue(
            any(fmt in str(analysis).lower() for fmt in formats),
            "Gemischte Formate wurden nicht erkannt"
        )

    def test_duplicate_data(self):
        """Testet die Analyse von Duplikaten."""
        results = self.analyze_file('duplicate_data.csv')
        self.check_analysis_quality(results)
        # Prüfe auf erkannte Duplikate
        quality = results['strukturierte_analyse'].get('qualitaet', '').lower()
        self.assertTrue(
            any(term in quality for term in ['duplikat', 'wiederhol', 'mehrfach']),
            "Duplikate wurden nicht erkannt"
        )

if __name__ == '__main__':
    unittest.main()