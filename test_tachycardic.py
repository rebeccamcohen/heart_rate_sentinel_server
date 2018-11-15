from tachycardic import is_tachycardic
import pytest


@pytest.mark.parametrize("age,recent_hr,expected", [
    (1/12, 180, 1),
    (1/12, 179, 0),
    (2/12, 160, 0),
    (2/12, 190, 1),
    (0.15, 200, 1),
    (0.09, 183, 1),
    (3/12, 186, 0),
    (0.41, 199, 1),
    (0.2, 190, 1)

])
def test_is_tachycardic_parametrize(age, recent_hr, expected):
    assert is_tachycardic(age, recent_hr) == expected


def test_is_tachycardic_validate_age():
    age = 0.08
    recent_hr = 180
    with pytest.raises(ValueError):
        is_tachycardic(age, recent_hr)