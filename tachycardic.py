def is_tachycardic(age, recent_hr):  # age in years
    if age < (1 / 12):
        raise ValueError("Age must be greater than or equal to 1/12 year (1 month)")
    if age >= (1 / 12) and age < (3 / 12):
        if recent_hr > 179:
            return 1
        else:
            return 0
    if age >= (3 / 12) and age < (6 / 12):
        if recent_hr > 186:
            return 1
        else:
            return 0
    

