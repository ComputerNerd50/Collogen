def affine():
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    sent = input("Enter text to decode: ").lower()
    a = int(input("A term: "))
    b = int(input("B term: "))
    new = ""
    for i in sent:
        if i in alphabet :
            ind = alphabet.find(i)
            new += alphabet[(a*ind+b)%26]
        elif i == "," :
            new += ","
        else:
            new += " "
    print(new)

def caesar():
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    sent = input("Enter text to decode: ").lower()
    shift = int(input("Enter shift in alphabet. Negative number for translating sentence: "))
    new = ""
    for i in sent:
        if i in alphabet :
            ind = alphabet.find(i)
            if ind + shift > 26:
                i = alphabet[(ind + shift) - 27]
            else:
                i = alphabet[ind + shift]
            new += i
        elif i == "," :
            new += ","
        else:
            new += " "
    print(new)

affine()
            
