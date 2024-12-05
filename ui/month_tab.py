from PyQt5.QtWidgets import (
    QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout,
    QPushButton, QDialog, QLabel, QLineEdit, QComboBox, QDateEdit, QMessageBox
)
from PyQt5.QtCore import Qt, QDate
from utils.database import JSONDatabase


class MonthTab(QWidget):
    def __init__(self, year, month, dias, saldo_anterior):
        super().__init__()
        self.year = year
        self.month = month
        self.db = JSONDatabase()  # Inicializa o banco de dados JSON

        # Inicializa a tabela
        self.tabela = QTableWidget()
        self.tabela.setRowCount(len(dias))
        self.tabela.setColumnCount(5)
        self.tabela.setHorizontalHeaderLabels(
            ["Data", "Dia da Semana", "Entrada", "Saida", "Saldo"])
        self.populate_table(dias, saldo_anterior)

        # Botão para adicionar entradas/saídas
        self.add_button = QPushButton("+")
        self.add_button.clicked.connect(self.open_form)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.tabela)
        layout.addWidget(self.add_button)
        self.setLayout(layout)

        # Carrega as transações do JSON e atualiza a tabela
        self.carregar_transacoes()

    def populate_table(self, dias, saldo_anterior):
        """
        Preenche a tabela com os dias do mês.
        """
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
            self.tabela.setItem(i, 3, QTableWidgetItem(""))  # Saida

            # Coluna de Saldo
            if i == 0:
                saldo = saldo_anterior
            else:
                saldo = 0
            self.tabela.setItem(i, 4, QTableWidgetItem(f"{saldo:.2f}"))
            self.tabela.item(i, 4).setFlags(
                Qt.ItemIsSelectable | Qt.ItemIsEnabled)

    def carregar_transacoes(self):
        """
        Carrega as transações do JSON e exibe na tabela correspondente.
        """
        transacoes = self.db.get_transactions()
        for transacao in transacoes:
            data = transacao["data"]
            tipo = transacao["tipo"]
            descricao = transacao["descricao"]
            valor = transacao["valor"]

            # Procura a linha correspondente à data
            for i in range(self.tabela.rowCount()):
                if self.tabela.item(i, 0).text() == data:
                    col = 2 if tipo == "Entrada" else 3
                    # Atualiza os valores na tabela
                    self.tabela.setItem(
                        i, col, QTableWidgetItem(f"{valor:.2f}"))
                    break

    def open_form(self):
        """
        Abre o formulário para adicionar uma nova entrada/saída.
        """
        dialog = EntryForm(self)
        dialog.exec_()

    def get_final_balance(self):
        """
        Retorna o saldo final do mês com base nos dados da tabela.
        """
        last_row = self.tabela.rowCount() - 1  # Índice da última linha
        # Verifica se há saldo na última linha
        if last_row >= 0 and self.tabela.item(last_row, 4):
            try:
                # Converte o saldo para float
                return float(self.tabela.item(last_row, 4).text())
            except ValueError:
                return 0.0  # Retorna 0.0 se o saldo não for numérico
        return 0.0  # Retorna 0.0 se a tabela estiver vazia


class EntryForm(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Cadastrar Entrada/Saída")
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
        Processa o formulário, adiciona os valores ao JSON e atualiza a tabela.
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

        # Recarrega as transações na tabela
        self.parent.carregar_transacoes()

        # Fecha o formulário após o cadastro
        self.accept()
