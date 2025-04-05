# main.py 

import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
from data.api_service import APIService
from data.data_processor import DataProcessor

def main():
    app = QApplication(sys.argv)
    
    # Aplicar o stylesheet global
    app.setStyleSheet("""
        QWidget {
            background-color: #2E2E2E; /* Cinza escuro */
            color: #FFFFFF; /* Texto branco */
            font-family: Arial;
            font-size: 14px;
        }
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
        }
        QCheckBox::indicator:unchecked {
            border: 2px solid #666666;
            background-color: #2E2E2E;
            border-radius: 3px;
        }
        QCheckBox::indicator:checked {
            border: 2px solid #666666;
            background-color: #4CAF50;
            border-radius: 3px;
        }
        QCheckBox::indicator:checked::after {
            content: "";
            position: absolute;
            left: 6px;
            top: 2px;
            width: 4px;
            height: 10px;
            border: solid white;
            border-width: 0 2px 2px 0;
            transform: rotate(45deg);
        }
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QPushButton:pressed {
            background-color: #3d8b40;
        }
        QLabel {
            color: #FFFFFF;
        }
        QTabWidget::pane {
            border: 1px solid #666666;
            background-color: #2E2E2E;
        }
        QTabBar::tab {
            background-color: #3E3E3E;
            color: #FFFFFF;
            padding: 8px 16px;
            border: 1px solid #666666;
            border-bottom: none;
        }
        QTabBar::tab:selected {
            background-color: #4CAF50;
        }
        QTableWidget {
            background-color: #2E2E2E;
            color: #FFFFFF;
            gridline-color: #666666;
            border: 1px solid #666666;
        }
        QTableWidget::item {
            padding: 5px;
        }
        QTableWidget::item:selected {
            background-color: #4CAF50;
        }
        QHeaderView::section {
            background-color: #3E3E3E;
            color: #FFFFFF;
            padding: 5px;
            border: 1px solid #666666;
        }
        QSpinBox {
            background-color: #2E2E2E;
            color: #FFFFFF;
            border: 1px solid #666666;
            padding: 5px;
            border-radius: 3px;
        }
        QSpinBox::up-button, QSpinBox::down-button {
            background-color: #4CAF50;
            border: none;
            border-radius: 2px;
        }
        QSpinBox::up-button:hover, QSpinBox::down-button:hover {
            background-color: #45a049;
        }
        QSpinBox::up-button:pressed, QSpinBox::down-button:pressed {
            background-color: #3d8b40;
        }
        QMenu {
            background-color: #2E2E2E;
            color: #FFFFFF;
            border: 1px solid #666666;
        }
        QMenu::item {
            padding: 5px 20px;
        }
        QMenu::item:selected {
            background-color: #4CAF50;
        }
        QColorDialog {
            background-color: #2E2E2E;
        }
        QColorDialog QLabel {
            color: #FFFFFF;
        }
    """)
    
    # Criar e mostrar a janela principal
    window = MainWindow()
    window.show()
    
    # Iniciar o loop de eventos
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
