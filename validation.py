from database import User
from pymodm import connect


class ValidationError(Exception):
    def __init__(self, message):
        self.message = message


class InputError(Exception):
    def __init__(self, message):
        self.message = message


class EmptyHrListError(Exception):
    def __init__(self, message):
        self.message = message


class UserDoesNotExistError(Exception):
    def __init__(self, message):
        self.message = message


class NoHrSinceError(Exception):
    def __init__(self, message):
        self.message = message


REQUIRED_REQUEST_KEYS_NEW_PATIENT = [
    "patient_id",
    "attending_email",
    "user_age",
]

REQUIRED_REQUEST_KEYS_POST_HEART_RATE = [
    "patient_id",
    "heart_rate",
]

REQUIRED_REQUEST_KEYS_POST_INTERNAL_AVERAGE = [
    "patient_id",
    "heart_rate_average_since",
]


def validate_new_patient(req):
    for key in REQUIRED_REQUEST_KEYS_NEW_PATIENT:
        if key not in req.keys():
            raise ValidationError(
                "Key '{0}' not present in request".format(key))


def check_new_id(patient_id):
    connect("mongodb://rebeccacohen:bme590@ds037768.mlab.com:37768/bme_590")
    my_id = patient_id
    all_ids = []
    all_patients_in_db = User.objects.raw({})
    for user in all_patients_in_db:
        all_ids.append(user.patient_id)

    for item in all_ids:
        if item == my_id:
            raise InputError("User '{}' already exists".format(patient_id))


def validate_post_heart_rate(req):
    for key in REQUIRED_REQUEST_KEYS_POST_HEART_RATE:
        if key not in req.keys():
            raise ValidationError(
                "Key '{0}' not present in request".format(key))


def check_list_empty(patient_id):
    connect("mongodb://rebeccacohen:bme590@ds037768.mlab.com:37768/bme_590")
    p = User.objects.raw({"_id": patient_id}).first()
    hr_list = p.heart_rate
    if len(hr_list) == 0:
        raise EmptyHrListError("No heart rate "
                               "measurements exist for "
                               "patient {0}".format(patient_id))


def check_id_exists(patient_id):
    connect("mongodb://rebeccacohen:bme590@ds037768.mlab.com:37768/bme_590")

    my_id = patient_id
    all_ids = []
    all_patients_in_db = User.objects.raw({})
    for user in all_patients_in_db:
        all_ids.append(user.patient_id)

    if my_id not in all_ids:
        raise InputError("User '{0}' does not exist".format(patient_id))


def validate_post_int_avg(req):
    for key in REQUIRED_REQUEST_KEYS_POST_INTERNAL_AVERAGE:
        if key not in req.keys():
            raise ValidationError("Key '{0}' not "
                                  "present in request".format(key))


def check_hr_since_list_empty(heart_rates_since):
    if len(heart_rates_since) == 0:
        raise NoHrSinceError("No heart rate measurements "
                             "exist since specified time stamp")
