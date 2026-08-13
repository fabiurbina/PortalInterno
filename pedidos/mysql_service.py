# mysql_service.py

import pymysql
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def consultar_conferencias(codigo_op):

    conn = pymysql.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE"),
        charset="utf8mb4"
    )

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql = """
    SELECT
        codigo_produto,
        usuario,
        data_conferencia
    FROM conferencia_op
    WHERE codigo_op = %s
    """

    cursor.execute(sql, (codigo_op,))

    resultado = cursor.fetchall()

    cursor.close()
    conn.close()

    return resultado


def salvar_conferencia_mysql(
    codigo_op,
    codigo_produto,
    descricao_produto,
    tipo,
    lote,
    validade,
    conferido,
    usuario,
    lote_pa,
    validade_pa,
    observacao,
    limpeza_sala,
    limpeza_equipamento,
):

    conn = pymysql.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE"),
        charset="utf8mb4"
    )

    cursor = conn.cursor()

    sql = """
    INSERT INTO conferencia_op (
        codigo_op,
        codigo_produto,
        descricao_produto,
        tipo,
        lote,
        validade,
        conferido,
        usuario,
        data_conferencia,
        lote_pa,
        validade_pa,
        observacao,
        limpeza_sala,
        limpeza_equipamento
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(
        sql,
        (
            codigo_op,
            codigo_produto,
            descricao_produto,
            tipo,
            lote,
            validade,
            True,
            usuario,
            datetime.now(),
            lote_pa,
            validade_pa,
            observacao,
            limpeza_sala,
            limpeza_equipamento
        )
    )

    conn.commit()

    cursor.close()
    conn.close()
    
    
def salvar_observacao_op(
    codigo_op,
    observacao,
    usuario
):

    conn = pymysql.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE"),
        charset="utf8mb4"
    )

    cursor = conn.cursor()

    sql = """
    INSERT INTO observacoes_op (
        codigo_op,
        observacao,
        usuario
    )
    VALUES (%s,%s,%s)
    """

    cursor.execute(
        sql,
        (
            codigo_op,
            observacao,
            usuario
        )
    )

    conn.commit()

    cursor.close()
    conn.close()
    
    
def salvar_apontamento(
    codigo_op,
    etapa,
    equipamento_limpo,
    area_limpa,
    mp_conferidas,
    data_inicio,
    data_fim,
    medida_prevista=None,
    medida_real=None,
    medida_perdas=None,
    unidade=None,
    usuario=None,
    observacao=None
):

    conn = pymysql.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE"),
        charset="utf8mb4"
    )

    cursor = conn.cursor()

    sql = """
    INSERT INTO op_apontamentos
    (
      
        codigo_op,
        etapa,
        equipamento_limpo,
        area_limpa,
        mp_conferidas,
        data_inicio,
        data_fim,
        medida_prevista,
        medida_real,
        medida_perdas,
        unidade,
        usuario,
        observacao
    )
    VALUES
    (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s
    )
    """

    cursor.execute(
        sql,
        (
            
            codigo_op,
            etapa,
            equipamento_limpo,
            area_limpa,
            mp_conferidas,
            data_inicio,
            data_fim,
            medida_prevista,
            medida_real,
            medida_perdas,
            unidade,
            usuario,
            observacao
        )
    )

    conn.commit()

    cursor.close()

    conn.close()
    
    
    
def salvar_setup(
    codigo_op,
    idMaquina,
    hora_inicio,
    hora_fim=None,
    usuario=None,
    observacao=None
):

    conn = pymysql.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE"),
        charset="utf8mb4"
    )

    cursor = conn.cursor()

    sql = """
    INSERT INTO op_setup
    (
        codigo_op,
        idMaquina,
        hora_inicio,
        hora_fim,
        usuario,
        observacao
    )
    VALUES
    (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s
    )
    """

    cursor.execute(
        sql,
        (
            codigo_op,
            idMaquina,
            hora_inicio,
            hora_fim,
            usuario,
            observacao
        )
    )

    conn.commit()

    cursor.close()

    conn.close()
    
from datetime import datetime, date   
def salvar_parada_sql(
    codigo_op,
    tipo_parada,
    motivo,
    data_inicio,
    data_fim,
    observacao,
    usuario
):

    conn = pymysql.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE"),
        charset="utf8mb4"
    )

    cursor = conn.cursor()

    # ==============================
    # CONVERTE HORÁRIO PARA DATETIME
    # ==============================

    if data_inicio:
        hora_inicio = datetime.strptime(data_inicio, "%H:%M").time()
        data_inicio = datetime.combine(date.today(), hora_inicio)

    if data_fim:
        hora_fim = datetime.strptime(data_fim, "%H:%M").time()
        data_fim = datetime.combine(date.today(), hora_fim)

    # ==============================
    # INSERT
    # ==============================

    sql = """
        INSERT INTO paradas_producao (
            codigo_op,
            tipo_parada,
            motivo,
            data_inicio,
            data_fim,
            duracao_min,
            observacao,
            usuario
        )
        VALUES (
            %s, %s, %s, %s, %s,
            TIMESTAMPDIFF(
                MINUTE,
                %s,
                %s
            ),
            %s,
            %s
        )
    """

    try:

        cursor.execute(sql, (
            codigo_op,
            tipo_parada,
            motivo,
            data_inicio,
            data_fim,
            data_inicio,
            data_fim,
            observacao,
            usuario
        ))

        conn.commit()

        print("✅ Parada registrada com sucesso!")

    except Exception as e:

        conn.rollback()

        print(f"❌ Erro ao registrar parada: {e}")

        raise

    finally:

        cursor.close()
        conn.close()
    
    
def consultar_apontamentos(codigo_op):

    conn = pymysql.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE"),
        charset="utf8mb4"
    )

    cursor = conn.cursor(
        pymysql.cursors.DictCursor
    )

    cursor.execute(
        """
        SELECT *
        FROM op_apontamentos
        WHERE codigo_op = %s
        """,
        (codigo_op,)
    )

    resultado = cursor.fetchall()

    cursor.close()
    conn.close()

    return resultado



def consultar_todos_pedidos():
    conn = pymysql.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE"),
        charset="utf8mb4"
    )

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql = """
    		
    
    SELECT * FROM ViesanoDW.PipelineCli;
    
    """

    cursor.execute(sql)

    resultado = cursor.fetchall()

    cursor.close()
    conn.close()
    return resultado


def buscar_relatorio_mrp():

    conn = pymysql.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with conn.cursor() as cursor:

            query = """
                SELECT *
                FROM ViesanoDW.MRP
            """

            cursor.execute(query)

            dados = cursor.fetchall()

            return dados

    except Exception as e:

        print(f"❌ Erro ao buscar relatório MRP: {e}")

        return []

    finally:

        conn.close()
        
def inserir_inspecao(
    codigo_for,
    revisao,
    data_vigente,
    codigo_produto,
    codigo_fornecedor,
    qtdd,
    data_recebimento,
    status,
    lote,
    data_fabricacao,
    data_validade,
    data,
    hora_inicio,
    hora_fim,
    parecer,
    motivo,
    observacoes,
    responsavel
):

    conn = pymysql.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE"),
        charset="utf8mb4"
    )

    cursor = conn.cursor()

    sql = """
        INSERT INTO tabInpecaoQualidade
        (
            codigo_for,
            revisao,
            data_vigente,
            codigo_produto,
            codido_fornecedor,
            qtdd,
            data_recebimento,
            status,
            lote,
            data_fabricacao,
            data_validade,
            data,
            hora_inicio,
            hora_fim,
            parecer,
            motivo,
            observacoes,
            responsavel
        )
        VALUES
        (
            %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """

    valores = (
        codigo_for,
        revisao,
        data_vigente,
        codigo_produto,
        codigo_fornecedor,
        qtdd,
        data_recebimento,
        status,
        lote,
        data_fabricacao,
        data_validade,
        data,
        hora_inicio,
        hora_fim,
        parecer,
        motivo,
        observacoes,
        responsavel
    )

    cursor.execute(sql, valores)

    conn.commit()

    id_inspecao = cursor.lastrowid

    cursor.close()
    conn.close()

    return id_inspecao


def inserir_resultado_inspecao(
    id_inspecao,
    id_parametro,
    resultado,
    conforme,
    observacao
):

    conn = pymysql.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE"),
        charset="utf8mb4"
    )

    cursor = conn.cursor()

    sql = """
        INSERT INTO tabResultadoInspecao
        (
            id_inspecao,
            id_parametro,
            resultado,
            conforme,
            observacao
        )
        VALUES
        (
            %s,%s,%s,%s,%s
        )
    """

    cursor.execute(
        sql,
        (
            id_inspecao,
            id_parametro,
            resultado,
            conforme,
            observacao
        )
    )

    conn.commit()

    cursor.close()
    conn.close()
    
    
def consultar_status_qualidade(codigo_produto, lote):

    conn = pymysql.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE"),
        charset="utf8mb4"
    )

    cursor = conn.cursor()

    sql = """
        SELECT parecer
        FROM tabInpecaoQualidade
        WHERE codigo_produto = %s
        AND lote = %s
        ORDER BY id DESC
        LIMIT 1
    """

    cursor.execute(
        sql,
        (
            codigo_produto,
            lote
        )
    )

    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    if resultado is None:
        return "Aguardando"

    parecer = resultado[0]

    if str(parecer) == "1":
        return "Aprovado"

    elif str(parecer) == "2":
        return "Reprovado"

    elif str(parecer) == "3":
        return "Aprovado com Restrição"

    return "Aguardando"


def buscar_lotes_sql(numero_op):

    conn = pymysql.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with conn.cursor() as cursor:

            query = """
                SELECT
                    codigo,
                    cNumLote,
                    dDataValidade
                FROM ViesanoDW.ConsumoLotes
                WHERE numero_op = %s
                  AND quantidade_consumida > 0
            """

            cursor.execute(query, (numero_op,))

            dados = cursor.fetchall()

            return {
                str(item["codigo_produto"]): {
                    "lote": item["cNumLote"],
                    "validade": item["dDataValidade"]
                }
                for item in dados
            }

    except Exception as e:

        print(f"Erro ao buscar lotes: {e}")
        return {}

    finally:
        conn.close()
        
        
def conectar():

    return pymysql.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )


def buscar_producao():

    sql = """
        SELECT *
        FROM vw_ia_producao
        ORDER BY ultima_atualizacao DESC
        LIMIT 20;
    """

    conexao = conectar()

    try:

        with conexao.cursor() as cursor:

            cursor.execute(sql)

            return cursor.fetchall()

    finally:

        conexao.close()
        
        
def buscar_CRM():

    sql = """
        SELECT *
        FROM vw_ia_comercial
    """

    conexao = conectar()

    try:

        with conexao.cursor() as cursor:

            cursor.execute(sql)

            return cursor.fetchall()

    finally:

        conexao.close()
        
if __name__ == "__main__":
    dados = buscar_CRM()
    print(dados)
    
    
def buscar_posicao_estoque(nome_estoque=None):

    sql = """
        SELECT *
        FROM ResumoEstoque
    """

    parametros = []

    if nome_estoque:
        sql += """
            WHERE nome_estoque = %s
        """

        parametros.append(nome_estoque)

    conexao = conectar()

    try:

        with conexao.cursor() as cursor:

            cursor.execute(sql, parametros)

            return cursor.fetchall()

    finally:

        conexao.close()
        
        
def buscar_previsao_demanda(
    nome_estoque=None,
    status=None,
    cDescrUsuario=None,
    Temperatura=None,
    identificacao_cNome=None
):
    sql = """
        SELECT *
        FROM ViesanoDW.vw_previsao_demandas
    """

    filtros = []
    parametros = []

    if nome_estoque:
        filtros.append("nome_estoque = %s")
        parametros.append(nome_estoque)

    if status:
        filtros.append("status = %s")
        parametros.append(status)

    if cDescrUsuario:
        filtros.append("cDescrUsuario = %s")
        parametros.append(cDescrUsuario)

    if Temperatura:
        filtros.append("Temperatura = %s")
        parametros.append(Temperatura)

    if identificacao_cNome:
        filtros.append("identificacao_cNome = %s")
        parametros.append(identificacao_cNome)

    if filtros:
        sql += " WHERE " + " AND ".join(filtros)

    conexao = conectar()

    try:
        with conexao.cursor() as cursor:
            cursor.execute(sql, parametros)
            return cursor.fetchall()
    finally:
        conexao.close()
        
        
        

        