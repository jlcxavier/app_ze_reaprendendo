from utils.database import JSONDatabase

db = JSONDatabase()

# Teste de inserção
db.insert_transaction("05/12/2024", "Entrada", "Teste de Salário", 3000)

# Teste de leitura
transactions = db.get_transactions()
print(transactions)
