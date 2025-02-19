# gui/setup_view.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QMessageBox
)
from PySide6.QtCore import Qt
import random


class SetupView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Layout principal
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Título da página
        self.title = QLabel("Configuração de Setup do Carro")
        self.title.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(self.title, alignment=Qt.AlignCenter)

        # Tabela para exibir os dados de setup
        self.table = QTableWidget(0, 14)
        self.table.setHorizontalHeaderLabels([
            "Setup", "Rear Height", "Front Height", "Rear Push", "Front Push",
            "Preload Springs", "Spring Height", "Tire Calibration", "Rake", "Wing Inclination",
            "Car Weight", "Balance", "Fuel in the Tank", "Lap Time (s)"
        ])
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.horizontalHeader().setDefaultSectionSize(150)
        self.table.horizontalHeader().setMinimumSectionSize(100)
        self.table.horizontalHeader().setStyleSheet("font-size: 12px; font-weight: bold;")
        self.table.resizeColumnsToContents()
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.layout.addWidget(self.table)

        # Botões
        button_layout = QHBoxLayout()
        self.simulate_button = QPushButton("Simular Dados de Setup")
        self.compare_button = QPushButton("Comparar Setups")
        button_layout.addWidget(self.simulate_button)
        button_layout.addWidget(self.compare_button)
        self.layout.addLayout(button_layout)

        # Conectar botões às ações
        self.simulate_button.clicked.connect(self.simulate_data)
        self.compare_button.clicked.connect(self.compare_setups)

        # Dados de setup
        self.setups = []

    def simulate_data(self):
        """
        Simula dados de setup e tempos de volta para várias voltas.
        """
        self.setups.clear()
        self.table.setRowCount(0)

        for lap in range(1, 31):  # 30 voltas simuladas
            setup = {
                "Setup": f"Setup {lap}",
                "Rear Height": round(random.uniform(100, 200), 2),
                "Front Height": round(random.uniform(100, 200), 2),
                "Rear Push": round(random.uniform(0, 50), 2),
                "Front Push": round(random.uniform(0, 50), 2),
                "Preload Springs": round(random.uniform(10, 100), 2),
                "Spring Height": round(random.uniform(20, 80), 2),
                "Tire Calibration": round(random.uniform(20, 40), 2),
                "Rake": round(random.uniform(1, 5), 2),
                "Wing Inclination": round(random.uniform(0, 45), 2),
                "Car Weight": round(random.uniform(800, 1500), 2),
                "Balance": round(random.uniform(-10, 10), 2),
                "Fuel in the Tank": round(random.uniform(10, 100), 2),
                "Lap Time": round(random.uniform(60, 120), 2),
            }
            self.setups.append(setup)
            self.add_setup_to_table(setup)

    def add_setup_to_table(self, setup):
        """
        Adiciona os dados de setup à tabela.
        """
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(setup["Setup"]))
        self.table.setItem(row, 1, QTableWidgetItem(str(setup["Rear Height"])))
        self.table.setItem(row, 2, QTableWidgetItem(str(setup["Front Height"])))
        self.table.setItem(row, 3, QTableWidgetItem(str(setup["Rear Push"])))
        self.table.setItem(row, 4, QTableWidgetItem(str(setup["Front Push"])))
        self.table.setItem(row, 5, QTableWidgetItem(str(setup["Preload Springs"])))
        self.table.setItem(row, 6, QTableWidgetItem(str(setup["Spring Height"])))
        self.table.setItem(row, 7, QTableWidgetItem(str(setup["Tire Calibration"])))
        self.table.setItem(row, 8, QTableWidgetItem(str(setup["Rake"])))
        self.table.setItem(row, 9, QTableWidgetItem(str(setup["Wing Inclination"])))
        self.table.setItem(row, 10, QTableWidgetItem(str(setup["Car Weight"])))
        self.table.setItem(row, 11, QTableWidgetItem(str(setup["Balance"])))
        self.table.setItem(row, 12, QTableWidgetItem(str(setup["Fuel in the Tank"])))
        self.table.setItem(row, 13, QTableWidgetItem(str(setup["Lap Time"])))

    def compare_setups(self):
        """
        Exibe uma mensagem com os dados do setup da volta mais rápida.
        """
        if not self.setups:
            QMessageBox.warning(self, "Sem Dados", "Por favor, simule dados antes de comparar.")
            return

        # Encontrar o setup com o menor tempo de volta
        fastest_setup = min(self.setups, key=lambda x: x["Lap Time"])
        details = "\n".join([
            f"Setup: {fastest_setup['Setup']}",
            f"Lap Time: {fastest_setup['Lap Time']} s",
            f"Rear Height: {fastest_setup['Rear Height']} mm",
            f"Front Height: {fastest_setup['Front Height']} mm",
            f"Rear Push: {fastest_setup['Rear Push']} mm",
            f"Front Push: {fastest_setup['Front Push']} mm",
            f"Preload Springs: {fastest_setup['Preload Springs']} mm",
            f"Spring Height: {fastest_setup['Spring Height']} mm",
            f"Tire Calibration: {fastest_setup['Tire Calibration']} psi",
            f"Rake: {fastest_setup['Rake']}",
            f"Wing Inclination: {fastest_setup['Wing Inclination']} graus",
            f"Car Weight: {fastest_setup['Car Weight']} kg",
            f"Balance: {fastest_setup['Balance']}",
            f"Fuel in the Tank: {fastest_setup['Fuel in the Tank']} l",
        ])
        QMessageBox.information(self, "Setup Mais Rápido", f"O setup mais rápido foi:\n\n{details}")
