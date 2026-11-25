
from flask import Blueprint, request, jsonify
from database import conectar_banco
from werkzeug.security import generate_password_hash
import re
import mysql.connector

cadastro_bp = Blueprint("cadastro", __name__)


@cadastro_bp.route("/cadastro/aluno", methods=["POST"])
def cadastrar_aluno():
    nome = request.form.get("nome", "").strip()
    data_nascimento = request.form.get("data_nascimento", "").strip()
    telefone = request.form.get("telefone", "").strip()
    genero = request.form.get("genero", "").strip()
    email = request.form.get("email", "").strip().lower()
    cpf = re.sub(r"\D", "", request.form.get("cpf", ""))
    senha = request.form.get("senha", "")

    campos_obrigatorios = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "telefone": telefone,
        "genero": genero,
        "email": email,
        "cpf": cpf,
        "senha": senha
    }

    if any(not valor for valor in campos_obrigatorios.values()):
        return jsonify({
            "status": "erro",
            "mensagem": "Preencha todos os campos obrigatórios."
        }), 400

    if len(cpf) != 11:
        return jsonify({
            "status": "erro",
            "mensagem": "CPF inválido."
        }), 400

    conexao = None
    cursor = None

    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT id_usuario FROM usuarios WHERE cpf = %s OR email = %s",
            (cpf, email)
        )

        if cursor.fetchone():
            return jsonify({
                "status": "erro",
                "mensagem": "CPF ou e-mail já cadastrado."
            }), 409

        senha_hash = generate_password_hash(senha)

        cursor.execute("""
            INSERT INTO usuarios
            (cpf, nome, email, data_nascimento, telefone, genero, senha)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            cpf,
            nome,
            email,
            data_nascimento,
            telefone,
            genero,
            senha_hash
        ))

        id_usuario = cursor.lastrowid

        cursor.execute(
            "INSERT INTO alunos (id_usuario) VALUES (%s)",
            (id_usuario,)
        )

        conexao.commit()

        return jsonify({
            "status": "sucesso",
            "mensagem": "Aluno cadastrado com sucesso."
        }), 201

    except mysql.connector.IntegrityError:
        if conexao:
            conexao.rollback()

        return jsonify({
            "status": "erro",
            "mensagem": "CPF ou e-mail já cadastrado."
        }), 409

    except mysql.connector.Error as erro:
        print("Erro MySQL:", erro)

        if conexao:
            conexao.rollback()

        return jsonify({
            "status": "erro",
            "mensagem": "Erro ao realizar o cadastro."
        }), 500

    finally:
        if cursor:
            cursor.close()

        if conexao:
            conexao.close()


@cadastro_bp.route("/cadastro/exercicio", methods=["POST"])
def cadastrar_exercicio():
    nome = request.form.get("nome", "").strip()
    maquina = request.form.get("maquina", "").strip()
    descricao = request.form.get("descricao", "").strip()

    if not nome or not maquina or not descricao:
        return jsonify({
            "status": "erro",
            "mensagem": "Preencha todos os campos."
        }), 400

    conexao = None
    cursor = None

    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO exercicios (nome, maquina, descricao)
            VALUES (%s, %s, %s)
        """, (nome, maquina, descricao))

        conexao.commit()

        return jsonify({
            "status": "sucesso",
            "mensagem": "Exercício cadastrado com sucesso."
        }), 201

    except mysql.connector.Error as erro:
        print("Erro MySQL:", erro)

        if conexao:
            conexao.rollback()

        return jsonify({
            "status": "erro",
            "mensagem": "Erro ao cadastrar exercício."
        }), 500

    finally:
        if cursor:
            cursor.close()

        if conexao:
            conexao.close()


@cadastro_bp.route("/exercicios", methods=["GET"])
def listar_exercicios():
    conexao = None
    cursor = None

    try:
        conexao = conectar_banco()
        cursor = conexao.cursor(dictionary=True)

        cursor.execute("""
            SELECT id_exercicio, nome, maquina, descricao
            FROM exercicios
            ORDER BY nome
        """)

        exercicios = cursor.fetchall()

        return jsonify(exercicios), 200

    except mysql.connector.Error as erro:
        print("Erro MySQL:", erro)

        return jsonify({
            "status": "erro",
            "mensagem": "Erro ao consultar exercícios."
        }), 500

    finally:
        if cursor:
            cursor.close()

        if conexao:
            conexao.close()


@cadastro_bp.route("/alunos", methods=["GET"])
def listar_alunos():
    conexao = None
    cursor = None

    try:
        conexao = conectar_banco()
        cursor = conexao.cursor(dictionary=True)

        cursor.execute("""
            SELECT usuarios.id_usuario, usuarios.nome, usuarios.email
            FROM usuarios
            INNER JOIN alunos
            ON usuarios.id_usuario = alunos.id_usuario
            ORDER BY usuarios.nome
        """)

        alunos = cursor.fetchall()

        return jsonify(alunos), 200

    except mysql.connector.Error as erro:
        print("Erro MySQL:", erro)

        return jsonify({
            "status": "erro",
            "mensagem": "Erro ao consultar alunos."
        }), 500

    finally:
        if cursor:
            cursor.close()

        if conexao:
            conexao.close()


