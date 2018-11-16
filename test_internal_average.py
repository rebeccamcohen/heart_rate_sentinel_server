from internal_average import data_for_internal_average
from internal_average import hr_since_specified_time


def test_hr_since_specified_time():
    d = 7
    time_stamps = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    hr_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    heart_rates_since = hr_since_specified_time(d, time_stamps, hr_list)
    expected = [8, 9, 10]

    assert heart_rates_since == expected
