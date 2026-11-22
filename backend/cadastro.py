
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

    except mysql.connector.Error:
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
