def td(a, b):
    ta = a[0] * 3600 + a[1] * 60 + a[2]
    tb = b[0] * 3600 + b[1] * 60 + b[2]
    if ta > tb:
        tb += 86400
    tc = tb - ta
    print([int(tc / 3600), int(tc / 60) % 60, tc % 60])


td([3, 20, 40], [0, 0, 0])
td([20, 39, 20], [0, 0, 0])
td([1, 20, 45], [3, 20, 44])

# This code is terribly ugly and hard to understand.
# How would you improve it? - Improved by breaking up lines of code and using black
