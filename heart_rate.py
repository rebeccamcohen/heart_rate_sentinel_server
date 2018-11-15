class ValidationError(Exception):
    def __init__(self, message):
        self.message = message


def validate_heart_rates_requests(heart_rates):
    if len(heart_rates) == 0:
        raise ValidationError("Specified patient exists in database, but there are no heart rate measurements")
