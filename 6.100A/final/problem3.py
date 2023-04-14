def uniqueValues(aDict):
    unique_list = []
    unique_values = []
    
    if aDict == {}:
        return unique_list
    
    for key in sorted(aDict):
        if aDict[key] not in unique_values:
            unique_values.append(aDict[key])
            unique_list.append(key)
        else:
            for item in unique_list:
                if aDict[item] == aDict[key]:
                    unique_list.remove(item)
                
    return unique_list
