import random
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem, QMessageBox, QLineEdit, QDialog, QFormLayout, QSpinBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
from pyqtgraph import PlotWidget, mkPen, InfiniteLine,BarGraphItem
from PySide6.QtWidgets import QComboBox, QSizePolicy

import os
import sys

def resource_path(relative_path):
    """ Obtenha o caminho absoluto do recurso, compatível com PyInstaller """
    try:
        # PyInstaller cria um diretório temporário e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class CarMonitoringView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Status do Carro")
        
        # Ajuste de tamanho da janela
        self.setMinimumSize(1235, 737)
        self.setMaximumSize(1920, 1080)        

        # Layout principal
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        # Legenda na lateral esquerda
        self.legend_container = QVBoxLayout()
        self.legend_search = QLineEdit()
        self.legend_search.setPlaceholderText("Pesquisar componentes...")
        self.legend_search.textChanged.connect(self.filter_legend_items)
        self.legend_container.addWidget(self.legend_search)

        self.legend = QListWidget()
        self.legend.setSizeAdjustPolicy(QListWidget.AdjustToContents)
        self.legend_container.addWidget(self.legend)

        # Widget para conter a legenda
        self.legend_widget = QWidget()
        self.legend_widget.setLayout(self.legend_container)
        self.legend_widget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)  # Ajusta ao conteúdo

        self.main_layout.addWidget(self.legend_widget)

        # Container para a imagem do carro
        self.car_image_container = QWidget()
        self.car_image_layout = QVBoxLayout(self.car_image_container)
        self.car_image_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.car_image_container, alignment=Qt.AlignCenter)

        # Carregar a imagem do carro
        self.car_image = QLabel(self.car_image_container)
        image_path = resource_path("assets/images/car_diagram.png")
        self.car_pixmap = QPixmap(image_path)
        if self.car_pixmap.isNull():
            print(f"Erro ao carregar a imagem: {image_path}")
        self.car_image.setPixmap(self.car_pixmap.scaled(800, 600))
        self.car_image.setAlignment(Qt.AlignCenter)
        self.car_image_layout.addWidget(self.car_image)


        # Dados simulados dos componentes
        self.component_data = {
            "Combustion Engine": {"Temperatura": 85},
            "Front Left Tire": {"Pressão": 2.2, "Temperatura": 65},
            "Front Right Tire": {"Pressão": 2.3, "Temperatura": 67},
            "Rear Left Tire": {"Pressão": 2.1, "Temperatura": 63},
            "Rear Right Tire": {"Pressão": 2.2, "Temperatura": 64},
            "Front Brake": {"Temperatura": 450},
            "Rear Brake": {"Temperatura": 420},
            "Eletric Engine": {"Temperatura": 40},
            "Accumulator Box": {"Temperatura": 40},
        }

        # Preferências de gráfico do cliente
        self.graph_preferences = {component: {} for component in self.component_data}

        # Configurações de gráficos padrão
        self.graph_styles = {
            "Pressão": {"type": "bar", "color": "g"},
            "Temperatura": {"type": "line", "color": "r"},
        }

        self.history = {component: [] for component in self.component_data}
        self.thresholds = {
            "Combustion Engine": [85, 100, 105, 110],
            "Front Left Tire": [70, 90, 100],
            "Front Right Tire": [70, 90, 100],
            "Rear Left Tire":[70, 90, 100],
            "Rear Right Tire": [70, 90, 100],
            "Front Brake": [100, 200, 300, 400],
            "Rear Brake": [100, 200, 300, 400],
            "Eletric Engine": [40,60,80,100],
            "Accumulator Box": [40,60,80,100],
        }
        
        # Adicionar bolinhas interativas
        self.add_interactive_balls()

        # Adicionar itens à legenda
        self.add_legend_items()

        # Botão de personalização
        self.settings_button = QPushButton("Configurar Escalas")
        self.settings_button.clicked.connect(self.open_settings_dialog)
        self.legend_container.addWidget(self.settings_button)

        # Adicionar um espaçador
        spacer = QWidget()
        spacer.setFixedHeight(10)  # Espaço entre os botões
        self.legend_container.addWidget(spacer)
        
        # Timer para atualizar os dados em tempo real
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_component_data)
        self.timer.start(500)  # Atualizar a cada 1 segundo
        
        
    def select_graph_type(self, component):
        """
        Exibe uma janela para o cliente selecionar o tipo de gráfico.
        """
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Selecione o Tipo de Gráfico - {component}")
        layout = QFormLayout(dialog)

        combo_boxes = {}
        for key in self.component_data[component]:
            combo_box = QComboBox()
            combo_box.addItems(["Linha", "Barra"])
            current_type = self.graph_preferences[component].get(key, "Linha")
            combo_box.setCurrentText(current_type)
            layout.addRow(f"{key}:", combo_box)
            combo_boxes[key] = combo_box

        def apply_changes():
            for key, combo_box in combo_boxes.items():
                self.graph_preferences[component][key] = combo_box.currentText()
            dialog.accept()

        apply_button = QPushButton("Aplicar")
        apply_button.clicked.connect(apply_changes)
        layout.addWidget(apply_button)

        dialog.exec()

    def add_interactive_balls(self):
        """
        Adiciona bolinhas interativas sobre a imagem do carro.
        """
        self.ball_positions = {
            "Combustion Engine": (200, 300),
            "Front Left Tire": (545, 120),
            "Front Right Tire": (545, 470),
            "Rear Left Tire": (200, 110),
            "Rear Right Tire": (200, 480),
            "Front Brake": (580, 350),
            "Rear Brake": (200, 350),
            "Eletric Engine": (545,300),
            "Accumulator Box": (350,400),
        }

        self.buttons = {}  # Para armazenar os botões dos componentes
        self.labels = {}  # Para armazenar os rótulos ao lado das bolinhas

        for component, position in self.ball_positions.items():
            button = QPushButton(" ", self.car_image_container)
            temperature = self.component_data[component].get("Temperatura", 0)
            button.setStyleSheet(self.get_button_style(temperature, component))  # Escala inicial
            button.setToolTip(component)  # Mostrar o nome do componente ao passar o mouse
            button.setFixedSize(20, 20)
            x, y = position
            button.move(x, y)

            # Adicionar rótulo ao lado da bolinha
            label = QLabel(self.car_image_container)
            label.move(x + 25, y)
            label.setText(self.get_component_values(component, only_values=True))
            label.setStyleSheet("""
            background-color: #666666;  /* Cor de fundo cinza escura */
            color: white;               /* Cor do texto */
            font-size: 12px;            /* Tamanho da fonte */
            font-weight: bold;          /* Texto em negrito */
            border-radius: 5px;         /* Bordas arredondadas */
            padding: 2px;               /* Espaçamento interno */
        """)
            self.labels[component] = label

            # Conectar eventos de clique e hover
            button.clicked.connect(lambda checked, c=component: self.show_graph(c))
            button.enterEvent = lambda event, c=component: self.highlight_legend(c)
            button.leaveEvent = lambda event, c=component: self.unhighlight_legend(c)

            # Adicionar ao dicionário de botões
            self.buttons[component] = button

    def add_legend_items(self):
        """
        Adiciona os itens à legenda, com valores iniciais.
        """
        self.legend_items = {}
        for component, data in self.component_data.items():
            item = QListWidgetItem(f"{component}: {self.get_component_values(component)}")
            self.legend.addItem(item)
            self.legend_items[component] = item
            
        # Certifique-se de que o texto inicial não está destacado
        font = item.font()
        font.setBold(False)
        item.setFont(font)

        # Ajustar a largura da legenda ao conteúdo
        legend_width = self.calculate_legend_width()
        self.legend.setFixedWidth(legend_width)        

    def calculate_legend_width(self):
        """
        Calcula a largura mínima necessária para exibir todo o texto na legenda.
        """
        max_width = 0
        for index in range(self.legend.count()):
            item = self.legend.item(index)
            text_width = self.legend.fontMetrics().horizontalAdvance(item.text())
            max_width = max(max_width, text_width)
        return max_width + 20  # Adicionar uma margem para espaço extra


    def filter_legend_items(self, text):
        """
        Filtra os itens na legenda com base no texto inserido.
        """
        for component, item in self.legend_items.items():
            item.setHidden(text.lower() not in component.lower())

    def open_settings_dialog(self):
        """
        Abre uma janela de diálogo para ajustar os limites de escala dos componentes.
        """
        dialog = QDialog(self)
        dialog.setWindowTitle("Configurar Escalas")
        layout = QFormLayout(dialog)

        spin_boxes = {}
        for component, thresholds in self.thresholds.items():
            spin_boxes[component] = []
            for i, value in enumerate(thresholds):
                spin_box = QSpinBox()
                spin_box.setMinimum(0)
                spin_box.setMaximum(1000)
                spin_box.setValue(value)
                spin_boxes[component].append(spin_box)
                layout.addRow(f"{component} - Limite {i + 1}:", spin_box)

        def apply_changes():
            for component, boxes in spin_boxes.items():
                self.thresholds[component] = [box.value() for box in boxes]
            dialog.accept()

        apply_button = QPushButton("Aplicar")
        apply_button.clicked.connect(apply_changes)
        layout.addWidget(apply_button)

        dialog.exec()

    def update_component_data(self):
        """
        Atualiza os dados simulados em tempo real e reflete na legenda e nas bolinhas.
        """
        for component, data in self.component_data.items():
            for key in data:
                data[key] += random.uniform(-5, 5) if key == "Temperatura" else random.uniform(-0.1, 0.1)
                data[key] = round(max(data[key], 0), 1)
            
            # Atualizar histórico
            self.history[component].append(data.copy())
            if len(self.history[component]) > 10:
                self.history[component].pop(0)

            self.legend_items[component].setText(f"{component}: {self.get_component_values(component)}")
            self.labels[component].setText(self.get_component_values(component, only_values=True))

            if "Temperatura" in data:
                temperature = data["Temperatura"]
                self.buttons[component].setStyleSheet(self.get_button_style(temperature, component))

        # Ajustar a largura da legenda ao conteúdo
        legend_width = self.calculate_legend_width()
        self.legend.setFixedWidth(legend_width)  # Ajusta apenas o widget de lista



    def get_button_style(self, value, component):
        """
        Retorna o estilo da bolinha com base nos valores do componente.
        """
        thresholds = self.thresholds.get(component, [100, 200, 300, 400])
        colors = ["blue", "green", "yellow", "red"]

        color = colors[-1]
        for t, c in zip(thresholds, colors):
            if value <= t:
                color = c
                break

        return f"""
            QPushButton {{
                background-color: {color};
                border-radius: 10px;
                width: 20px;
                height: 20px;
            }}
        """
    def get_component_values(self, component, only_values=False):
        """
        Retorna os valores formatados de um componente.
        """
        data = self.component_data[component]
        if only_values:
            return ", ".join([f"{value}" for value in data.values()])
        return ", ".join([f"{key}: {value}" for key, value in data.items()])

    def show_graph(self, component):
        """
        Exibe o gráfico com os valores do componente, com uma legenda interativa.
        """
        # Permitir que o cliente selecione o tipo de gráfico
        self.select_graph_type(component)

        data = self.history.get(component, [])
        if not data:
            QMessageBox.information(self, "Erro", "Nenhum dado disponível para este componente.")
            return

        # Criar janela do gráfico se não existir
        if not hasattr(self, "graph_window") or not self.graph_window.isVisible():
            self.graph_window = QWidget()
            self.graph_window.setWindowTitle(f"Histórico: {component}")
            self.graph_window.setGeometry(100, 100, 800, 600)

            layout = QVBoxLayout()
            self.graph_window.setLayout(layout)

            self.plot_widget = PlotWidget()
            self.plot_widget.addLegend()  # Adiciona a legenda ao gráfico
            layout.addWidget(self.plot_widget)


            # Adiciona interação para exibir valores ao passar o mouse
            self.vline = InfiniteLine(angle=90, movable=False, pen=mkPen('w', width=1))
            self.hline = InfiniteLine(angle=0, movable=False, pen=mkPen('w', width=1))
            self.plot_widget.addItem(self.vline, ignoreBounds=True)
            self.plot_widget.addItem(self.hline, ignoreBounds=True)
            self.label = QLabel("", self.graph_window)
            layout.addWidget(self.label)

            self.plot_widget.scene().sigMouseMoved.connect(self.update_tooltip)

        # Atualizar o título da janela
        self.graph_window.setWindowTitle(f"Histórico: {component}")

        # Atualizar os dados do gráfico
        self.plot_widget.clear()
        self.plot_items = []   # Rastreamento manual de itens do gráfico
        self.data_curves = []  # Inicializar as curvas para interação
        for key in data[0]:
            y = [d[key] for d in data]
            x = list(range(len(y)))
            graph_type = self.graph_preferences[component].get(key, "Linha")

            if graph_type == "Linha":
                curve = self.plot_widget.plot(x, y, pen=mkPen("r", width=2), name=key)
                self.plot_items.append(curve)
                self.data_curves.append((key, curve))
            elif graph_type == "Barra":
                bar_item = BarGraphItem(x=x, height=y, width=0.5, brush="g")
                self.plot_widget.addItem(bar_item)
                self.plot_items.append(bar_item)
                # Adicionar barras ao conjunto de curvas com None como substituto
                self.data_curves.append((key, None))

        self.graph_window.show()

    def update_tooltip(self, pos):
        """
        Atualiza a tooltip ao passar o mouse sobre o gráfico.
        """
        if self.plot_widget.sceneBoundingRect().contains(pos):
            mouse_point = self.plot_widget.plotItem.vb.mapSceneToView(pos)
            x = int(mouse_point.x())
            y = mouse_point.y()

            self.vline.setPos(x)
            self.hline.setPos(y)

            tooltip_text = []
            for key, curve in self.data_curves:
                if curve is not None:  # Gráfico de linha
                    if 0 <= x < len(curve.yData):  # Verifica se está dentro do intervalo
                        value = curve.yData[x]
                        tooltip_text.append(f"{key}: {value:.2f}")
                else:  # Gráfico de barra
                    bar_data = next((item for item in self.plot_items if isinstance(item, BarGraphItem)), None)
                    if bar_data:
                        bar_x = bar_data.opts["x"]
                        bar_height = bar_data.opts["height"]
                        if x in bar_x:  # Verifica se a posição x corresponde a uma barra
                            index = bar_x.index(x)
                            value = bar_height[index]
                            tooltip_text.append(f"{key}: {value:.2f}")

            self.label.setText(" | ".join(tooltip_text))

    
    def highlight_legend(self, component):
        """
        Destaque visual do item da legenda correspondente ao passar o mouse sobre o botão.
        """
        # Remover destaque de todos os itens
        for item in self.legend_items.values():
            font = item.font()
            font.setBold(False)
            item.setFont(font)

        # Adicionar destaque ao item correspondente
        item = self.legend_items.get(component)
        if item:
            font = item.font()
            font.setBold(True)
            item.setFont(font)

    def unhighlight_legend(self, component):
        """
        Remove o destaque visual do item da legenda quando o mouse sai do botão.
        """
        # Remover destaque do item correspondente
        item = self.legend_items.get(component)
        if item:
            font = item.font()
            font.setBold(False)
            item.setFont(font)