@cadastro_bp.route("/treinos", methods=["POST"])
def cadastrar_treino():
    dados = request.get_json()

    if not dados:
        return jsonify({
            "status": "erro",
            "mensagem": "Dados não enviados."
        }), 400

    id_aluno = dados.get("id_aluno")
    nome = dados.get("nome", "").strip() if isinstance(dados.get("nome"), str) else ""
    descricao = dados.get("descricao", "")
    exercicios = dados.get("exercicios", [])

    if not id_aluno or not nome or not isinstance(exercicios, list) or not exercicios:
        return jsonify({
            "status": "erro",
            "mensagem": "Informe o aluno, o nome do treino e pelo menos um exercício."
        }), 400

    conexao = None
    cursor = None

    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT id_usuario FROM alunos WHERE id_usuario = %s",
            (id_aluno,)
        )

        if not cursor.fetchone():
            return jsonify({
                "status": "erro",
                "mensagem": "Aluno não encontrado."
            }), 404

        cursor.execute("""
            INSERT INTO treinos (id_aluno, nome, descricao)
            VALUES (%s, %s, %s)
        """, (id_aluno, nome, descricao))

        id_treino = cursor.lastrowid

        for exercicio in exercicios:
            if not isinstance(exercicio, dict):
                raise ValueError("Dados de exercício inválidos.")

            id_exercicio = exercicio.get("id_exercicio")
            series = exercicio.get("series")
            repeticoes = exercicio.get("repeticoes")

            if not id_exercicio or not series or not repeticoes:
                raise ValueError("Dados de exercício inválidos.")

            if int(series) < 1 or int(repeticoes) < 1:
                raise ValueError("Séries e repetições devem ser maiores que zero.")

            cursor.execute("""
                INSERT INTO treino_exercicios
                (id_treino, id_exercicio, series, repeticoes)
                VALUES (%s, %s, %s, %s)
            """, (id_treino, id_exercicio, series, repeticoes))

        conexao.commit()

        return jsonify({
            "status": "sucesso",
            "mensagem": "Treino cadastrado com sucesso.",
            "id_treino": id_treino
        }), 201

    except (ValueError, TypeError) as erro:
        if conexao:
            conexao.rollback()

        return jsonify({
            "status": "erro",
            "mensagem": str(erro)
        }), 400

    except mysql.connector.Error as erro:
        if conexao:
            conexao.rollback()

        print("Erro MySQL:", erro)

        return jsonify({
            "status": "erro",
            "mensagem": "Erro ao cadastrar o treino."
        }), 500

    finally:
        if cursor:
            cursor.close()

        if conexao:
            conexao.close()
@cadastro_bp.route("/treinos/<int:id_aluno>", methods=["GET"])
def listar_treinos_aluno(id_aluno):
    conexao = None
    cursor = None

    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                t.id_treino,
                t.nome,
                t.descricao,
                e.id_exercicio,
                e.nome,
                te.series,
                te.repeticoes
            FROM treinos t
            LEFT JOIN treino_exercicios te
                ON t.id_treino = te.id_treino
            LEFT JOIN exercicios e
                ON te.id_exercicio = e.id_exercicio
            WHERE t.id_aluno = %s
            ORDER BY t.id_treino, e.nome
        """, (id_aluno,))

        resultados = cursor.fetchall()
        treinos = {}

        for linha in resultados:
            id_treino = linha[0]

            if id_treino not in treinos:
                treinos[id_treino] = {
                    "id_treino": id_treino,
                    "nome": linha[1],
                    "descricao": linha[2],
                    "exercicios": []
                }

            if linha[3] is not None:
                treinos[id_treino]["exercicios"].append({
                    "id_exercicio": linha[3],
                    "nome": linha[4],
                    "series": linha[5],
                    "repeticoes": linha[6]
                })

        return jsonify(list(treinos.values()))

    except mysql.connector.Error as erro:
        print("Erro MySQL:", erro)
        return jsonify({
            "status": "erro",
            "mensagem": "Erro ao consultar os treinos."
        }), 500

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()
            
@cadastro_bp.route("/treinos/<int:id_treino>", methods=["PUT"])
def editar_treino(id_treino):
    dados = request.get_json()

    if not dados:
        return jsonify({
            "status": "erro",
            "mensagem": "Dados não enviados."
        }), 400

    nome = dados.get("nome", "").strip()
    descricao = dados.get("descricao", "")
    exercicios = dados.get("exercicios", [])

    if not nome or not exercicios:
        return jsonify({
            "status": "erro",
            "mensagem": "Informe o nome e pelo menos um exercício."
        }), 400

    conexao = None
    cursor = None

    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT id_treino FROM treinos WHERE id_treino = %s",
            (id_treino,)
        )

        if not cursor.fetchone():
            return jsonify({
                "status": "erro",
                "mensagem": "Treino não encontrado."
            }), 404

        cursor.execute("""
            UPDATE treinos
            SET nome = %s, descricao = %s
            WHERE id_treino = %s
        """, (nome, descricao, id_treino))

        cursor.execute(
            "DELETE FROM treino_exercicios WHERE id_treino = %s",
            (id_treino,)
        )

        for exercicio in exercicios:
            id_exercicio = exercicio.get("id_exercicio")
            series = int(exercicio.get("series", 0))
            repeticoes = int(exercicio.get("repeticoes", 0))

            if not id_exercicio or series < 1 or repeticoes < 1:
                raise ValueError("Dados dos exercícios inválidos.")

            cursor.execute("""
                INSERT INTO treino_exercicios
                (id_treino, id_exercicio, series, repeticoes)
                VALUES (%s, %s, %s, %s)
            """, (id_treino, id_exercicio, series, repeticoes))

        conexao.commit()

        return jsonify({
            "status": "sucesso",
            "mensagem": "Treino atualizado com sucesso."
        })

    except (ValueError, TypeError) as erro:
        if conexao:
            conexao.rollback()

        return jsonify({
            "status": "erro",
            "mensagem": str(erro)
        }), 400

    except mysql.connector.Error as erro:
        if conexao:
            conexao.rollback()

        print("Erro MySQL:", erro)

        return jsonify({
            "status": "erro",
            "mensagem": "Erro ao atualizar o treino."
        }), 500

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()
