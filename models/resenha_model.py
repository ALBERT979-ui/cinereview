import unicodedata
from models.conexao import conectar, criar_cursor

def normalizar_texto(texto):

    texto = unicodedata.normalize(
        "NFD",
        texto
    )

    texto = "".join(
        letra
        for letra in texto
        if unicodedata.category(letra) != "Mn"
    )

    return texto.lower()

def buscar_resenhas(
        busca="",
        nota_minima=None,
        ordem="recentes"
):

    conexao = conectar()
    cursor = criar_cursor(conexao)

    comando = """
        SELECT
            id,
            nome,
            ano,
            resenha,
            nota,
            data_criacao
        FROM resenha
        WHERE 1=1
    """

    valores = []

    if busca:

        comando += """
            AND LOWER(nome)
            LIKE %s
        """

        valores.append(
            "%" + normalizar_texto(busca) + "%"
        )

    if nota_minima is not None:

        comando += """
            AND nota = %s
        """

        valores.append(
            nota_minima
        )

    if ordem == "alfabetica":

        comando += """
            ORDER BY LOWER(nome) ASC
        """

    elif ordem == "antigas":

        comando += """
            ORDER BY data_criacao ASC
        """

    else:

        comando += """
            ORDER BY data_criacao DESC
        """

    cursor.execute(
        comando,
        valores
    )

    dados = cursor.fetchall()

    resenhas = []

    for filme in dados:

        resenhas.append({
        "id": filme["id"],
        "nome": filme["nome"],
        "ano": filme["ano"],
        "resenha": filme["resenha"],
        "nota": filme["nota"],
        "data_criacao": filme["data_criacao"].strftime("%d/%m/%Y às %H:%M") if filme["data_criacao"] else "",
        "is_long": len(filme["resenha"]) > 250
    })

    cursor.close()
    conexao.close()

    return resenhas

def adicionar_resenha(
        nome,
        ano,
        texto,
        nota
):

    conexao = conectar()
    cursor = criar_cursor(conexao)

    cursor.execute(
        """
        SELECT id
        FROM resenha
        WHERE nome = %s
        AND ano = %s
        AND resenha = %s
        AND nota = %s
        """,
        (
            nome,
            ano,
            texto,
            nota
        )
    )

    existente = cursor.fetchone()

    if existente:

        cursor.close()
        conexao.close()

        return False

    cursor.execute(
        """
        INSERT INTO resenha
        (
            nome,
            ano,
            resenha,
            nota
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s
        )
        """,
        (
            nome,
            ano,
            texto,
            nota
        )
    )

    conexao.commit()

    cursor.close()
    conexao.close()

    return True

def contar_resenhas():

    conexao = conectar()
    cursor = criar_cursor(conexao)

    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM resenha
        """
    )

    total = cursor.fetchone()["total"]

    cursor.close()
    conexao.close()

    return total

def buscar_resenha_por_id(id):

    conexao = conectar()
    cursor = criar_cursor(conexao)

    cursor.execute(
        """
        SELECT
            id,
            nome,
            ano,
            resenha,
            nota,
            data_criacao
        FROM resenha
        WHERE id = %s
        """,
        (id,)
    )

    resenha = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resenha

def atualizar_resenha(
        id,
        nome,
        ano,
        texto,
        nota
):

    conexao = conectar()
    cursor = criar_cursor(conexao)

    cursor.execute(
        """
        UPDATE resenha
        SET
            nome = %s,
            ano = %s,
            resenha = %s,
            nota = %s
        WHERE id = %s
        """,
        (
            nome,
            ano,
            texto,
            nota,
            id
        )
    )

    conexao.commit()

    cursor.close()
    conexao.close()

def excluir_resenha(id):

    conexao = conectar()
    cursor = criar_cursor(conexao)

    cursor.execute(
        """
        DELETE FROM resenha
        WHERE id = %s
        """,
        (id,)
    )

    conexao.commit()

    cursor.close()
    conexao.close()