from faker import Faker
import random


locales_estrangeiros = ["en_US", "it_IT", "fr_FR"]

REGIOES_ESTADOS = {
    "Norte": ["AC", "AM", "AP", "PA", "RO", "RR", "TO"],
    "Nordeste": ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"],
    "Centro_Oeste": ["DF", "GO", "MT", "MS"],
    "Sudeste": ["ES", "MG", "RJ", "SP"],
    "Sul": ["PR", "RS", "SC"],
}

def gerar_assessorias(n):
    "> Gera (regiao) fictícias, mas coerentes entre si."

    assessorias = []

    for _ in range(n):

        fake_cidade = Faker(random.choice(locales_estrangeiros))
        nome = f"Assessoria {fake_cidade.city()}"

        regiao_atuacao = random.choice(list(REGIOES_ESTADOS.keys()))
        assessorias.append((nome, regiao_atuacao))
        

    return assessorias

def inserir_assessorias(cursor, assessorias):
    "> Insere as assessorias em lote na tabela assessorias."

    query = "INSERT INTO assessorias (nome, regiao_atuacao) VALUES (%s, %s);"

    cursor.executemany(query, assessorias)