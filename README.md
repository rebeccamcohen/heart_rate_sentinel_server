# heart_rate_sentinel_server

**To add a new patient:**
- will not be able to add a user with a patient_id that already exists 
- will only be able to add a new user with all of the specified keys

r = requests.post("http://vcm-7437.vm.duke.edu:5000/api/new_patient", json={"patient_id": 1, "attending_email": "rmc50@duke.edu", "user_age": 21})   



**To add heart rate measurements associated with a given patient id:**
- will not be able to post a heart rate if the user_id does not exist 
- each time a heart rate is posted, whether or not the patient is tachycardic is determined.
- if the patient is tachycardic, an email will be sent
r = requests.post("http://vcm-7437.vm.duke.edu:5000/api/heart_rate", json={"patient_id": 1, "heart_rate": 100})   

