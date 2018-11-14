from flask import Flask, jsonify, request
app = Flask(__name__)
from pymodm import connect
from pymodm import MongoModel, fields
from database import User


@app.route("/api/new_patient", methods=["POST"])
def get_new_patient():
    r = request.get_json() #parses input request data as json
    patient = User(_id=r["patient_id"], attending_email=r["attending_email"], user_age=r["user_age"])
    patient.save()



if __name__ == "__main__":
    connect("mongodb://rebeccacohen:bme590@ds037768.mlab.com:37768/bme_590")
    app.run(host="127.0.0.1")