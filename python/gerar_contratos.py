from datetime import datetime, timedelta
import random

STATUS = ["Em Aberto", "Quitado", "Renegociado", "Cancelado"]

data_inicio = datetime(2023, 1, 1)
data_fim = datetime(2026, 9, 30)

def gerar_contratos(n, clientes_ids, assessorias_ids):

    contratos = []

    diferenca_dias = (data_fim - data_inicio).days

    for _ in range(n):
        
        dias_aleatorios = random.randint(0,diferenca_dias)
        
        cliente_id = random.choice(clientes_ids)
        assessoria_id = random.choice(assessorias_ids)
        data_contratacao = (data_inicio + timedelta(days=dias_aleatorios)).date()
        numero_parcelas = random.randint(1, 24)
        data_vencimento = data_contratacao + timedelta(days=30 * numero_parcelas)
        valor_divida = round(random.uniform(500, 80000),2)
        status_contrato = random.choice(STATUS)
        contratos.append((cliente_id, assessoria_id, data_contratacao, numero_parcelas, data_vencimento, valor_divida, status_contrato))

    return contratos

def inserir_contratos(cursor, contratos):
    "> Insere os contratos em lote na tabela contratos."

    query = "INSERT INTO contratos (cliente_id, assessoria_id, data_contratacao, numero_parcelas, data_vencimento, valor_divida, status_contrato) VALUES (%s, %s, %s, %s, %s, %s, %s);"

    cursor.executemany(query, contratos)