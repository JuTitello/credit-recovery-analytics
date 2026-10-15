from datetime import datetime,  timedelta
import random

RESULTADO = {
    "Sucesso" : ["Acordo Fechado", "Boleto 2ªVia Enviado", "Pix Gerado", "Mensagem Entregue"],
    "Insucesso Operacional" : ["Sem Resposta", "Telefone Inexistente"],
    "Recusa" : ["Recusa de Contato", "Recusa de Acordo", "Contestação"],
    "Em Negociação" : ["Sem Previsão", "Cliente Alega Pago", "Promessa de pagamento"]
}

PESOS_STATUS = [20, 45, 15, 20]

CANAL = ["WhatsApp", "SMS", "Telefonia", "E-mail", "Carta"]

CANAL_TELEFONE = ["WhatsApp", "SMS", "Telefonia"]

QTD_INTERACOES = {
        "Em Aberto": (3, 8),
        "Renegociado": (2, 6),
        "Cancelado": (0, 2),
}

def gerar_interacoes(contratos, data_carga):
 
    interacoes = []
 
    for contrato_id, data_vencimento, status_contrato in contratos:
 
        # Status sem cobrança (ex: Quitado) são ignorados
        if status_contrato not in QTD_INTERACOES:
            continue
 
        # A cobrança só começa 1 dia depois do vencimento
        inicio = data_vencimento + timedelta(days=1)
        if inicio > data_carga:
            continue  # contrato ainda não venceu, então não há cobrança
 
        minimo, maximo = QTD_INTERACOES[status_contrato]
        quantidade = random.randint(minimo, maximo)
        dias_janela = (data_carga - inicio).days
 
        interacoes_contrato = []
 
        for _ in range(quantidade):
 
            # data aleatória dentro da janela + hora comercial aleatória
            data_base = inicio + timedelta(days=random.randint(0, dias_janela))
            data_interacao = datetime.combine(data_base, datetime.min.time()) + timedelta(
                hours=random.randint(8, 18), minutes=random.randint(0, 59)
            )
 
            # sorteia o status com pesos e depois o resultado coerente com ele
            status_interacao = random.choices(list(RESULTADO.keys()), weights=PESOS_STATUS)[0]
            resultado = random.choice(RESULTADO[status_interacao])
 
            if resultado == "Telefone Inexistente":
                canal_interacao = random.choice(CANAL_TELEFONE)
            else:
                canal_interacao = random.choice(CANAL)
 
            interacoes_contrato.append(
                (contrato_id, data_interacao, canal_interacao, status_interacao, resultado)
            )
 
        # ordena por data, pra o interacao_id crescer junto com o tempo
        interacoes_contrato.sort(key=lambda x: x[1])
        interacoes += interacoes_contrato
 
    return interacoes
 
 
def inserir_interacoes(cursor, interacoes):
    "> Insere as interações em lote na tabela interacoes_cobrancas."
 
    query = (
        "INSERT INTO interacoes_cobrancas "
        "(contrato_id, data_interacao, canal_interacao, status_interacao, resultado) "
        "VALUES (%s, %s, %s, %s, %s);"
    )
 
    cursor.executemany(query, interacoes)