from datetime import date
from db import conectar_banco
from gerar_clientes import gerar_clientes, inserir_clientes
from gerar_assessorias import gerar_assessorias, inserir_assessorias
from gerar_contratos import gerar_contratos, inserir_contratos
from gerar_pagamentos import gerar_pagamentos, inserir_pagamentos
from gerar_interacoes import gerar_interacoes, inserir_interacoes
import random

random.seed(42)




if __name__ == "__main__":
    conn, cursor = conectar_banco()

    try:

        #clientes = gerar_clientes(60000)
        #inserir_clientes(cursor, clientes)
        #conn.commit()
        #print("> Clientes inseridos com sucesso.")

        #assessorias = gerar_assessorias(500)
        #inserir_assessorias(cursor, assessorias)
        #conn.commit()
        #print("> Assessorias inseridas com sucesso.")
        
        #cursor.execute("SELECT cliente_id FROM clientes ORDER BY cliente_id ASC")
        #clientes_ids = [row[0] for row in cursor.fetchall()]

        #cursor.execute("SELECT assessoria_id FROM assessorias ORDER BY assessoria_id ASC")
        #assessorias_ids = [row[0] for row in cursor.fetchall()]

        #contratos = gerar_contratos(60000, clientes_ids, assessorias_ids)
        #inserir_contratos(cursor, contratos)
        #conn.commit()
        #print("> Contratos inseridos com sucesso.")

        #cursor.execute("SELECT contrato_id, data_contratacao, valor_divida, status_contrato, numero_parcelas FROM contratos ORDER BY data_contratacao ASC")
        #data_carga = date.today()
        #contratos = cursor.fetchall()

        #pagamentos = gerar_pagamentos(contratos, data_carga)
        #inserir_pagamentos(cursor, pagamentos)
        #conn.commit()
        #print("> Pagamentos inseridos com sucesso.")

        cursor.execute("SELECT contrato_id, data_vencimento, status_contrato FROM contratos ORDER BY data_contratacao ASC")
        data_carga = date.today()
        contratos = cursor.fetchall()

        interacoes = gerar_interacoes(contratos, data_carga)
        inserir_interacoes(cursor, interacoes)
        conn.commit()
        print("> Interações inseridas com sucesso")

    except Exception as e:
        conn.rollback()
        print(f"Erro: {e}")

    finally:
        cursor.close()
        conn.close()