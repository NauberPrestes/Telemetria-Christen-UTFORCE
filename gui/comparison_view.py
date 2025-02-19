# gui/comparison_view.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy,
    QGroupBox, QColorDialog, QMessageBox, QGridLayout, QCheckBox
)
from PySide6.QtCore import Qt
from pyqtgraph import PlotWidget, mkPen
import pyqtgraph as pg
import random

from gui.sensor_selection import SensorSelectionWidget
from gui.flow_layout import FlowLayout



class FullscreenPlotWindow(QWidget):
    def __init__(self, curves, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Comparação de Voltas - Tela Cheia")
        self.setWindowFlags(self.windowFlags() | Qt.Window)
        self.showFullScreen()

        # Layout principal
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # PlotWidget para tela cheia
        self.plot_widget = PlotWidget(title="Comparação de Voltas - Tela Cheia")
        self.plot_widget.setBackground('#2E2E2E')  # Cinza escuro para o fundo do gráfico
        self.plot_widget.setLabel('left', 'Valor')
        self.plot_widget.setLabel('bottom', 'Tempo (s)')
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self.plot_widget.setMouseEnabled(x=True, y=True)

        main_layout.addWidget(self.plot_widget, stretch=5)

        # Botão para sair da tela cheia
        exit_fullscreen_button = QPushButton("Sair da Tela Cheia")
        exit_fullscreen_button.setFixedWidth(150)
        exit_fullscreen_button.clicked.connect(self.close)
        main_layout.addWidget(exit_fullscreen_button, alignment=Qt.AlignRight)

        # Caixa de legenda compacta com FlowLayout
        self.legend_box = QGroupBox("Legenda das Linhas")
        self.legend_layout = FlowLayout()
        self.legend_box.setLayout(self.legend_layout)
        self.legend_box.setStyleSheet("font-size: 10px;")
        main_layout.addWidget(self.legend_box, stretch=1)

        # Box separada para mostrar o valor sob o mouse (REMOVIDA)
        # self.mouse_value_box = QGroupBox("Valor Sob o Mouse")
        # self.mouse_value_layout = QVBoxLayout()
        # self.mouse_value_box.setLayout(self.mouse_value_layout)
        # self.mouse_value_label = QLabel("Valor: N/A")
        # self.mouse_value_label.setStyleSheet("font-weight: bold; color: white;")
        # self.mouse_value_layout.addWidget(self.mouse_value_label)
        # main_layout.addWidget(self.mouse_value_box, stretch=1)

        # Adicionando linha vertical para tooltips
        self.vLine = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('w', width=1))  # Linha branca
        self.plot_widget.addItem(self.vLine, ignoreBounds=True)

        # Mapeamento de curvas para legendas
        self.legend_labels = {}  # {(lap, sensor): QLabel}

        # Plotar as curvas no PlotWidget de tela cheia
        self.curves = {}
        for (lap, sensor), curve in curves.items():
            time_data = curve.x_data
            value_data = curve.y_data
            color = curve.opts['pen'].color()
            pen = mkPen(color=color, width=2)
            new_curve = self.plot_widget.plot(
                time_data, value_data, pen=pen, 
                name=f"{lap} - {sensor.replace('_', ' ').title()}",
                symbol='o', symbolSize=5, symbolBrush=color
            )
            # Anexar os dados diretamente à curva para facilitar o acesso
            new_curve.x_data = time_data
            new_curve.y_data = value_data
            self.curves[(lap, sensor)] = new_curve

            # Adicionar legenda compacta
            label = QLabel(f"{lap} - {sensor.replace('_', ' ').title()} - Tempo: N/A - Valor: N/A")
            label.setStyleSheet("font-size: 10px; font-weight: bold; color: white;")
            self.legend_layout.addWidget(label)
            self.legend_labels[(lap, sensor)] = label

        # Depuração: Verificar quantas curvas foram plotadas
        print(f"FullscreenPlotWindow: {len(self.curves)} curvas plotadas.")

        # Conectar o sinal de movimento do mouse
        self.plot_widget.scene().sigMouseMoved.connect(self.on_mouse_moved)

    def get_y_at_x(self, curve, x):
        """
        Retorna o valor y correspondente ao ponto x na curva, interpolando se necessário.
        """
        x_data = curve.x_data
        y_data = curve.y_data
        if x < x_data[0] or x > x_data[-1]:
            return None  # Fora do intervalo de dados

        # Encontrar o índice i tal que x_data[i] <= x <= x_data[i+1]
        for i in range(len(x_data) - 1):
            if x_data[i] <= x <= x_data[i + 1]:
                x0, y0 = x_data[i], y_data[i]
                x1, y1 = x_data[i + 1], y_data[i + 1]
                if x1 - x0 == 0:
                    return y0  # Evitar divisão por zero
                # Interpolação linear
                return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        return None

    def on_mouse_moved(self, pos):
        """
        Atualiza as legendas com os valores correspondentes ao ponto x atual do mouse na janela de tela cheia.
        """
        if self.plot_widget.sceneBoundingRect().contains(pos):
            mouse_point = self.plot_widget.plotItem.vb.mapSceneToView(pos)
            x = mouse_point.x()

            # Mover a linha vertical para a posição x atual
            self.vLine.setPos(x)

            # Iterar sobre todas as curvas para atualizar as legendas
            for (lap, sensor), curve in self.curves.items():
                y = self.get_y_at_x(curve, x)
                if y is not None:
                    self.legend_labels[(lap, sensor)].setText(f"{lap} - {sensor.replace('_', ' ').title()} - Tempo: {x:.3f} - Valor: {y:.2f}")
                else:
                    self.legend_labels[(lap, sensor)].setText(f"{lap} - {sensor.replace('_', ' ').title()} - Tempo: N/A - Valor: N/A")
        else:
            # Resetar a linha vertical e todas as legendas
            self.vLine.setPos(None)
            for (lap, sensor), label in self.legend_labels.items():
                label.setText(f"{lap} - {sensor.replace('_', ' ').title()} - Tempo: N/A - Valor: N/A")

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy,
    QGroupBox, QColorDialog, QMessageBox, QGridLayout, QCheckBox
)
from PySide6.QtCore import Qt
from pyqtgraph import PlotWidget, mkPen
import pyqtgraph as pg
import random

