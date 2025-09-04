EXPECTED_BAKE_TIME =40

def bake_time_remaining(real_minutes):
    return EXPECTED_BAKE_TIME - real_minutes

def preparation_time_in_minutes(number_of_layers):
    return number_of_layers * 2
  
def elapsed_time_in_minutes(number_of_layers,elapsed_bake_time):
    return preparation_time_in_minutes(number_of_layers) + elapsed_bake_time

print(elapsed_time_in_minutes(3,20))