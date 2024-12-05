from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5.QtCore import Qt


class MonthTab(QWidget):
    def __init__(self, year, month, dias, saldo_anterior):
        super().__init__()
        self.year = year
        self.month = month

        # Tabela
        self.tabela = QTableWidget()
        self.tabela.setRowCount(len(dias))
        self.tabela.setColumnCount(5)
        self.tabela.setHorizontalHeaderLabels(
            ["Data", "Dia da Semana", "Entrada", "Saída", "Saldo"])
        self.populate_table(dias, saldo_anterior)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.tabela)
        self.setLayout(layout)

        # Eventos
        self.setup_events()

    def populate_table(self, dias, saldo_anterior):
        for i, (data, dia_semana) in enumerate(dias):
            # Coluna de Data
            self.tabela.setItem(i, 0, QTableWidgetItem(data))
            self.tabela.item(i, 0).setFlags(
                Qt.ItemIsSelectable | Qt.ItemIsEnabled)

            # Coluna de Dia da Semana
            self.tabela.setItem(i, 1, QTableWidgetItem(dia_semana))
            self.tabela.item(i, 1).setFlags(
                Qt.ItemIsSelectable | Qt.ItemIsEnabled)

            # Colunas de Entrada e Saída (Editáveis)
            self.tabela.setItem(i, 2, QTableWidgetItem(""))  # Entrada
            self.tabela.setItem(i, 3, QTableWidgetItem(""))  # Saída

            # Coluna de Saldo
            if i == 0:
                saldo = saldo_anterior
            else:
                saldo = 0
            self.tabela.setItem(i, 4, QTableWidgetItem(f"{saldo:.2f}"))
            self.tabela.item(i, 4).setFlags(
                Qt.ItemIsSelectable | Qt.ItemIsEnabled)

    def setup_events(self):
        # Conecta os eventos de edição de entrada e saída
        self.tabela.itemChanged.connect(self.update_saldo)

    def update_saldo(self, item):
        if item.column() not in [2, 3]:  # Apenas para Entrada ou Saída
            return

        for i in range(self.tabela.rowCount()):
            try:
                entrada = float(self.tabela.item(i, 2).text()) if self.tabela.item(
                    i, 2) and self.tabela.item(i, 2).text() else 0
                saida = float(self.tabela.item(i, 3).text()) if self.tabela.item(
                    i, 3) and self.tabela.item(i, 3).text() else 0
                saldo_anterior = float(self.tabela.item(
                    i - 1, 4).text()) if i > 0 else float(self.tabela.item(0, 4).text())
                saldo_atual = saldo_anterior + entrada - saida
                self.tabela.item(i, 4).setText(f"{saldo_atual:.2f}")
            except ValueError:
                self.tabela.item(i, 4).setText("Erro")

    def get_final_balance(self):
        """Retorna o saldo final do mês."""
        last_row = self.tabela.rowCount() - 1
        return float(self.tabela.item(last_row, 4).text()) if self.tabela.item(last_row, 4) else 0
