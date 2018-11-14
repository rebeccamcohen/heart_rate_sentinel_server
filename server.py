from flask import Flask, jsonify, request
from pymodm import connect
from new_patient import validate_new_patient_request
from new_patient import ValidationError
from database import User

app = Flask(__name__)


@app.route("/api/new_patient", methods=["POST"])
def get_new_patient():
    connect("mongodb://rebeccacohen:bme590@ds037768.mlab.com:37768/bme_590")
    r = request.get_json()  # parses input request data as json
    print(r)
    # patient_dict = {
    #    "patient_id":r["patient_id"],
    #    "attending_email":r["attending_email"],
    #    "user_age":r["user_age"]
    # }
    # return jsonify(patient_dict)
    try:
        validate_new_patient_request(r)
    except ValidationError as inst:
        return jsonify({"message": inst.message})

    patient = User(patient_id=r["patient_id"],
                   attending_email=r["attending_email"],
                   user_age=r["user_age"])
    patient.save()

    result = {
        "message": "Added patient successfully "
                   "to the database"
    }
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="127.0.0.1")
