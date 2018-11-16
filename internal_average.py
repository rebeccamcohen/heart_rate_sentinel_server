from database import User
from pymodm import connect
import logging

logging.basicConfig(filename="main_log.txt",
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)


def data_for_internal_average(patient_id):
    """Finds required data in database for specified user

    Args:
        patient_id (int): Specified patient id

    Returns:
        time_stamps (list): All time stamps associated with patient id
        hr_list (list): All heart rate measurements
        associated with patient id

    """
    connect("mongodb://rebeccacohen:bme590@ds037768.mlab.com:37768/bme_590")
    p = User.objects.raw({"_id": patient_id}).first()
    time_stamps = p.time_stamp
    hr_list = p.heart_rate

    return time_stamps, hr_list


def hr_since_specified_time(d, time_stamps, hr_list):
    """Finds list of heart rate measurements since specified time

    Args:
        d (datetime.datetime): Specified time stamp
        time_stamps (list): All time stamps associated with patient id
        hr_list:  hr_list (list): All heart rate measurements
        associated with patient id

    Returns:
        heart_rates_since (list): List of heart rate
        measurements since specified time

    """
    heart_rates_since = []
    for item in time_stamps:
        if item > d:
            index = time_stamps.index(item)
            heart_rates_since.append(hr_list[index])

    return heart_rates_since
