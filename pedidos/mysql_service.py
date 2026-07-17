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
    		
    
    SELECT
    
            cl.razao_social,
			p.numero_pedido,
			p.etapa,
			e.descricao_etapa,
			p.codigo_cliente,
			case when op.numero_op is null then 
            rc.dtSugestao else data_previsao end as data_previsao,
			REGEXP_REPLACE(c.cnpj_cpf, '[^0-9]', '') as cnpj_cpf,
			op.numero_op,
            case  when pro.descricao is null then it.descricao else pro.descricao
            end
            as descricao_produto,
            op.numero_CodProduto,	
            op.quantidade,
			op.etapaid,
             rc.codIntReqCompra,
            
			case when eop.descricao_etapa is null and rc.dtSugestao is not null then 
			'Requisição de compra' else eop.descricao_etapa end as 'status_producao'
			
		FROM pedidos p
		LEFT JOIN (SELECT * FROM etapas WHERE descricao_operacao = 'Venda de Produto') e ON e.codigo_etapa = p.etapa
		INNER JOIN clientes c on c.codigo_cliente_omie = p.codigo_cliente
		LEFT JOIN ordem_producao op on op.numero_pedido = p.numero_pedido
		LEFT JOIN requisicoes_compra rc on rc.numero_pedido = p.numero_pedido
		LEFT JOIN (SELECT * FROM etapas WHERE descricao_operacao = 'Ordem de Produção') eop ON eop.codigo_etapa = op.etapaid
        LEFT JOIN produtos pro on pro.codigo_produto = op.numero_CodProduto
        LEFT JOIN clientes cl on cl.codigo_cliente_omie = p.codigo_cliente
        LEFT JOIN itens_pedido it on it.numero_pedido = p.numero_pedido
		WHERE
        (
            eop.descricao_etapa IS NOT NULL
            OR rc.dtSugestao IS NOT NULL
        )
        
        group by op.numero_op, p.numero_pedido, descricao_produto
        having status_producao <> 'Armazenar/Expedir'
        ORDER BY p.data_previsao DESC
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