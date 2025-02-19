# gui/sensor_selection.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QLabel
from PySide6.QtCore import Signal, Qt

class SensorSelectionWidget(QWidget):
    # Sinal emitido quando as seleções são aplicadas
    selections_applied = Signal(list)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Título do widget
        self.title = QLabel("Selecione os Sensores:")
        self.layout.addWidget(self.title)
        
        # Lista de sensores disponíveis
        self.sensor_list = QListWidget()
        self.sensor_list.setSelectionMode(QListWidget.NoSelection)  # Usar checkboxes
        self.sensor_list.setUniformItemSizes(True)
        
        # Lista de sensores conforme data_simulator.py
        sensors = [
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
        
        # Função para formatar nomes de sensores para melhor legibilidade
        def format_sensor_name(sensor_name):
            return sensor_name.replace('_', ' ').capitalize()
        
        # Adicionar sensores à lista com formatação
        for sensor in sensors:
            formatted_name = format_sensor_name(sensor)
            item = QListWidgetItem(formatted_name)
            item.setData(Qt.UserRole, sensor)  # Armazena o nome original
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.sensor_list.addItem(item)
        
        self.layout.addWidget(self.sensor_list)
        
        # Botão para aplicar seleções
        self.apply_button = QPushButton("Aplicar Seleções")
        self.layout.addWidget(self.apply_button)
        
        # Conectar o botão ao método de aplicação
        self.apply_button.clicked.connect(self.emit_selections)
    
    def emit_selections(self):
        # Obter as seleções verificadas
        selected_sensors = []
        for index in range(self.sensor_list.count()):
            item = self.sensor_list.item(index)
            if item.checkState() == Qt.Checked:
                sensor_name = item.data(Qt.UserRole)  # Nome original do sensor
                selected_sensors.append(sensor_name)
        
        # Emitir o sinal com a lista de sensores selecionados
        self.selections_applied.emit(selected_sensors)
