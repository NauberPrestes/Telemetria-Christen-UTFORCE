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
            "DHT - Temperatura",
            "DHT - Umidade",
            "MAX - Temperatura",
            "Volante - Ângulo",
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
