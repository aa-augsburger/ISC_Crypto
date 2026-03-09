def shift(plaintext, shift_value):
    shifted_text=""
    for i in plaintext :
        shifted_i = chr((ord(i) + shift_value)%128)
        shifted_text +=shifted_i
    return shifted_text    

    
def unshift(plaintext, shift_value):
    unshifted_text=""
    for i in plaintext :
        unshifted_i = chr((ord(i) - shift_value)%128)
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