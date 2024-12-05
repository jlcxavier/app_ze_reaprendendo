from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QPushButton
from ui.month_tab import MonthTab
from utils.data import get_days_of_month, get_month_name


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciador de Meses")
        self.resize(800, 600)

        # Widget de abas
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)  # Permite fechar abas
        self.tabs.tabCloseRequested.connect(self.close_tab)

        # Botão para adicionar novas abas
        self.add_tab_button = QPushButton("Adicionar Mês")
        self.add_tab_button.clicked.connect(self.add_new_tab)

        # Layout principal
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tabs)
        self.layout.addWidget(self.add_tab_button)

        self.setLayout(self.layout)

        # Variável para armazenar o saldo final do mês anterior
        self.saldo_anterior = 0

        # Adicionar aba inicial (Dezembro)
        self.add_new_tab(2024, 12)

    def add_new_tab(self, ano=None, mes=None):
        """
        Adiciona uma nova aba com a tabela do mês e ano fornecidos.
        Se nenhum mês/ano for fornecido, exibe o próximo mês a partir da aba atual.
        """
        if ano is None or mes is None:
            # Determina o próximo mês/ano com base na última aba
            current_tab_index = self.tabs.count() - 1
            last_tab = self.tabs.widget(current_tab_index)
            last_month = last_tab.month
            last_year = last_tab.year

            # Incrementa o mês e ajusta o ano, se necessário
            if last_month == 12:
                mes = 1
                ano = last_year + 1
            else:
                mes = last_month + 1
                ano = last_year
        else:
            mes = mes
            ano = ano

        # Gera a tabela para o mês/ano
        dias = get_days_of_month(ano, mes)
        tab = MonthTab(ano, mes, dias, self.saldo_anterior)
        self.tabs.addTab(tab, f"{get_month_name(mes)} {ano}")

        # Atualiza o saldo anterior com o saldo final do mês atual
        self.saldo_anterior = tab.get_final_balance()

    def close_tab(self, index):
        """
        Fecha a aba solicitada e ajusta o saldo anterior se a aba fechada for a última.
        """
        if index == self.tabs.count() - 1:
            # Se a aba fechada for a última, redefine o saldo anterior
            if self.tabs.count() > 1:
                last_tab = self.tabs.widget(self.tabs.count() - 2)
                self.saldo_anterior = last_tab.get_final_balance()
            else:
                self.saldo_anterior = 0
        self.tabs.removeTab(index)
