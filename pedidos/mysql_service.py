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
    data_inicio,
    data_fim,
    peso,
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
        INSERT INTO op_apontamentos
        (
            codigo_op,
            etapa,
            data_inicio,
            data_fim,
            peso,
            usuario
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
            etapa,
            data_inicio,
            data_fim,
            peso,
            usuario
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