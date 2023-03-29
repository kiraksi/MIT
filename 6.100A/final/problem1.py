def isPalindrome(aString):
    aString_lower = aString.lower()
    if len(aString) <= 1:
        return True
    else:
        return aString_lower[0] == aString_lower[-1] and isPalindrome(aString[1:-1])
