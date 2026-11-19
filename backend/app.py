from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def inicio():
    return jsonify({
        "mensagem": "Backend do Gym-System em funcionamento"
    })

if __name__ == "__main__":
    app.run(debug=True)
