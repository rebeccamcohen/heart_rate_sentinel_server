from pymodm import MongoModel, fields


class User(MongoModel):
    patient_id = fields.IntegerField(primary_key=True)
    attending_email = fields.EmailField()
    user_age = fields.FloatField()
    time_stamp = fields.DateTimeField()
    heart_rate = fields.ListField(field=fields.IntegerField())
    time_stamp = fields.ListField(field=fields.DateTimeField())
