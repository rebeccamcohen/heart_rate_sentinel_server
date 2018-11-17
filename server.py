from flask import Flask, jsonify, request
from pymodm import connect
from validation import validate_new_patient
from validation import check_new_id
from validation import InputError
from validation import validate_post_heart_rate
from validation import ValidationError
from validation import check_list_empty
from validation import EmptyHrListError
from validation import check_id_exists
from validation import validate_post_int_avg
from validation import check_hr_since_list_empty
from validation import NoHrSinceError
from database import User
from statistics import mean
from tachycardic import data_for_is_tach
from tachycardic import is_tachycardic
from internal_average import data_for_internal_average
from internal_average import hr_since_specified_time
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
    """Adds new patient info (patient id, attending email, and user age)
    to server and saves new patient to database

    Returns:
        Result (Response instance): Description noting successful addition
        of patient or explanation of error exception

    Excepts:
        ValidationError: If a required key is not present in request
        InputError: If the patient_id specified
        in request already exists

    """

    connect("mongodb://rebeccacohen:bme590@ds037768.mlab.com:37768/bme_590")
    r = request.get_json()  # parses input request data as json
    print(r)
    patient_id = r["patient_id"]

    check_new_id(r)

    try:
        validate_new_patient(r)
    except ValidationError as inst:
        logging.warning(inst.message)
        return jsonify({"message": inst.message})

    try:
        check_new_id(patient_id)
    except InputError as inst2:
        logging.warning(inst2.message)
        return jsonify({"message:": inst2.message})

    patient = User(patient_id=r["patient_id"],
                   attending_email=r["attending_email"],
                   user_age=r["user_age"])
    patient.save()

    result = {"message": "Added patient {0} successfully "
                         "to the database".format(patient_id)}
    logging.info("Added patient {0} successfully "
                 "to the database".format(patient_id))
    return jsonify(result)


@app.route("/api/heart_rate", methods=["POST"])
def heart_rate():
    """Saves heart rate measurement and time stamp
    (associated with a patient id) to database, checks
    if patient is tachycardic, and sends email if patient is tachycardic

    Returns:
        Result (Response instance): Description noting successful
        addition of heart rate or explanation of error exception

    Excepts:
        InputError: If specified user
        does not exist
        ValidationError: If a required
        key is not present in request



    """
    connect("mongodb://rebeccacohen:bme590@ds037768.mlab.com:37768/bme_590")
    r = request.get_json()  # parses input request data as json
    patient_id = r["patient_id"]
    hr = r["heart_rate"]

    try:
        check_id_exists(patient_id)
    except InputError as inst3:
        logging.warning("Specified a user that does not exist")
        return jsonify({"message": inst3.message})

    try:
        validate_post_heart_rate(r)
    except ValidationError as inst4:
        logging.warning(inst4.message)
        return jsonify({"message": inst4.message})

    dt = str(datetime.datetime.now())

    id_user = User.objects.raw({"_id": patient_id})
    id_user.update({"$push": {"heart_rate": r["heart_rate"]}})
    id_user.update({"$push": {"time_stamp": dt}})
    logging.info("stored heart rate measurement and associated time stamp")

    (age, recent_hr, recent_time_str) = data_for_is_tach(patient_id)
    is_tach = is_tachycardic(age, hr)

    if is_tach == 1:
        send_email(patient_id, recent_time_str)
        logging.info("Patient {0} is tachycardic "
                     "and email sent".format(patient_id))

    result = {"message": "heartrate added successfully to the database"}
    logging.info("heartrate added successfully to the database")
    return jsonify(result)


