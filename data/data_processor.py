# data/data_processor.py

from PySide6.QtCore import QObject, Signal

class DataProcessor(QObject):
    data_updated = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def process_data(self, raw_data):
        """
        Processa os dados brutos e emite um sinal com os dados processados.
        """
        # Aqui você pode adicionar lógica de processamento dos dados
        # Para simplificar, vamos emitir os dados brutos diretamente
        processed_data = raw_data  # Substitua por processamento real se necessário
        self.data_updated.emit(processed_data)
