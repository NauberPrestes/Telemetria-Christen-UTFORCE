# gui/styles.py

DARK_THEME = """
    QWidget {
        background-color: #2E2E2E; /* Cinza escuro */
        color: #FFFFFF; /* Texto branco */
        font-family: Arial;
        font-size: 14px;
    }
    QCheckBox::indicator {
        background-color: #4A4A4A;
        border: 1px solid #FFFFFF;
        width: 15px;
        height: 15px;
    }
    QCheckBox::indicator:checked {
        background-color: #FFFFFF;
    }
    QPushButton {
        background-color: #4A4A4A;
        border: none;
        padding: 5px 10px;
        color: #FFFFFF;
    }
    QPushButton:hover {
        background-color: #606060;
    }
    QComboBox {
        background-color: #4A4A4A;
        border: 1px solid #FFFFFF;
        color: #FFFFFF;
    }
    QLabel {
        color: #FFFFFF;
    }
    QListWidget {
        background-color: #3A3A3A;
        border: 1px solid #FFFFFF;
        color: #FFFFFF;
    }
    QGroupBox {
        border: 2px solid #4A4A4A;
        border-radius: 5px;
        margin-top: 10px;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top center; /* Ajuste conforme necessário */
        padding: 0 3px;
        color: #FFFFFF;
    }
"""

LIGHT_THEME = """
    QWidget {
        background-color: #FFFFFF; /* Branco */
        color: #000000; /* Texto preto */
        font-family: Arial;
        font-size: 14px;
    }
    QCheckBox::indicator {
        background-color: #CCCCCC;
        border: 1px solid #000000;
        width: 15px;
        height: 15px;
    }
    QCheckBox::indicator:checked {
        background-color: #000000;
    }
    QPushButton {
        background-color: #CCCCCC;
        border: none;
        padding: 5px 10px;
        color: #000000;
    }
    QPushButton:hover {
        background-color: #AAAAAA;
    }
    QComboBox {
        background-color: #CCCCCC;
        border: 1px solid #000000;
        color: #000000;
    }
    QLabel {
        color: #000000;
    }
    QListWidget {
        background-color: #F0F0F0;
        border: 1px solid #000000;
        color: #000000;
    }
    QGroupBox {
        border: 2px solid #AAAAAA;
        border-radius: 5px;
        margin-top: 10px;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top center; /* Ajuste conforme necessário */
        padding: 0 3px;
        color: #000000;
    }
"""
