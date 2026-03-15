def shift(plaintext, shift_value):
    shifted_text=""
    for i in plaintext :
        shifted_i = chr(ord(i) + shift_value)
        shifted_text +=shifted_i
    return shifted_text

def shift_int(int_list, shift_value):
    shifted_output = []
    for i in int_list:
        shifted_output.append(i + int(shift_value))
    return shifted_output

    
def unshift(plaintext, shift_value):
    unshifted_text=""
    for i in plaintext :
        unshifted_i = chr(ord(i) - shift_value)
        unshifted_text +=unshifted_i
    return unshifted_text


"""
shift_key = 5
message = "bonjour"
shifted_message=shift(message,shift_key)
print(shifted_message)
unshifted_message =unshift(shifted_message,shift_key)
print(unshifted_message)
"""