import json
import os


class JSONDatabase:
    def __init__(self, file_name="finance_app.json"):
        # Caminho completo do arquivo JSON
        app_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(app_dir, file_name)

        # Cria o arquivo JSON vazio, se ele não existir
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as file:
                json.dump([], file)

    def insert_transaction(self, data, tipo, descricao, valor):
        """
        Insere uma nova transação no arquivo JSON.
        """
        # Carrega transações existentes
        transactions = self.get_transactions()

        # Adiciona a nova transação
        transactions.append({
            "data": data,
            "tipo": tipo,
            "descricao": descricao,
            "valor": valor
        })

        # Salva de volta no arquivo JSON
        with open(self.file_path, "w") as file:
            json.dump(transactions, file, indent=4)

    def get_transactions(self):
        """
        Retorna todas as transações armazenadas no arquivo JSON.
        """
        # Lê as transações do arquivo JSON
        with open(self.file_path, "r") as file:
            return json.load(file)
