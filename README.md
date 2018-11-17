# heart_rate_sentinel_server

**Python files:**
- server.py: main python file (contains flask server)
- database.py: creates the class User for the database
- tachycardic.py: contains functions to calculate whether patient is tachycardic
- sendgrid_email.py: contains functions to send email
- validation.py: contains functions to validate data 
- test files: contains unit tests for functions 


**To add a new patient:**
- will not be able to add a user with a patient_id that already exists 
- will only be able to add a new user with all of the specified keys
r = requests.post("http://vcm-7437.vm.duke.edu:5000/api/new_patient", json={"patient_id": 1, "attending_email": "rmc50@duke.edu", "user_age": 21})   

**To add heart rate measurements associated with a given patient id:**
- will not be able to post a heart rate if the user_id does not exist 
- each time a heart rate is posted, whether or not the patient is tachycardic is determined.
- if the patient is tachycardic, an email will be sent
r = requests.post("http://vcm-7437.vm.duke.edu:5000/api/heart_rate", json={"patient_id": 1, "heart_rate": 100})   

**To get the status of a patient (to determine whether a patient is tachycardic based on previously available heart rate):**
- also returns the timestamp of most recent heart rate
r = requests.get("http://vcm-7437.vm.duke.edu:5000/api/status/2")

**To get all the previous heart rate measurements of a specified patient:**
- will not be able to calculate if patient id does not exist
r = requests.get("http://vcm-7437.vm.duke.edu:5000/api/heart_rate/2")

**To get the average of all the previous heart rate measurements of a specified patient:**
- will not be able to calculate if patient id does not exist
r = requests.get("http://vcm-7437.vm.duke.edu:5000/api/heart_rate/average/2")

**To calculate the internal average:**
- will not be able to calculate if patient id does not exist
- will not be able to calculate if there are no heart rate measurements since the specified time stamp
r = requests.post("http://vcm-7437.vm.duke.edu:5000/api/heart_rate/internal_average", json={"patient_id": 1, "heart_rate_average_since": "2018-03-09 11:00:36.372339" })   
