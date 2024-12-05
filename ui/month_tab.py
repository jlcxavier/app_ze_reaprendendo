from utils.database import JSONDatabase
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QComboBox, QDateEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtWidgets import (
    QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QDialog,
    QLabel, QLineEdit, QComboBox, QDateEdit, QHBoxLayout
)
from PyQt5.QtCore import Qt, QDate


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
            ["Data", "Dia da Semana", "Entrada", "Saida", "Saldo"])
        self.populate_table(dias, saldo_anterior)

        # Botão para adicionar entrada/Saida
        self.add_button = QPushButton("+")
        self.add_button.clicked.connect(self.open_form)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.tabela)
        layout.addWidget(self.add_button)
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

            # Colunas de Entrada e Saida (Editáveis)
            self.tabela.setItem(i, 2, QTableWidgetItem(""))  # Entrada
            self.tabela.setItem(i, 3, QTableWidgetItem(""))  # Saida

            # Coluna de Saldo
            if i == 0:
                saldo = saldo_anterior
            else:
                saldo = 0
            self.tabela.setItem(i, 4, QTableWidgetItem(f"{saldo:.2f}"))
            self.tabela.item(i, 4).setFlags(
                Qt.ItemIsSelectable | Qt.ItemIsEnabled)

    def setup_events(self):
        # Conecta os eventos de edição de entrada e Saida
        self.tabela.itemChanged.connect(self.update_saldo)

    def update_saldo(self, item):
        if item.column() not in [2, 3]:  # Apenas para Entrada ou Saida
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

    def open_form(self):
        """
        Abre um formulário para adicionar uma nova entrada ou Saida.
        """
        dialog = EntryForm(self)
        dialog.exec_()


class EntryForm(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Cadastrar Entrada/Saida")
        self.setFixedSize(600, 400)
        self.db = JSONDatabase()  # Usa JSON como armazenamento

        # Widgets do formulário
        self.description_label = QLabel("Descrição:")
        self.description_input = QLineEdit()

        self.value_label = QLabel("Valor:")
        self.value_input = QLineEdit()

        self.type_label = QLabel("Tipo:")
        self.type_dropdown = QComboBox()
        self.type_dropdown.addItems(["Entrada", "Saida"])

        self.date_label = QLabel("Data:")
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)

        # Botão para cadastrar
        self.submit_button = QPushButton("Cadastrar")
        self.submit_button.clicked.connect(self.submit_form)

        # Layout
        form_layout = QVBoxLayout()
        form_layout.addWidget(self.description_label)
        form_layout.addWidget(self.description_input)
        form_layout.addWidget(self.value_label)
        form_layout.addWidget(self.value_input)
        form_layout.addWidget(self.type_label)
        form_layout.addWidget(self.type_dropdown)
        form_layout.addWidget(self.date_label)
        form_layout.addWidget(self.date_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.submit_button)

        form_layout.addLayout(button_layout)
        self.setLayout(form_layout)

    def submit_form(self):
        """
        Processa o formulário, adiciona os valores ao JSON e à tabela.
        """
        descricao = self.description_input.text()
        valor = self.value_input.text()
        tipo = self.type_dropdown.currentText()
        data = self.date_input.date().toString("dd/MM/yyyy")

        # Validação: o valor deve ser numérico
        if not valor.replace('.', '', 1).isdigit():
            QMessageBox.critical(self, "Erro", "O valor deve ser numérico.")
            return

        valor = float(valor)

        # Salva a transação no JSON
        self.db.insert_transaction(data, tipo, descricao, valor)

        # Adiciona a transação na tabela
        for i in range(self.parent.tabela.rowCount()):
            if self.parent.tabela.item(i, 0).text() == data:
                col = 2 if tipo == "Entrada" else 3
                self.parent.tabela.item(i, col).setText(f"{valor:.2f}")
                self.parent.update_saldo(self.parent.tabela.item(i, col))
                break

        self.accept()
