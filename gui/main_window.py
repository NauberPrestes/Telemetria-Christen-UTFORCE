# gui/main_window.py

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QGridLayout, QTabWidget,
    QLabel, QPushButton, QDialog, QFormLayout, QMessageBox,
    QListWidget, QListWidgetItem, QHBoxLayout, QApplication, QSpinBox,QMenu,QColorDialog
)
from PySide6.QtCore import Qt, QMimeData, QSize, QPoint
from PySide6.QtGui import QPalette, QColor, QDrag, QCursor, QPixmap, QPainter, QBrush,QAction
from gui.sensor_selection import SensorSelectionWidget
from gui.comparison_view import ComparisonView
from gui.styles import DARK_THEME, LIGHT_THEME
from gui.setup_view import SetupView
from gui.car_monitoring_view import CarMonitoringView
from pyqtgraph import PlotWidget, mkPen
import pyqtgraph as pg
import json
import os
import time
import math
from data.api_service import APIService


class DraggablePlotWidget(PlotWidget):
    def __init__(self, title, main_window, parent=None):
        super().__init__(parent=parent)
        self.main_window = main_window  # Referência à MainWindow
        self.setTitle(title)
        self.setAcceptDrops(True)
        self.drag_start_position = None
        self.current_chart_type = "line"

        # Configuração inicial do plot
        self.setBackground('#2E2E2E' if self.main_window.current_theme == "Dark" else '#FFFFFF')
        self.setTitle(title)
        self.setLabel('left', 'Valor')
        self.setLabel('bottom', 'Tempo (s)')
        self.plot_item = self.plot([], [], pen=mkPen(color='r', width=2))

        # Adicionar menu de contexto
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.open_context_menu)

    def open_context_menu(self, position):
        """
        Menu de contexto para alterar o tipo de gráfico.
        """
        menu = QMenu(self)

        line_chart_action = QAction("Gráfico de Linha", self)
        bar_chart_action = QAction("Gráfico de Barra", self)
        radial_chart_action = QAction("Gráfico Radial", self)

        line_chart_action.triggered.connect(lambda: self.set_chart_type("line"))
        bar_chart_action.triggered.connect(lambda: self.set_chart_type("bar"))
        radial_chart_action.triggered.connect(lambda: self.set_chart_type("radial"))

        menu.addAction(line_chart_action)
        menu.addAction(bar_chart_action)
        menu.addAction(radial_chart_action)

        menu.exec(self.mapToGlobal(position))

    def set_chart_type(self, chart_type):
        """
        Alterna o tipo de gráfico.
        """
        self.current_chart_type = chart_type
        self.update_chart()

    def update_chart(self):
        """
        Atualiza o gráfico com base no tipo selecionado.
        """
        self.clear()

        if self.current_chart_type == "line":
            self.plot(self.data_x, self.data_y, pen=mkPen(color='r', width=2))
        elif self.current_chart_type == "bar":
            bg = pg.BarGraphItem(x=self.data_x, height=self.data_y, width=0.1, brush='g')
            self.addItem(bg)
        elif self.current_chart_type == "radial":
            radial_plot = pg.PlotCurveItem(
                x=self.data_x,
                y=self.data_y,
                pen=mkPen(color='b', width=2, style=Qt.DashLine),
                name="Radial"
            )
            self.addItem(radial_plot)

    def add_data_point(self, x, y):
        """
        Adiciona um ponto de dados ao gráfico e atualiza continuamente, mantendo apenas os últimos 100 pontos.
        """
        if not hasattr(self, 'data_x'):
            self.data_x = []
        if not hasattr(self, 'data_y'):
            self.data_y = []

        self.data_x.append(x)
        self.data_y.append(y)

        # Limita os dados a 100 pontos
        if len(self.data_x) > 100:
            self.data_x = self.data_x[-100:]
            self.data_y = self.data_y[-100:]

        # Atualiza o gráfico
        self.update_chart()

    def update_chart(self):
        """
        Atualiza o gráfico com base no tipo selecionado.
        """
        self.clear()  # Limpa o gráfico antes de redesenhar

        if self.current_chart_type == "line":
            self.plot(self.data_x, self.data_y, pen=mkPen(color='r', width=2))
        elif self.current_chart_type == "bar":
            bar_graph = pg.BarGraphItem(x=self.data_x, height=self.data_y, width=0.5, brush='g')
            self.addItem(bar_graph)
        elif self.current_chart_type == "radial":
            radial_plot = pg.PlotCurveItem(
                x=self.data_x,
                y=self.data_y,
                pen=mkPen(color='b', width=2, style=Qt.DashLine),
                name="Radial"
            )
            self.addItem(radial_plot)




    def contextMenuEvent(self, event):
        """
        Sobrescreve o evento de menu de contexto para adicionar opções ao gráfico.
        """
        menu = QMenu(self)

        # Adicionar a opção para alterar a cor da linha
        change_color_action = menu.addAction("Alterar Cor da Linha")
        change_color_action.triggered.connect(self.change_line_color)

        # Executar o menu de contexto
        menu.exec(event.globalPos())

    def change_line_color(self):
        """
        Abre um diálogo para selecionar a cor da linha do gráfico.
        """
        color = QColorDialog.getColor()
        if color.isValid():
            color_hex = color.name()
            print(f"Cor selecionada: {color_hex}")
            self.plot_item.setPen(mkPen(color=color_hex, width=2))  # Atualizar a cor da linha


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.position()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if self.drag_start_position is None:
            return
        distance = (event.position() - self.drag_start_position).manhattanLength()
        if distance < QApplication.startDragDistance():
            return

        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.objectName())  # Enviar identificação do widget
        drag.setMimeData(mime_data)

        # Criar pixmap com sombra
        pixmap = self.grab()
        shadow = QPixmap(pixmap.size())
        shadow.fill(Qt.transparent)

        painter = QPainter(shadow)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(0, 0, 0, 100)))  # Sombra preta semi-transparente
        painter.drawRoundedRect(shadow.rect(), 10, 10)
        painter.end()

        combined = QPixmap(pixmap.size())
        combined.fill(Qt.transparent)

        painter = QPainter(combined)
        painter.drawPixmap(10, 10, shadow)  # Deslocar a sombra
        painter.drawPixmap(0, 0, pixmap)     # Desenhar o pixmap original
        painter.end()

        drag.setPixmap(combined.scaled(200, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # Iniciar o drag
        drag.exec(Qt.MoveAction)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
            self.highlight_target(True)
    
    
    def dragMoveEvent(self, event):
        """Esse método é fundamental para aceitar o drop ao movimentar o mouse dentro do widget."""
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()    


    def dragLeaveEvent(self, event):
        self.highlight_target(False)
        event.accept()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            source_sensor = event.mimeData().text()
            target_sensor = self.objectName()

            # Solicitar confirmação antes de trocar
            confirm = QMessageBox.question(
                self,
                "Confirmar Troca",
                f"Deseja trocar o gráfico '{source_sensor}' com o gráfico '{target_sensor}'?",
                QMessageBox.Yes | QMessageBox.No
            )

            if confirm == QMessageBox.Yes:
                self.main_window.swap_plots(source_sensor, target_sensor)

            self.highlight_target(False)
            event.acceptProposedAction()
        else:
            event.ignore()

    def highlight_target(self, highlight):
        """
        Destaca o gráfico alvo durante o drag-and-drop.
        """
        palette = self.palette()
        if highlight:
            palette.setColor(QPalette.Window, QColor("#FFDD57"))  # Amarelo
            self.setCursor(QCursor(Qt.PointingHandCursor))
        else:
            palette.setColor(QPalette.Window, QColor("#2E2E2E") if self.main_window.current_theme == "Dark" else QColor("#FFFFFF"))
            self.setCursor(QCursor(Qt.ArrowCursor))
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        self.update()

class GridConfigDialog(QDialog):

    def __init__(self, graph_widgets, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configurar Grade dos Gráficos")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Lista de gráficos
        self.graph_list = QListWidget()
        self.graph_list.setSelectionMode(QListWidget.MultiSelection)
        for sensor_name, plot in graph_widgets.items():
            item = QListWidgetItem(f"Gráfico {sensor_name}")
            item.setData(Qt.UserRole, sensor_name)
            self.graph_list.addItem(item)
        self.layout.addWidget(QLabel("Selecionar Gráficos para Configurar:"))
        self.layout.addWidget(self.graph_list)
        
        # Formulário para configuração
        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)
        
        self.row_spin = QSpinBox()
        self.row_spin.setRange(0, 10)
        self.form_layout.addRow("Linha Inicial:", self.row_spin)
        
        self.column_spin = QSpinBox()
        self.column_spin.setRange(0, 10)
        self.form_layout.addRow("Coluna Inicial:", self.column_spin)
        
        self.row_span_spin = QSpinBox()
        self.row_span_spin.setRange(1, 10)
        self.row_span_spin.setValue(1)
        self.form_layout.addRow("Span de Linhas:", self.row_span_spin)
        
        self.col_span_spin = QSpinBox()
        self.col_span_spin.setRange(1, 10)
        self.col_span_spin.setValue(1)
        self.form_layout.addRow("Span de Colunas:", self.col_span_spin)
        
        # Botões para aplicar ou cancelar
        button_layout = QHBoxLayout()
        self.apply_button = QPushButton("Aplicar")
        self.cancel_button = QPushButton("Cancelar")
        button_layout.addWidget(self.apply_button)
        button_layout.addWidget(self.cancel_button)
        self.layout.addLayout(button_layout)
        
        self.apply_button.clicked.connect(self.apply_configuration)
        self.cancel_button.clicked.connect(self.reject)
        
        # Armazenar a configuração
        self.configuration = {}
    
    def apply_configuration(self):
        selected_items = self.graph_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Nenhum Gráfico Selecionado", "Por favor, selecione pelo menos um gráfico para configurar.")
            return
        
        row = self.row_spin.value()
        column = self.column_spin.value()
        row_span = self.row_span_spin.value()
        col_span = self.col_span_spin.value()
        
        # Verificar conflitos de posição
        for item in selected_items:
            sensor_name = item.data(Qt.UserRole)
            for existing_sensor, pos in self.configuration.items():
                if self.positions_overlap(row, column, row_span, col_span, pos['row'], pos['column'], pos['rowSpan'], pos['colSpan']):
                    QMessageBox.warning(
                        self, 
                        "Conflito de Posição", 
                        f"O gráfico '{sensor_name}' está sendo posicionado em uma área já ocupada por '{existing_sensor}'."
                    )
                    return
        
        # Aplicar a configuração para cada gráfico selecionado
        for item in selected_items:
            sensor_name = item.data(Qt.UserRole)
            self.configuration[sensor_name] = {
                'row': row,
                'column': column,
                'rowSpan': row_span,
                'colSpan': col_span
            }
        
        self.accept()
    
    def positions_overlap(self, row1, col1, rowSpan1, colSpan1, row2, col2, rowSpan2, colSpan2):
        # Verificar se duas posições na grade se sobrepõem
        return not (row1 + rowSpan1 <= row2 or row2 + rowSpan2 <= row1 or
                    col1 + colSpan1 <= col2 or col2 + colSpan2 <= col1)
    
    def get_configuration(self):
        return self.configuration

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Telemetria Utforce")
        self.setGeometry(100, 100, 1600, 900)
        
        # Inicialmente, definir o tema escuro
        self.current_theme = "Dark"
        self.apply_theme(DARK_THEME)
        
        # Configuração do layout principal com QTabWidget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        
        # Adicionar Layout de Botões para Alternar Tema e Configurar Grade
        theme_button_layout = QHBoxLayout()
        self.dark_theme_button = QPushButton("Tema Escuro")
        self.light_theme_button = QPushButton("Tema Claro")
        self.configure_grid_button = QPushButton("Configurar Grade")
        theme_button_layout.addWidget(self.dark_theme_button)
        theme_button_layout.addWidget(self.light_theme_button)
        theme_button_layout.addWidget(self.configure_grid_button)
        self.main_layout.addLayout(theme_button_layout)
        
        # Adicionar Tooltips aos Botões
        self.dark_theme_button.setToolTip("Ativar Tema Escuro")
        self.light_theme_button.setToolTip("Ativar Tema Claro")
        self.configure_grid_button.setToolTip("Configurar Posição e Tamanho dos Gráficos")
        
        # Conectar os botões aos métodos correspondentes
        self.dark_theme_button.clicked.connect(lambda: self.change_theme("Dark"))
        self.light_theme_button.clicked.connect(lambda: self.change_theme("Light"))
        self.configure_grid_button.clicked.connect(self.open_grid_config_dialog)
        
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)
        
        # Página de Monitoramento em Tempo Real
        self.monitoring_page = QWidget()
        self.monitoring_layout = QHBoxLayout()
        self.monitoring_page.setLayout(self.monitoring_layout)
        self.tabs.addTab(self.monitoring_page, "Monitoramento em Tempo Real")
        
        # Widget de seleção de sensores (lado esquerdo)
        self.sensor_selection = SensorSelectionWidget()
        self.monitoring_layout.addWidget(self.sensor_selection, stretch=1)
        
        # Área de gráficos organizada em Grid sem Splitters
        self.graph_grid_layout = QGridLayout()
        self.graph_grid_widget = QWidget()
        self.graph_grid_widget.setLayout(self.graph_grid_layout)
        self.monitoring_layout.addWidget(self.graph_grid_widget, stretch=4)
        
        # Inicialização de dados
        self.graph_widgets = {}
        # Não usamos mais a grade fixa; os plots serão gerenciados dinamicamente
        
        # Definir `highlighted_positions` antes de carregar a configuração
        self.highlighted_positions = set()
        
        # Definir `selected_sensors`
        self.selected_sensors = []  # Lista para mapear sensores selecionados
        
        # Conectar o sinal de seleção de sensores
        self.sensor_selection.selections_applied.connect(self.setup_graphs)
        
        # Página de Comparação de Voltas
        self.comparison_page = ComparisonView()
        self.tabs.addTab(self.comparison_page, "Comparação de Voltas")

        # Página de Configuração de Setup do Carro
        self.setup_page = SetupView()
        self.tabs.addTab(self.setup_page, "Setup do Carro")
        
        # Página de Monitoramento do Carro
        self.car_monitoring_page = CarMonitoringView()
        self.tabs.addTab(self.car_monitoring_page, "Monitoramento do Carro")
        
        # Load API configuration
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'api_config.json')
        try:
            with open(config_path, 'r') as f:
                self.api_config = json.load(f)
        except FileNotFoundError:
            QMessageBox.warning(self, "Configuration Error", 
                              "API configuration file not found. Using default settings.")
            self.api_config = {
                "api_endpoint": "YOUR_API_ENDPOINT_HERE",
                "update_rate": 0.1,
                "retry_delay": 1.0
            }
        
        # Initialize API service with configuration
        self.api_service = APIService(
            api_url=self.api_config["api_endpoint"],
            update_rate=self.api_config["update_rate"],
            retry_delay=self.api_config["retry_delay"]
        )
        self.api_service.data_generated.connect(self.update_graphs_with_data)
        self.api_service.start()
        
        # Caminho para o arquivo de configuração
        self.config_file = "graph_layout_config.json"
        self.load_grid_configuration()
    
    def setup_grid_graphs(self):
        """
        Inicializa a grade de gráficos. Mantida para possíveis futuras utilizações.
        """
        pass  # Removido devido à configuração automática
    
    def open_grid_config_dialog(self):
        """
        Abre o diálogo para configurar manualmente a grade de gráficos.
        """
        self.clear_highlights()
        dialog = GridConfigDialog(self.graph_widgets, self)
        if dialog.exec():
            config = dialog.get_configuration()
            self.apply_grid_configuration(config)
    
    def apply_grid_configuration(self, config):
        """
        Aplica a configuração da grade conforme selecionado pelo usuário.
        `config` é um dicionário com a posição e span para cada gráfico.
        """
        # Limpar a grade existente
        self.clear_grid_layout()
        
        # Re-adicionar os widgets conforme a configuração
        for sensor_name, pos in config.items():
            plot = self.graph_widgets.get(sensor_name)
            if plot:
                self.graph_grid_layout.addWidget(plot, pos['row'], pos['column'], pos['rowSpan'], pos['colSpan'])
                plot.row = pos['row']
                plot.column = pos['column']
                self.highlight_cells(pos['row'], pos['column'], pos['rowSpan'], pos['colSpan'])
        
        # Salvar a configuração
        self.save_grid_configuration(config)
    
    def highlight_cells(self, row, column, rowSpan, colSpan):
        """
        Destaca as células ocupadas pelos gráficos configurados.
        """
        for i in range(row, row + rowSpan):
            for j in range(column, column + colSpan):
                cell_widget = self.graph_grid_layout.itemAtPosition(i, j).widget()
                if cell_widget:
                    palette = cell_widget.palette()
                    palette.setColor(QPalette.Window, QColor("#444444"))  # Cor de destaque
                    cell_widget.setAutoFillBackground(True)
                    cell_widget.setPalette(palette)
                    cell_widget.update()
                    self.highlighted_positions.add((i, j))
    
    def clear_grid_layout(self):
        """
        Remove todos os widgets da grade e reseta o layout.
        """
        while self.graph_grid_layout.count():
            item = self.graph_grid_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()  # Remover o widget completamente

        # Resetar todas as stretch para evitar comportamento inesperado
        for r in range(self.graph_grid_layout.rowCount()):
            self.graph_grid_layout.setRowStretch(r, 0)
        for c in range(self.graph_grid_layout.columnCount()):
            self.graph_grid_layout.setColumnStretch(c, 0)

        self.graph_grid_layout.update()
    
    def clear_highlights(self):
        """
        Remove o destaque das células.
        """
        for (i, j) in self.highlighted_positions:
            cell_widget = self.graph_grid_layout.itemAtPosition(i, j).widget()
            if cell_widget:
                palette = cell_widget.palette()
                palette.setColor(QPalette.Window, QColor("#2E2E2E") if self.current_theme == "Dark" else QColor("#FFFFFF"))
                cell_widget.setPalette(palette)
                cell_widget.update()
        self.highlighted_positions.clear()
    
    def change_theme(self, theme_name):
        """
        Alterna entre temas escuro e claro.
        """
        if theme_name == "Dark":
            self.apply_theme(DARK_THEME)
            self.current_theme = "Dark"
            print("Tema alterado para Escuro")
        elif theme_name == "Light":
            self.apply_theme(LIGHT_THEME)
            self.current_theme = "Light"
            print("Tema alterado para Claro")
        
        # Atualizar o fundo dos gráficos de acordo com o tema
        for sensor_name, plot in self.graph_widgets.items():
            plot.setBackground('#2E2E2E' if self.current_theme == "Dark" else '#FFFFFF')
        
        # Atualizar os destaques, se houver
        for (i, j) in self.highlighted_positions:
            cell_widget = self.graph_grid_layout.itemAtPosition(i, j).widget()
            if cell_widget:
                palette = cell_widget.palette()
                palette.setColor(QPalette.Window, QColor("#444444"))  # Cor de destaque permanece
                cell_widget.setPalette(palette)
                cell_widget.update()
    
    def apply_theme(self, stylesheet):
        """
        Aplica o stylesheet selecionado à aplicação.
        """
        self.setStyleSheet(stylesheet)
    
    def load_grid_configuration(self):
        """
        Carrega as configurações da grade a partir de um arquivo JSON, se existir.
        """
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            # Converter as chaves de string para sensor names
            self.apply_grid_configuration(config)
    
    def save_grid_configuration(self, config):
        """
        Salva as configurações da grade em um arquivo JSON.
        """
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)
    
    def closeEvent(self, event):
        """
        Garante que as configurações sejam salvas ao fechar a aplicação.
        """
        # Salvar a configuração atual
        config = {}
        for sensor_name, plot in self.graph_widgets.items():
            # Determine the position and spans of each plot
            pos = self.graph_grid_layout.getItemPosition(self.graph_grid_layout.indexOf(plot))
            config[sensor_name] = {
                'row': pos[0],
                'column': pos[1],
                'rowSpan': pos[2],
                'colSpan': pos[3]
            }
        self.save_grid_configuration(config)
        
        # Parar o DataSimulator
        self.api_service.stop()
        
        super().closeEvent(event)
    
    def setup_graphs(self, selected_sensors_list):
        """
        Configura os gráficos com base nos sensores selecionados e arranja a grade automaticamente.
        """
        # Atualizar a lista de sensores selecionados
        self.selected_sensors = selected_sensors_list
        
        # Limpar a grade existente
        self.clear_grid_layout()
        self.clear_highlights()
        
        # Limpar graph_widgets
        self.graph_widgets.clear()
        
        # Determinar o número de sensores
        num_sensors = len(selected_sensors_list)
        
        if num_sensors == 0:
            return
        
        # Calcular o número de linhas e colunas para uma grade quase quadrada
        rows = math.ceil(math.sqrt(num_sensors))
        cols = math.ceil(num_sensors / rows)

        # Ajustar a grade dinamicamente
        for index, sensor in enumerate(selected_sensors_list):
            row = index // cols
            col = index % cols

            # Criar um novo plot widget
            plot = DraggablePlotWidget(
                title=sensor,
                main_window=self,
                parent=self.graph_grid_widget
            )
            plot.data_x = []
            plot.data_y = []
            plot.setObjectName(sensor)  # Usado para drag-and-drop identification
            self.graph_grid_layout.addWidget(plot, row, col, 1, 1)
            self.graph_widgets[sensor] = plot

        # Ajustar a stretch para ocupar todo o espaço disponível
        self.adjust_grid_stretch(rows, cols)

        # Atualizar layout
        self.graph_grid_widget.update()

        # Exibir uma mensagem de confirmação (opcional)
        QMessageBox.information(self, "Configuração Atualizada", "A grade de gráficos foi atualizada com sucesso!")
    
    def adjust_grid_stretch(self, rows, cols):
        """
        Ajusta a stretch das linhas e colunas para ocupar todo o espaço disponível.
        """
        # Resetar todas as stretch
        for r in range(self.graph_grid_layout.rowCount()):
            self.graph_grid_layout.setRowStretch(r, 0)
        for c in range(self.graph_grid_layout.columnCount()):
            self.graph_grid_layout.setColumnStretch(c, 0)

        # Configurar stretch para as linhas e colunas usadas
        for r in range(rows):
            self.graph_grid_layout.setRowStretch(r, 1)
        for c in range(cols):
            self.graph_grid_layout.setColumnStretch(c, 1)
    
    def swap_plots(self, source_sensor, target_sensor):
        """
        Troca os gráficos entre dois sensores.
        """
        plot_source = self.graph_widgets.get(source_sensor)
        plot_target = self.graph_widgets.get(target_sensor)
        
        if plot_source and plot_target:
            # Obter as posições atuais dos plots
            pos_source = self.graph_grid_layout.getItemPosition(self.graph_grid_layout.indexOf(plot_source))
            pos_target = self.graph_grid_layout.getItemPosition(self.graph_grid_layout.indexOf(plot_target))
            
            # Trocar os plots na grade
            self.graph_grid_layout.addWidget(plot_target, pos_source[0], pos_source[1], pos_source[2], pos_source[3])
            self.graph_grid_layout.addWidget(plot_source, pos_target[0], pos_target[1], pos_target[2], pos_target[3])
            
            # Atualizar as entradas no graph_widgets
            self.graph_widgets[source_sensor], self.graph_widgets[target_sensor] = plot_target, plot_source
            
            print(f"Troca realizada: Gráfico '{source_sensor}' ↔ Gráfico '{target_sensor}'")
    
    def update_graphs_with_data(self, sensor_data):
        """
        Atualiza os gráficos com os dados recebidos.
        """
        current_time = time.time()  # Marca de tempo para eixo X
        for sensor in self.selected_sensors:
            if sensor in sensor_data:
                value = sensor_data[sensor]
                plot = self.graph_widgets.get(sensor)
                if plot:
                    # Adiciona os dados ao gráfico
                    plot.add_data_point(current_time, value)