from gui.sensor_selection import SensorSelectionWidget
from gui.flow_layout import FlowLayout


class ComparisonView(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # Layout para seleção de sensores (esquerda)
        self.sensor_selection = SensorSelectionWidget()
        self.sensor_selection.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        main_layout.addWidget(self.sensor_selection, stretch=1)

        # Layout para seleção de voltas e gráfico (direita)
        right_layout = QVBoxLayout()
        main_layout.addLayout(right_layout, stretch=4)

        # Seção de seleção de voltas
        selection_layout = QVBoxLayout()
        selection_label = QLabel("Selecione as Voltas para Comparar:")
        selection_layout.addWidget(selection_label)

        self.lap_checkboxes = {}  # Armazenar as caixas de seleção para cada volta
        lap_selection_box = QWidget()
        lap_selection_layout = QGridLayout()  # Usaremos um QGridLayout para organizar as voltas lado a lado
        lap_selection_box.setLayout(lap_selection_layout)

        # Adicionar voltas simuladas com caixas de seleção
        max_columns = 10  # Defina quantas colunas por linha você deseja
        for i in range(1, 21):  # Simulação de 20 voltas
            checkbox = QCheckBox(f"{i}")
            row = (i - 1) // max_columns
            col = (i - 1) % max_columns
            lap_selection_layout.addWidget(checkbox, row, col)
            self.lap_checkboxes[f"Volta {i}"] = checkbox

        # Adicionar ao layout principal
        selection_layout.addWidget(lap_selection_box)
        right_layout.addLayout(selection_layout)

        # Botão para comparar
        self.compare_button = QPushButton("Comparar Voltas")
        right_layout.addWidget(self.compare_button)
        self.compare_button.clicked.connect(self.compare_laps)

        # Área de gráficos
        self.plot_widget = PlotWidget(title="Comparação de Voltas")
        right_layout.addWidget(self.plot_widget, stretch=5)  # Aumentar a proporção do gráfico
        self.plot_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Botão para tela cheia
        self.fullscreen_button = QPushButton("Tela Cheia")
        self.fullscreen_button.setFixedWidth(100)
        right_layout.addWidget(self.fullscreen_button)
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)

        # Habilitar interação para tooltips
        self.plot_widget.setMouseEnabled(x=True, y=True)
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)  # Grade mais sutil
        self.plot_widget.setBackground('#2E2E2E')  # Cinza escuro para o fundo do gráfico
        self.plot_widget.setLabel('left', 'Valor')
        self.plot_widget.setLabel('bottom', 'Tempo (s)')

        # Box separada para legendas das linhas com FlowLayout
        self.legend_box = QGroupBox("Legenda das Linhas")
        self.legend_layout = FlowLayout()
        self.legend_box.setLayout(self.legend_layout)
        right_layout.addWidget(self.legend_box)
        self.legend_labels = {}   # Para armazenar QLabel das legendas
        self.color_buttons = {}    # Para armazenar os botões de cor

        # Inicialização de dados
        self.lap_data = {}
        self.curves = {}
        self.selected_sensors = []
        self.selected_laps = []

        # Habilitar tooltips
        self.plot_widget.scene().sigMouseMoved.connect(self.on_mouse_moved)
        self.vLine = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('w', width=1))  # Linha branca
        self.plot_widget.addItem(self.vLine, ignoreBounds=True)

        # Conectar o sinal de seleção de sensores
        self.sensor_selection.selections_applied.connect(self.update_selected_sensors)

        # Estado de tela cheia
        self.is_fullscreen = False
        self.fullscreen_window = None

    # Os métodos compare_laps e outros permanecem iguais


    def get_y_at_x(self, curve, x):
        """
        Retorna o valor y correspondente ao ponto x na curva, interpolando se necessário.
        """
        x_data = curve.x_data
        y_data = curve.y_data
        if x < x_data[0] or x > x_data[-1]:
            return None  # Fora do intervalo de dados

        # Encontrar o índice i tal que x_data[i] <= x <= x_data[i+1]
        for i in range(len(x_data) - 1):
            if x_data[i] <= x <= x_data[i + 1]:
                x0, y0 = x_data[i], y_data[i]
                x1, y1 = x_data[i + 1], y_data[i + 1]
                if x1 - x0 == 0:
                    return y0  # Evitar divisão por zero
                # Interpolação linear
                return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        return None

    def on_mouse_moved(self, pos):
        """
        Atualiza as legendas com os valores correspondentes ao ponto x atual do mouse.
        """
        if self.plot_widget.sceneBoundingRect().contains(pos):
            mouse_point = self.plot_widget.plotItem.vb.mapSceneToView(pos)
            x = mouse_point.x()

            # Mover a linha vertical para a posição x atual
            self.vLine.setPos(x)

            # Iterar sobre todas as curvas para atualizar as legendas
            for (lap, sensor), curve in self.curves.items():
                y = self.get_y_at_x(curve, x)
                if y is not None:
                    self.legend_labels[(lap, sensor)].setText(f"{lap} - {sensor.replace('_', ' ').title()} - Tempo: {x:.3f} - Valor: {y:.2f}")
                else:
                    self.legend_labels[(lap, sensor)].setText(f"{lap} - {sensor.replace('_', ' ').title()} - Tempo: N/A - Valor: N/A")
        else:
            # Resetar a linha vertical e todas as legendas
            self.vLine.setPos(None)
            for (lap, sensor), label in self.legend_labels.items():
                label.setText(f"{lap} - {sensor.replace('_', ' ').title()} - Tempo: N/A - Valor: N/A")

    def update_selected_sensors(self, selected_sensors):
        """
        Atualiza a lista de sensores selecionados.
        """
        self.selected_sensors = selected_sensors
        print("Sensores Selecionados na Comparação:", self.selected_sensors)

    def compare_laps(self):
        """
        Compara as voltas selecionadas com os sensores escolhidos.
        """
        # Coletar voltas selecionadas
        self.selected_laps = [lap for lap, checkbox in self.lap_checkboxes.items() if checkbox.isChecked()]
        print("Voltas Selecionadas para Comparar:", self.selected_laps)

        if not self.selected_sensors:
            print("Nenhum sensor selecionado para comparação.")
            QMessageBox.warning(self, "Nenhum Sensor Selecionado", "Por favor, selecione pelo menos um sensor para comparar.")
            return

        if not self.selected_laps:
            print("Nenhuma volta selecionada para comparação.")
            QMessageBox.warning(self, "Nenhuma Volta Selecionada", "Por favor, selecione pelo menos uma volta para comparar.")
            return

        # Limpar gráficos anteriores
        self.plot_widget.clear()
        self.curves = {}
        print("Gráficos anteriores limpos.")

        # Readicionar a linha vertical e tooltips
        self.plot_widget.addItem(self.vLine, ignoreBounds=True)
        print("Linha vertical adicionada novamente.")

        # Limpar legend_box
        for i in reversed(range(self.legend_layout.count())):
            widget_to_remove = self.legend_layout.itemAt(i).widget()
            self.legend_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)
        self.legend_labels.clear()
        self.color_buttons.clear()

        # Plotar dados simulados para cada volta e sensor selecionados
        for lap in self.selected_laps:
            for sensor in self.selected_sensors:
                if (lap, sensor) not in self.lap_data:
                    # Simular dados para a volta e sensor
                    time_data = list(range(60))
                    value_data = [random.uniform(150, 200) for _ in time_data]
                    self.lap_data[(lap, sensor)] = (time_data, value_data)
                    print(f"Simulando dados para {lap} - {sensor}")

                time_data, value_data = self.lap_data[(lap, sensor)]
                # Gerar uma cor única para cada curva baseada no hash do sensor e volta
                color = pg.intColor(abs(hash(lap + sensor)) % 256)
                pen = mkPen(color=color, width=2)
                curve = self.plot_widget.plot(
                    time_data, value_data, pen=pen,
                    name=f"{lap} - {sensor.replace('_', ' ').title()}",
                    symbol='o', symbolSize=5, symbolBrush=color
                )
                # Anexar os dados diretamente à curva para facilitar o acesso
                curve.x_data = time_data
                curve.y_data = value_data
                self.curves[(lap, sensor)] = curve
                print(f"Plotando {lap} - {sensor}")

                # Adicionar legenda e botão de cor
                self.add_legend_entry(lap, sensor, curve)


    def add_legend_entry(self, lap, sensor, curve):
        """
        Adiciona uma entrada de legenda e botão de cor para a combinação de volta e sensor.
        """
        # Adicionar QLabel correspondente na legend_box
        label = QLabel(f"{lap} - {sensor.replace('_', ' ').title()} - Tempo: N/A - Valor: N/A")
        label.setStyleSheet("font-size: 10px; font-weight: bold; color: white;")
        self.legend_layout.addWidget(label)
        self.legend_labels[(lap, sensor)] = label

        # Adicionar botão de seleção de cor
        color_button = QPushButton("🔴")
        color_button.setFixedWidth(30)
        color_button.setStyleSheet(f"background-color: {curve.opts['pen'].color().name()}; border: none;")
        # Conectar com lambda que captura o sensor_tuple corretamente
        color_button.clicked.connect(lambda checked, s=(lap, sensor): self.change_line_color(s))
        self.legend_layout.addWidget(color_button)
        self.color_buttons[(lap, sensor)] = color_button

        # Ajustar a altura da legenda para ser menor
        #self.legend_box.setMaximumHeight(150)  # Ajuste conforme necessário


    def change_line_color(self, sensor_tuple):
        """
        Abre um diálogo para selecionar a cor da linha do sensor especificado.
        """
        color = QColorDialog.getColor()
        if color.isValid():
            color_hex = color.name()
            print(f"Cor selecionada para {sensor_tuple}: {color_hex}")
            # Atualizar a cor no gráfico
            curve = self.curves[sensor_tuple]
            curve.setPen(mkPen(color=color_hex, width=2))
            curve.setSymbolBrush(pg.mkBrush(color_hex))
            # Atualizar a cor do botão
            self.color_buttons[sensor_tuple].setStyleSheet(f"background-color: {color_hex}; border: none;")

    def toggle_fullscreen(self):
        """
        Alterna entre o modo normal e o modo de tela cheia para o gráfico de comparação.
        """
        if not self.is_fullscreen:
            # Criar e mostrar a janela de tela cheia
            self.fullscreen_window = FullscreenPlotWindow(self.curves, self)
            self.fullscreen_window.show()
            self.is_fullscreen = True
            print("Janela de tela cheia aberta.")
        else:
            # Fechar a janela de tela cheia
            if self.fullscreen_window:
                self.fullscreen_window.close()
                self.fullscreen_window = None
                print("Janela de tela cheia fechada.")
            self.is_fullscreen = False
