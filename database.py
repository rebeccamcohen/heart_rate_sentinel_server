from pymodm import connect
from pymodm import MongoModel, fields

connect("mongodb://rebeccacohen:bme590@ds037768.mlab.com:37768/bme_590") # connect to database

class User(MongoModel):
    patient_id = fields.IntegerField()
    attending_email = fields.EmailField()
    user_age = fields.IntegerField()
    heart_rate = fields.IntegerField()
    time_stamp = fields.DateTimeField()

