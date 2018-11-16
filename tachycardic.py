from database import User
from pymodm import connect
import logging

logging.basicConfig(filename="main_log.txt",
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)


def data_for_is_tach(patient_id):
    """

    Args:
        patient_id:

    Returns:

    """
    connect("mongodb://rebeccacohen:bme590@ds037768.mlab.com:37768/bme_590")
    p = User.objects.raw({"_id": patient_id}).first()
    recent_hr = p.heart_rate[-1]
    age = float(p.user_age)
    recent_time_stamp = p.time_stamp[-1]
    recent_time_str = str(recent_time_stamp)

    return age, recent_hr, recent_time_str


def is_tachycardic(age, recent_hr):  # age in years
    """

    Args:
        age:
        recent_hr:

    Returns:

    """

    if age < float(1 / 12):
        raise ValueError("Age must be greater "
                         "than or equal to 1/12 year (1 month)")
    if age >= float(1 / 12) and age < float(3 / 12):
        if recent_hr > 179:
            return 1
        else:
            return 0
    if age >= float(3 / 12) and age < float(6 / 12):
        if recent_hr > 186:
            return 1
        else:
            return 0
    if age >= float(6 / 12) and age < float(11 / 12):
        if recent_hr > 169:
            return 1
        else:
            return 0
    if age >= float(11/12) and age < 2:
        if recent_hr > 151:
            return 1
        else:
            return 0
    if age >= 2 and age < 4:
        if recent_hr > 137:
            return 1
        else:
            return 0
    if age >= 4 and age < 7:
        if recent_hr > 133:
            return 1
        else:
            return 0
    if age >= 7 and age < 11:
        if recent_hr > 130:
            return 1
        else:
            return 0
    if age >= 11 and age < 15:
        if recent_hr > 133:
            return 1
        else:
            return 0
    if age >= 15:
        if recent_hr > 100:
            return 1
        else:
            return 0
