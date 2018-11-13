from flask import Flask, jsonify, request
app = Flask(__name__)
from new_patient import new_patient


@app.route("/api/new_patient", methods=["POST"])
def get_new_patient():
    new_patient_dict = new_patient()
    return jsonify(new_patient_dict)

@app.route("/api/new_patient", methods=["POST"])


if __name__ == "__main__":
    app.run(host="127.0.0.1")