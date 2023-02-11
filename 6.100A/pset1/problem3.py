# Assume s is a string of lower case characters.
# Write a program that prints the longest substring of s in which the letters occur in alphabetical order. For example, if s = 'azcbobobegghakl', then your program should print (in case of ties print first substring): "Longest substring in alphabetical order is: beggh"

def alpha_order():

    alpha_string = ""
    check_string = ""
    
    for i in range (len(s)-1):
        if s[i] > s[i+1]:
            alpha_string += s[i]
            if len(alpha_string) > len(check_string):
                check_string = alpha_string
            alpha_string = ""
        else:
            alpha_string += s[i]
            if i== len(s) - 2:
                alpha_string += s[i+1]

    if(len(alpha_string) > len(check_string)):
        print("Longest substring in alphabetical order is:", alpha_string)
    else:
        print("Longest substring in alphabetical order is:", check_string)

alpha_order()
