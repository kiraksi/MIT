def keysWithValue(aDict, target):
    '''
    aDict: a dictionary
    target: an integer
    '''
    values = aDict.values()
    newList = []

    if target not in values:
        return newList
    else:
        for key, value in aDict.items():
            if value == target:
                newList.append(key)
        return sorted(newList)
