
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from database import conectar_banco

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["POST"])
def realizar_login():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Dados não informados"}), 400

    email = dados.get("email")
    senha = dados.get("senha")
    tipo = dados.get("tipo")

    tabelas = {
        "aluno": "alunos",
        "professor": "professores",
        "funcionario": "funcionarios"
    }

    if not email or not senha or tipo not in tabelas:
        return jsonify({"erro": "Dados de login inválidos"}), 400

    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT id_usuario, nome, email, senha FROM usuarios WHERE email = %s",
            (email,)
        )

        usuario = cursor.fetchone()

        if not usuario or not check_password_hash(usuario["senha"], senha):
            return jsonify({"erro": "Email ou senha incorretos"}), 401

        tabela = tabelas[tipo]

        cursor.execute(
            f"SELECT id_usuario FROM {tabela} WHERE id_usuario = %s",
            (usuario["id_usuario"],)
        )

        if not cursor.fetchone():
            return jsonify({"erro": "Usuário não pertence a esta categoria"}), 401

        return jsonify({
            "mensagem": "Login realizado com sucesso",
            "id_usuario": usuario["id_usuario"],
            "nome": usuario["nome"],
            "tipo": tipo
        }), 200

    finally:
        cursor.close()
        conexao.close()

