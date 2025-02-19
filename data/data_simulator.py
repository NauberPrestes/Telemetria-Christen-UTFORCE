# data/data_simulator.py

from PySide6.QtCore import QObject, QThread, Signal
import random
import time

class DataSimulator(QObject):
    data_generated = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.running = False
    
    def start(self):
        self.running = True
        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.run)
        self.thread.start()
    
    def run(self):
        while self.running:
            # Simula os dados dos sensores
            sensor_data = {
                "alarme_status": random.choice([0, 1]),  # 0: Desligado, 1: Ligado
                "avg_lap_speed": random.uniform(150.0, 200.0),
                "beacon_code": random.randint(1000, 9999),
                "box_voltage": random.uniform(12.0, 14.0),
                "correct_stance": random.choice([0, 1]),
                "correct_speed": random.choice([0, 1]),
                "cpu_usage": random.uniform(0.0, 100.0),
                "cumulative_diff": random.uniform(-5.0, 5.0),
                "cumulative_time": random.uniform(0.0, 1000.0),
                "current": random.uniform(0.0, 100.0),
                "stance": random.uniform(0.0, 100.0),
                "ecu_airbox_temp": random.uniform(-40.0, 150.0),
                "ecu_cooler_temp": random.uniform(0.0, 100.0),
                "ecu_engine_safe_hard": random.choice([0, 1]),
                "ecu_engine_safe_soft": random.choice([0, 1]),  # Corrigido
                "ecu_fan": random.choice([0, 1]),
                "ecu_fuel_pressure": random.uniform(0.0, 100.0),
                "ecu_fuel_pump": random.choice([0, 1]),
                "ecu_fuel_temp": random.uniform(-40.0, 150.0),
                "ecu_fuel_total": random.uniform(0.0, 1000.0),
                "ecu_gear": random.randint(1, 8),
                "ecu_gear_voltage": random.uniform(0.0, 5.0),
                "ecu_kl15": random.choice([0, 1]),
                "ecu_lambida_1": random.uniform(0.0, 100.0),
                "ecu_lambida_2": random.uniform(0.0, 100.0),
                "ecu_oil_lamp": random.choice([0, 1]),
                "ecu_oil_pressure": random.uniform(20.0, 100.0),
                "ecu_oil_temp": random.uniform(-40.0, 150.0),
                "ecu_push_to_pass_block": random.choice([0, 1]),
                "ecu_push_to_pass_button": random.choice([0, 1]),
                "ecu_push_to_pass_delay": random.uniform(0.0, 10.0),
                "ecu_push_to_pass_lamp": random.choice([0, 1]),
                "ecu_push_to_pass_on": random.choice([0, 1]),
                "ecu_push_to_pass_remain": random.uniform(0.0, 10.0),
                "ecu_push_to_pass_timer": random.uniform(0.0, 60.0),
                "ecu_pit_limit_button": random.choice([0, 1]),
                "ecu_pit_limit_on": random.choice([0, 1]),
                "ecu_powershift_on": random.choice([0, 1]),
                "ecu_powershift_sensor": random.uniform(0.0, 100.0),
                "ecu_rpm_limit": random.uniform(3000.0, 10000.0),
                "ecu_rpm": random.uniform(0.0, 12000.0),
                "ecu_syncro": random.choice([0, 1]),
                "ecu_throttle_pedal": random.uniform(0.0, 100.0),
                "ecu_voltage": random.uniform(0.0, 14.0),
                "elipse_lap_time": random.uniform(60.0, 300.0),
                "elipse_time": random.uniform(0.0, 1000.0),
                "energy used": random.uniform(-80.0, 80.0),
                "front_left_wheel_speed": random.uniform(0.0, 300.0),
                "front_right_wheel_speed": random.uniform(0.0, 300.0),
                "front_brake": random.choice([0, 1]),
                "fuel_economy": random.uniform(0.0, 20.0),
                "lap_number": random.randint(1, 100),
                "lap_fuel_left": random.uniform(0.0, 100.0),
                "lateral_g": random.uniform(-3.0, 3.0),
                "logging": random.choice([0, 1]),
                "longitudinal_g": random.uniform(-3.0, 3.0),
                "map_position_d": random.uniform(0.0, 100.0),
                "map_position_x": random.uniform(0.0, 1000.0),
                "map_position_y": random.uniform(0.0, 1000.0),
                "map_position_z": random.uniform(0.0, 1000.0),
                "max_straight_speed": random.uniform(200.0, 300.0),
                "minimal_corner_speed": random.uniform(100.0, 200.0),
                "network_time": time.time(),
                "oil_temp": random.uniform(-40.0, 150.0),
                "pi_ecu_mode": random.choice([0, 1]),
                "rear_brake": random.choice([0, 1]),
                "running_lap_time": random.uniform(60.0, 300.0),
                "section_diff": random.uniform(-5.0, 5.0),
                "section_time": random.uniform(0.0, 1000.0),
                "SOC": random.uniform(0.0, 100.0),
                "SOH": random.uniform(0.0, 100.0),
                "speed": random.uniform(0.0, 300.0),
                "steering": random.uniform(-45.0, 45.0),
                "tank_fuel": random.uniform(0.0, 100.0),
                "tank_fuel_used": random.uniform(0.0, 100.0),
                "temperature": random.uniform(0.0, 100.0),
                "voltage": random.uniform(0.0, 300.0)
            }
            self.data_generated.emit(sensor_data)
            time.sleep(0.1)  # Simula 10 Hz de atualização
    
    def stop(self):
        self.running = False
        if self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()
