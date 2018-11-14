class ValidationError(Exception):
    def __init__(self, message):
        self.message = message


REQUIRED_REQUEST_KEYS = [
    "patient_id",
    "attending_email",
    "user_age",
]


def validate_new_patient_request(req):
    for key in REQUIRED_REQUEST_KEYS:
        if key not in req.keys():
            raise ValidationError(
                "Key '{0}' not present in request".format(key))
