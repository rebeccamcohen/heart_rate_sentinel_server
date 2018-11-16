from flask import Flask, jsonify, request
from pymodm import connect
from new_patient import validate_new_patient_request
from heart_rate import validate_heart_rates_requests
from new_patient import ValidationError
from heart_rate import ValidationError
from database import User
from statistics import mean
from tachycardic import is_tachycardic
from sendgrid_email import send_email
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
    dt = str(datetime.datetime.now())
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
            recent_hr = user.heart_rate[-1]
            age = float(user.user_age)
            recent_time_stamp = user.time_stamp[-1]
            time_str = str(recent_time_stamp)
            is_tach = is_tachycardic(age, recent_hr)

            if is_tach == 1:
                d = {
                    "message": "patient is tachycardic",
                    "timestamp of recent hr measurement": time_str
                }

                send_email(r, time_str)

                return jsonify(d)

            if is_tach == 0:
                d = {
                    "message": "patient is not tachycardic",
                    "timestamp of recent hr measurement": time_str
                }
                return jsonify(d)
    except UnboundLocalError:
        logging.warning("Tried to specify a patient that does not exist")
        raise ValidationError("Specified patient does not exist")


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

@app.route("/api/heart_rate/internal_average", methods=["POST"])
def internal_average():
    connect("mongodb://rebeccacohen:bme590@ds037768.mlab.com:37768/bme_590")
    r = request.get_json()  # parses input request data as json
    d = datetime.datetime.strptime(r[""], "%Y-%m-%d %H:%M:%S.%f")

p = User.objects.raw({"_id": 6}).first()
list = p.time_stamp
hr_list = p.heart_rate
l = []
for item in list:
    if item > datetime.datetime(2018, 11, 15, 18, 2, 32, 33843):
        index = list.index(item)
        l.append(hr_list[index])


if __name__ == "__main__":
    app.run(host="127.0.0.1")
