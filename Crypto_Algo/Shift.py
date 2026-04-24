

def shift_int(int_list, shift_value):
    shifted_output = []
    for i in int_list:
        shifted_output.append(i + int(shift_value))
    return shifted_output

#fonctions pour shifter les lettre sur une liste d'entier, permet de gérer les caractères hors ascii

def unshift_int(int_list, shift_value):
    shifted_output = []
    for i in int_list:
        shifted_output.append(i-int(shift_value))
    return shifted_output




def decode_shift_int(int_list):
    output = []
    for s in range(26):
        shifted_list = unshift_int(int_list, s)
        output.append(shifted_list)
    return output

#fonction pour trouver la clé
def key_finder(int_list):
    count_letter = {}
    clean_int_list = []
    #on nettoie la liste recu pour ne tenir compte que des lettres
    for i in int_list:
        if (65 <= i <= 90) or (97 <= i <= 122):
            if i > 97: #on met les lettres en minuscules
                i = i-32
            clean_int_list.append(i) #on ajoute la lettre dans le tableau nettoye
            count_letter[i] = count_letter.get(i,0)+1 #on compte le nombre d'occurence

    lettre_max = ""
    nb_max = 0
    #on cherche la letter qui qui apparait le plus de fois
    for letter, nb_letter in count_letter.items():
        if nb_letter > nb_max:
            nb_max = nb_letter
            lettre_max = letter
    guessed_shift = (lettre_max - 69) % 26 #valeur du E
    return guessed_shift



"""
shift_key = 5
message = "bonjour"
shifted_message=shift(message,shift_key)
print(shifted_message)
unshifted_message =unshift(shifted_message,shift_key)
print(unshifted_message)
"""