@app.route("/api/status/<patient_id>", methods=["GET"])
def get_status(patient_id):
    """Determine whether or not a
    specified patient is tachycardic
    based on previously available heart rate

    Args:
        patient_id: Specified patient id

    Returns:
        d (Response instance): Whether or not the patient is
        tachycardic and the time stamp associated
        with the most recent heart rate measurement

    Excepts:
        Input Error: If specified user does not exist
        EmptyHrListError: If no heart rate
        measurements exist for specified user


    """

    connect("mongodb://rebeccacohen:bme590@ds037768.mlab.com:37768/bme_590")
    r = int(patient_id)
    try:
        check_id_exists(r)
    except InputError as inst4:
        logging.warning("Specified a user that does not exist")
        return jsonify({"message": inst4.message})

    try:
        check_list_empty(r)
    except EmptyHrListError as inst5:
        logging.warning("No heart rate measurements exist for specified user")
        return jsonify({"message": inst5.message})

    (age, recent_hr, recent_time_str) = data_for_is_tach(r)

    is_tach = is_tachycardic(age, recent_hr)

    if is_tach == 1:
        d = {
            "message": "patient is tachycardic",
            "timestamp of recent hr measurement": recent_time_str
        }
        logging.info("successfully returned that patient is tachycardic")
        return jsonify(d)

    if is_tach == 0:
        d = {
            "message": "patient is tachycardic",
            "timestamp of recent hr measurement": recent_time_str
        }
        logging.info("successfully returned that patient is not tachycardic")
        return jsonify(d)


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def get_heart_rates(patient_id):
    """Returns all previous heart rate
    measurements for specified patient

    Args:
        patient_id: Specified patient id

    Returns:
        hr_list (Response instance): all previous heart rate
        measurements for specified patient

    Excepts:
        Input Error: If specified user does not exist
        EmptyHrListError: if no heart rate
        measurements exist for specified user

    """
    connect("mongodb://rebeccacohen:bme590@ds037768.mlab.com:37768/bme_590")
    r = int(patient_id)

    try:
        check_id_exists(r)
    except InputError as inst4:
        logging.warning("Specified a user that does not exist")
        return jsonify({"message": inst4.message})

    try:
        check_list_empty(r)
    except EmptyHrListError as inst5:
        logging.warning("No heart rate measurements exist for specified user")
        return jsonify({"message": inst5.message})

    p = User.objects.raw({"_id": r}).first()
    hr_list = p.heart_rate

    logging.info("Successfully returned all previous "
                 "heart rate measurements for specified patient")
    return jsonify(hr_list)


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def get_average_heart_rate(patient_id):
    """Calculates patient's average
    heart rate over all measurements stored for specified user

    Args:
        patient_id: Specified patient id

    Returns:
        avg_heart_rate (Response instance): average heart rate over all
        measurements stored for specified user

    Excepts:
        Input Error: If specified user does not exist
        EmptyHrListError: If no heart rate
        measurements exist for specified user

    """
    connect("mongodb://rebeccacohen:bme590@ds037768.mlab.com:37768/bme_590")
    r = int(patient_id)

    try:
        check_id_exists(r)
    except InputError as inst4:
        logging.warning("Specified a user that does not exist")
        return jsonify({"message": inst4.message})

    try:
        check_list_empty(r)
    except EmptyHrListError as inst5:
        logging.warning("No heart rate measurements exist for specified user")
        return jsonify({"message": inst5.message})

    p = User.objects.raw({"_id": r}).first()
    hr_list = p.heart_rate
    avg_heart_rate = mean(hr_list)
    logging.info("Successfully returned average "
                 "heart rate for specified user")
    return jsonify(avg_heart_rate)


@app.route("/api/heart_rate/internal_average", methods=["POST"])
def internal_average():
    """Calculates patient's internal average
    heart rate over
    measurements  since a specified time

    Returns:
        internal_avg (Response instance): heart rate
        average since specified time\

    Excepts:
        ValidationError: If a required key is not present in request
        ValueError: If inputted time_stamp data for
                        'heart_rate_average_since'
                        with incorrect format
        Input Error: If specified user does not exist
        EmptyHrListError: If no heart rate measurements
        exist for specified user
        NoHrSinceError: If no heart rate measurements
        exist since specified time


    """

    connect("mongodb://rebeccacohen:bme590@ds037768.mlab.com:37768/bme_590")
    r = request.get_json()

    try:
        validate_post_int_avg(r)
    except ValidationError as inst:
        logging.warning(inst.message)
        return jsonify({"message": inst.message})

    patient_id_str = r["patient_id"]
    patient_id = int(patient_id_str)

    try:
        d = datetime.datetime.strptime(r["heart_rate_average_since"],
                                       "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        logging.warning("inputted time_stamp data for "
                        "'heart_rate_average_since' "
                        "with incorrect format. "
                        "Use format '%Y-%m-%d %H:%M:%S.%f'")
        return jsonify("inputted time_stamp data for "
                       "'heart_rate_average_since' "
                       "with incorrect format. "
                       "Use format '%Y-%m-%d %H:%M:%S.%f'")

    try:
        check_id_exists(patient_id)
    except InputError:
        logging.warning("Specified a user that does not exist")
        return jsonify("Specified a user that does not exist")

    try:
        check_list_empty(patient_id)
    except EmptyHrListError as inst5:
        logging.warning("No heart rate measurements exist for specified user")
        return jsonify({"message": inst5.message})

    (time_stamps, hr_list) = data_for_internal_average(patient_id)

    heart_rates_since = hr_since_specified_time(d, time_stamps, hr_list)

    try:
        check_hr_since_list_empty(heart_rates_since)
    except NoHrSinceError:
        logging.warning("No heart rate measurements "
                        "taken since specified date")
        return jsonify("No heart rate measurements "
                       "taken since specified date")

    internal_avg = mean(heart_rates_since)
    return jsonify(internal_avg)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
