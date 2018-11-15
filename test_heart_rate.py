import pytest
from heart_rate import validate_heart_rates_requests, ValidationError


def test_validate_heart_rate_requests():
    heart_rates = []
    with pytest.raises(ValidationError):
        validate_heart_rates_requests(heart_rates)
