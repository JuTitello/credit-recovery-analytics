from datetime import timedelta
import random

FORMA_PGTO = ["Pix", "Boleto", "Cartão de Crédito", "Transferência Bancária"]


def dividir_em_centavos(valor_divida, numero_partes):

    valor_centavos = round(valor_divida * 100)
    parte_centavos = valor_centavos // numero_partes
    resto_centavos = valor_centavos - (parte_centavos * numero_partes)
    #Foi necessário a conversão de centavos para não gerar problemas como neste exemplo: 100/3 = 33,33 (33,33*3 = 99,99 ao invés de 100)

    partes = [parte_centavos] * numero_partes
    partes[-1] += resto_centavos  # A última parte absorve o resto
 
    return [p / 100 for p in partes]  # Devolve já convertido de volta pra reais

def gerar_quitado(contrato_id, data_contratacao, valor_divida, numero_parcelas):
    "Contrato Quitado:"
    "\nsoma dos pagamentos = valor_divida."
    "\n~60% paga no prazo combinado (numero_parcelas)"
    "\n~40% antecipa (menos parcelas que o combinado)"

    pagamentos = []

    if random.random() < 0.6:
        parcelas_pagas = numero_parcelas

    else:
        parcelas_pagas = random.randint(1, numero_parcelas)

    valores = dividir_em_centavos(valor_divida, parcelas_pagas)


    for i, valor_parcela in enumerate(valores):

        data_pagamento = data_contratacao + timedelta(days=30 * (i + 1))
        forma_pagamento = random.choice(FORMA_PGTO)
        pagamentos.append((contrato_id, data_pagamento, valor_parcela, forma_pagamento))
        
    return pagamentos


def gerar_parcial(contrato_id, data_contratacao, valor_divida, data_carga):
    "Contrato Em Aberto ou Renegociado:"
    "\npagamentos parciais, somando entre 10% e 70% de valor_divida."
    "\nAs datas podem passar de data_vencimento (é o que caracteriza a inadimplência)."

    pagamentos = []

    percentual_pago = random.uniform(0.10, 0.70)
    valor_pago_total = round(valor_divida * percentual_pago, 2)

    numero_pagamentos = random.randint(1, 4)
    valores = dividir_em_centavos(valor_pago_total, numero_pagamentos)

     # janela de datas possíveis: entre a contratação e a data_carga (Inseridos)
    dias_disponiveis = max((data_carga - data_contratacao). days, 1)

    for valor_parcela in valores:
        dias_aleatórios = random.randint(1, dias_disponiveis)
        data_pagamento = data_contratacao + timedelta(days=dias_aleatórios)
        forma_pagamento = random.choice(FORMA_PGTO)
        pagamentos.append((contrato_id, data_pagamento, valor_parcela, forma_pagamento))

    return pagamentos

def gerar_cancelado(contrato_id, data_contratacao, valor_divida):
    "Contrato Cancelado:"
    "\n~85% não teve nenhum pagamento"
    "\n~15% teve 1 pagamento parcial pequeno (não reembolsado) antes do cancelamento."

    if random.random() >= 0.15:
        return []

    valor_parcial = round(valor_divida * random.uniform(0.05, 0.30), 2)
    dias_ate_pagamento = random.randint(1, 30)
    data_pagamento = data_contratacao + timedelta(days=dias_ate_pagamento)
    forma_pagamento = random.choice(FORMA_PGTO)

    return[(contrato_id, data_pagamento, valor_parcial, forma_pagamento)]

def gerar_pagamentos(contratos, data_carga):

    pagamentos = []

    for (contrato_id, data_contratacao, valor_divida, status_contrato, numero_parcelas) in contratos:

        valor_divida = float(valor_divida)

        if status_contrato == "Quitado":
            pagamentos += gerar_quitado( contrato_id, data_contratacao, valor_divida, numero_parcelas)

        elif status_contrato in ("Em Aberto", "Renegociado"):
            pagamentos += gerar_parcial(contrato_id, data_contratacao, valor_divida, data_carga)

        elif status_contrato == "Cancelado":
            pagamentos += gerar_cancelado(contrato_id, data_contratacao, valor_divida)

    return pagamentos

def inserir_pagamentos(cursor, pagamentos):
    "> Insere os pagamentos em lote na tabela pagamentos."

    query = "INSERT INTO pagamentos (contrato_id, data_pagamento, valor_pagamento, forma_pagamento) VALUES (%s, %s, %s, %s);"

    cursor.executemany(query, pagamentos)