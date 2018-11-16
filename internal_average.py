from database import User
from pymodm import connect
import logging

logging.basicConfig(filename="main_log.txt",
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)


def data_for_internal_average(patient_id):
    connect("mongodb://rebeccacohen:bme590@ds037768.mlab.com:37768/bme_590")
    p = User.objects.raw({"_id": patient_id}).first()
    time_stamps = p.time_stamp
    hr_list = p.heart_rate

    return time_stamps, hr_list


def hr_since_specified_time(d, time_stamps, hr_list):
    heart_rates_since = []
    for item in time_stamps:
        if item > d:
            index = time_stamps.index(item)
            heart_rates_since.append(hr_list[index])

    return heart_rates_since
