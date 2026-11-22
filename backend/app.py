from flask import Flask, jsonify
from login import login_bp
from cadastro import cadastro_bp

app = Flask(__name__)

app.register_blueprint(login_bp)
app.register_blueprint(cadastro_bp)

@app.route("/", methods=["GET"])
def inicio():
    return jsonify({
        "mensagem": "Backend do Gym-System em funcionamento"
    })

if __name__ == "__main__":
    app.run(debug=True)
