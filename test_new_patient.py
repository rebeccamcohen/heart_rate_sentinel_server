from server import get_new_patient
from new_patient import validate_new_patient_request
from new_patient import ValidationError
import pytest


def test_get_new_patient1():
    new_patient = {
        "attending_email": "rebecca.cohen@duke.edu",
    }
    with pytest.raises(ValidationError):
        validate_new_patient_request(new_patient)


def test_get_new_patient2():
    new_patient = {
        "patient_id": 1,
        "attending_email": "rebecca.cohen@duke.edu",
        "age": 20
    }

    with pytest.raises(ValidationError):
        validate_new_patient_request(new_patient)
