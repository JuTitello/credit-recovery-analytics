import random

REGIOES_ESTADOS = {
    "Norte": ["AC", "AM", "AP", "PA", "RO", "RR", "TO"],
    "Nordeste": ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"],
    "Centro_Oeste": ["DF", "GO", "MT", "MS"],
    "Sudeste": ["ES", "MG", "RJ", "SP"],
    "Sul": ["PR", "RS", "SC"],
}

def gerar_clientes(n):
    "> Gera n tuplas (regiao, estado) fictícias, mas coerentes entre si."
     
    clientes = []

    for _ in range(n):

        regiao = random.choice(list(REGIOES_ESTADOS.keys()))
        estado = random.choice(REGIOES_ESTADOS[regiao])
        clientes.append((regiao,estado))

    return clientes

def inserir_clientes(cursor, clientes):
     "> Insere os clientes em lote na tabela clientes."

     query = "INSERT INTO clientes (regiao, estado) VALUES (%s, %s);"

     cursor.executemany(query, clientes)