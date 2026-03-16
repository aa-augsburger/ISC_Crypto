
def shift_int(int_list, shift_value):
    shifted_output = []
    for i in int_list:
        shifted_output.append(i + int(shift_value))
    return shifted_output

def unshift_int(int_list, shift_value):
    shifted_output = []
    for i in int_list:
        shifted_output.append(i-int(shift_value))
    return shifted_output




def decode_shift_int(int_list):
    output = []
    for s in range(25):
        shifted_list = unshift_int(int_list, s)
        output.append(shifted_list)
    return output


"""
shift_key = 5
message = "bonjour"
shifted_message=shift(message,shift_key)
print(shifted_message)
unshifted_message =unshift(shifted_message,shift_key)
print(unshifted_message)
"""