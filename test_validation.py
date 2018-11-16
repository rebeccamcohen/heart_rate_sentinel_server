from validation import validate_new_patient
from validation import ValidationError
from validation import check_new_id
from validation import InputError
from validation import validate_post_heart_rate
from validation import check_id_exists
from validation import validate_post_int_avg
from validation import check_hr_since_list_empty
from validation import NoHrSinceError
from pymodm import connect
from test_database import test_User
import pytest


def test_get_new_patient1():
    new_patient = {
        "attending_email": "rebecca.cohen@duke.edu",
    }
    with pytest.raises(ValidationError):
        validate_new_patient(new_patient)


def test_get_new_patient2():
    new_patient = {
        "patient_id": 1,
        "attending_email": "rebecca.cohen@duke.edu",
        "age": 20
    }

    with pytest.raises(ValidationError):
        validate_new_patient(new_patient)


def test_check_new_id():
    connect("mongodb://rebeccamcohen:bme590@ds037097.mlab.com:3"
            "7097/_test_database_")
    patient = test_User(patient_id=1,
                        attending_email="rmc50@duke.edu",
                        user_age=20)
    patient.save()
    patient = test_User(patient_id=2,
                        attending_email="rmc50@duke.edu",
                        user_age=20)
    patient.save()
    patient = test_User(patient_id=3,
                        attending_email="rmc50@duke.edu",
                        user_age=20)
    patient.save()

    with pytest.raises(InputError):
        check_new_id(1)


def test_validate_post_heart_rate1():
    d = {
        "patient_id": 1,
    }
    with pytest.raises(ValidationError):
        validate_post_heart_rate(d)


def test_validate_post_heart_rate2():
    d = {
        "patient": 1,
        "heart_rate": 100
    }
    with pytest.raises(ValidationError):
        validate_post_heart_rate(d)


def test_check_id_exists():
    connect("mongodb://rebeccamcohen:bme590@ds037097.mlab.com:3"
            "7097/_test_database_")
    patient = test_User(patient_id=1,
                        attending_email="rmc50@duke.edu",
                        user_age=20)
    patient.save()
    patient = test_User(patient_id=2,
                        attending_email="rmc50@duke.edu",
                        user_age=20)
    patient.save()
    patient = test_User(patient_id=3,
                        attending_email="rmc50@duke.edu",
                        user_age=20)
    patient.save()

    with pytest.raises(InputError):
        check_id_exists(1000)


def test_validate_post_int_avg():
    d = {
        "patient_id": 1,
    }
    with pytest.raises(ValidationError):
        validate_post_int_avg(d)


def test_check_hr_since_list_empty():
    heart_rates_since = []
    with pytest.raises(NoHrSinceError):
        check_hr_since_list_empty(heart_rates_since)
