from flask import Blueprint, request, jsonify
import re

cadastro_bp = Blueprint("cadastro", __name__)

@cadastro_bp.route("/cadastro/aluno", methods=["POST"])
def cadastrar_aluno():
    nome = request.form.get("nome", "").strip()
    data_nascimento = request.form.get("data_nascimento", "").strip()
    telefone = request.form.get("telefone", "").strip()
    genero = request.form.get("genero", "").strip()
    email = request.form.get("email", "").strip().lower()
    cpf = request.form.get("cpf", "").strip()
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

    campos_vazios = [
        campo for campo, valor in campos_obrigatorios.items()
        if not valor
    ]

    if campos_vazios:
        return jsonify({
            "status": "erro",
            "mensagem": "Preencha todos os campos obrigatórios."
        }), 400

    cpf = re.sub(r"\D", "", cpf)

    if len(cpf) != 11:
        return jsonify({
            "status": "erro",
            "mensagem": "CPF inválido."
        }), 400

    return jsonify({
        "status": "validado",
        "mensagem": "Dados recebidos e validados. O salvamento no banco será implementado na próxima etapa."
    }), 200
