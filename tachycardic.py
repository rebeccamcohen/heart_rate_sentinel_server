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
    if age >= (6 / 12) and age < (11 / 12):
        if recent_hr > 169:
            return 1
        else:
            return 0
    if age >= 11/12 and age < 2:
        if recent_hr > 151:
            return 1
        else:
            return 0
    if age >= 2 and age < 4:
        if recent_hr > 137:
            return 1
        else:
            return 0
    if age >= 4 and age < 7:
        if recent_hr > 133:
            return 1
        else:
            return 0
    if age >= 7 and age < 11:
        if recent_hr > 130:
            return 1
        else:
            return 0
    if age >= 11 and age < 15:
        if recent_hr > 133:
            return 1
        else:
            return 0
    if age >=15:
        if recent_hr > 100:
            return 1
        else:
            return 0



