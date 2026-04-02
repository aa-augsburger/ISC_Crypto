def ints_to_string(int_list):
    output = ""
    for num in int_list:
        try:
            num_bytes = num.to_bytes(4, byteorder='little')
            num_bytes = num_bytes.rstrip(b'\x00')
            output += num_bytes.decode('utf-8')
        except ValueError:
            output += '*'
    return output

def frequential_analysis(ints_list):

    encoded = ints_to_string(ints_list)
    encoded.lower()

    frequences_caracteres = [

    ]

    for c in encoded:
        print(c)






