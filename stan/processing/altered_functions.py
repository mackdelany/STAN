def impute_airway(airway): #to airway_altered
    if airway == 'OTHER':
        return True
    return False

def impute_breathing(breathing): #to breathing_altered
    if breathing == 'OTHER':
        return True
    return False

def impute_circulation(circulation): #to breathing_altered
    if circulation == 'ALTERED':
        return True
    return False

def impute_disability_gcs(disability_gcs): #to breathing_altered
    if disability_gcs == 'A':
        return 15
    if disability_gcs == 'V':
        return 12
    if disability_gcs == 'P':
        return 9
    if disability_gcs == 'U':
        return 6
    # else impute to A
    return 15

def impute_neuro(neuro): #to breathing_altered
    if neuro == 'OTHER':
        return True
    return False

def impute_mental(mental):
    if mental == 'YES':
        return True
    return False