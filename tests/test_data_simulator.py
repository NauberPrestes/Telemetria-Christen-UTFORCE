# tests/test_data_simulator.py

import unittest
from data.data_simulator import DataSimulator
from PySide6.QtCore import QCoreApplication
import sys

class TestDataSimulator(unittest.TestCase):
    def setUp(self):
        """
        Configura o ambiente de teste. Inicializa o QApplication,
        instancia o DataSimulator e conecta o sinal para coletar dados.
        """
        self.app = QCoreApplication(sys.argv)
        self.simulator = DataSimulator()
        self.received_data = []
        self.simulator.data_generated.connect(self.collect_data)
        self.simulator.start()
    
    def collect_data(self, data):
        """
        Coleta os dados emitidos pelo DataSimulator.
        Após receber 5 emissões, para o simulador e encerra o loop de eventos.
        """
        self.received_data.append(data)
        if len(self.received_data) >= 5:
            self.simulator.stop()
            self.app.quit()
    
    def test_data_generation(self):
        """
        Testa a geração de dados pelo DataSimulator.
        Verifica se 5 conjuntos de dados foram gerados e se todos os sensores estão presentes.
        """
        self.app.exec()
        self.assertEqual(len(self.received_data), 5, "Deve receber exatamente 5 conjuntos de dados.")
        
        # Lista completa de sensores conforme data_simulator.py
        expected_sensors = [
            "DHT - Temperatura",
            "DHT - Umidade",
            "MAX - Temperatura",
            "Volante - Ângulo",
        ]
        
        # Verificar se todos os sensores estão presentes em cada emissão de dados
        for idx, data in enumerate(self.received_data):
            for sensor in expected_sensors:
                self.assertIn(sensor, data, f"Sensor '{sensor}' ausente na emissão de dados {idx+1}.")

if __name__ == "__main__":
    unittest.main()
