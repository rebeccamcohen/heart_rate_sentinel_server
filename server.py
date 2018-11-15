from flask import Flask, jsonify, request
from pymodm import connect
from new_patient import validate_new_patient_request
from heart_rate import validate_heart_rates_requests
from new_patient import ValidationError
from heart_rate import ValidationError
from database import User
from statistics import mean
from tachycardic import is_tachycardic
import datetime
import logging

logging.basicConfig(filename="main_log.txt",
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)

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


@app.route("/api/heart_rate", methods=["POST"])
def heart_rate():
    connect("mongodb://rebeccacohen:bme590@ds037768.mlab.com:37768/bme_590")
    r = request.get_json()  # parses input request data as json
    dt = datetime.datetime.now()
    print(r)
    print(dt)

    id_user = User.objects.raw({"_id": r["patient_id"]})
    id_user.update({"$push": {"heart_rate": r["heart_rate"]}})
    id_user.update({"$push": {"time_stamp": dt}})

    result = {
        "message": "stored heart rate measurement and associated time stamp"
    }
    return jsonify(result)


@app.route("/api/status/<patient_id>", methods=["GET"])
def get_status(patient_id):
    connect("mongodb://rebeccacohen:bme590@ds037768.mlab.com:37768/bme_590")
    r = int(patient_id)
    for user in User.objects.raw({"_id": r}):
        recent_hr = user.heart_rate[-1]
        age = user.user_age

        is_tachycardic(recent_hr, age)



@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def get_heart_rates(patient_id):
    connect("mongodb://rebeccacohen:bme590@ds037768.mlab.com:37768/bme_590")
    r = int(patient_id)

    try:
        for user in User.objects.raw({"_id": r}):
            try:
                validate_heart_rates_requests(user.heart_rate)
            except ValidationError:
                logging.warning("No heart rate "
                                "measurements associated with "
                                "specified patient")
                return jsonify({"message": "No heart rate "
                                           "measurements associated with "
                                           "specified patient"})
        logging.info("Successfully returned all "
                     "previous heart rate measurements "
                     "for specified patient")
        return jsonify(user.heart_rate)
    except UnboundLocalError:
        logging.warning("Tried to specify a patient that does not exist")
        raise ValidationError("Specified patient does not exist")


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def get_average_heart_rate(patient_id):
    connect("mongodb://rebeccacohen:bme590@ds037768.mlab.com:37768/bme_590")
    r = int(patient_id)

    try:
        for user in User.objects.raw({"_id": r}):
            try:
                validate_heart_rates_requests(user.heart_rate)
            except ValidationError:
                logging.warning("No heart rate "
                                "measurements associated with "
                                "specified patient")
                return jsonify({"message": "No heart rate "
                                           "measurements associated with "
                                           "specified patient"})

        logging.info("Successfully returned patient's average heart rate")
        avg_heart_rate = mean(user.heart_rate)
        return jsonify(avg_heart_rate)

    except UnboundLocalError:
        logging.warning("Tried to specify a patient that does not exist")
        raise ValidationError("Specified patient does not exist")


if __name__ == "__main__":
    app.run(host="127.0.0.1")
