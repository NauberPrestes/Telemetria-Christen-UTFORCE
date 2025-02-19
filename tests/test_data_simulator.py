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
            "alarme_status",
            "avg_lap_speed",
            "beacon_code",
            "box_voltage",
            "correct_stance",
            "correct_speed",
            "cpu_usage",
            "cumulative_diff",
            "cumulative_time",
            "current",
            "stance",
            "ecu_airbox_temp",
            "ecu_cooler_temp",
            "ecu_engine_safe_hard",
            "ecu_engine_safe_soft",  # Corrigido
            "ecu_fan",
            "ecu_fuel_pressure",
            "ecu_fuel_pump",
            "ecu_fuel_temp",
            "ecu_fuel_total",
            "ecu_gear",
            "ecu_gear_voltage",
            "ecu_kl15",
            "ecu_lambida_1",
            "ecu_lambida_2",
            "ecu_oil_lamp",
            "ecu_oil_pressure",
            "ecu_oil_temp",
            "ecu_push_to_pass_block",
            "ecu_push_to_pass_button",
            "ecu_push_to_pass_delay",
            "ecu_push_to_pass_lamp",
            "ecu_push_to_pass_on",
            "ecu_push_to_pass_remain",
            "ecu_push_to_pass_timer",
            "ecu_pit_limit_button",
            "ecu_pit_limit_on",
            "ecu_powershift_on",
            "ecu_powershift_sensor",
            "ecu_rpm_limit",
            "ecu_rpm",
            "ecu_syncro",
            "ecu_throttle_pedal",
            "ecu_voltage",
            "elipse_lap_time",
            "elipse_time",
            "energy used",
            "front_left_wheel_speed",
            "front_right_wheel_speed",
            "front_brake",
            "fuel_economy",
            "lap_number",
            "lap_fuel_left",
            "lateral_g",
            "logging",
            "longitudinal_g",
            "map_position_d",
            "map_position_x",
            "map_position_y",
            "map_position_z",
            "max_straight_speed",
            "minimal_corner_speed",
            "network_time",
            "oil_temp",
            "pi_ecu_mode",
            "rear_brake",
            "running_lap_time",
            "section_diff",
            "section_time",
            "SOC",
            "SOH",
            "speed",
            "steering",
            "tank_fuel",
            "tank_fuel_used",
            "temperature",
            "voltage",
        ]
        
        # Verificar se todos os sensores estão presentes em cada emissão de dados
        for idx, data in enumerate(self.received_data):
            for sensor in expected_sensors:
                self.assertIn(sensor, data, f"Sensor '{sensor}' ausente na emissão de dados {idx+1}.")

if __name__ == "__main__":
    unittest.main()
