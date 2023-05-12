# 6.101 recitation: image_processing_2 wrapup
# Spring 2023

# stubs of some lab 1/2 filters, just for demonstration 
def invert(image):
    print('invert')
    return image

def make_blur(n):
    def blur(image):
        print(f'blur {n}')
        return image
    return blur

some_image = {'width': 0, 'height': 0, 'pixels': []}



################### higher-order functions

def filter_cascade1(filters):
    """Given a list of filters (implemented as functions on images),
    returns a new single filter such that applying that filter to an
    image produces the same output as applying each of the individual
    ones in turn.
    """
    def cascade(image):
        for f in filters:
            image = f(image)
        return image
    return cascade

# What gets printed by:
my_filters = [ invert, make_blur(3) ]
my_cascade = filter_cascade1(my_filters)
my_cascade(some_image)

# What if we mutate the filters list after creating the cascade?
# Now what gets printed? Why?
my_filters[0] = make_blur(5)
my_cascade(some_image)



## how does this version behave if filters is mutated later?
def filter_cascade2(filters):
    def cascade(image):
        for f in filters.copy():
            image = f(image)
        return image
    return cascade

my_filters = [ invert, make_blur(3) ]
my_cascade = filter_cascade2(my_filters)
my_cascade(some_image)
print()
my_filters[0] = make_blur(5)
my_cascade(some_image)



## how does this version behave?
def filter_cascade3(filters):
    cascade = ___________ # fill in what goes here
    for f in filters:
        cascade = lambda image: f(cascade(image))
    return cascade


my_filters = [ invert, make_blur(3) ]
my_cascade = filter_cascade3(my_filters)
my_cascade(some_image)
print()
my_filters[0] = make_blur(5)
my_cascade(some_image)



## how does this version behave if filters is mutated later?
def filter_cascade4(filters):
    def compose(first, second):
        """Returns composite filter that applies first, then applies second"""
        return lambda image: second(first(image))

    cascade = lambda image: image
    for f in filters:
        cascade = compose(f, cascade)
    return cascade


my_filters = [ invert, make_blur(3) ]
my_cascade = filter_cascade4(my_filters)
my_cascade(some_image)
print()
my_filters[0] = make_blur(5)
my_cascade(some_image)

# How fix the bug?



## how does this version behave?
def filter_cascade5(filters):
    def cascade(image):
        while filters:
            f = filters.pop(0)
            image = f(image)
        return image
    return cascade


my_filters = [ invert, make_blur(3) ]
my_cascade = filter_cascade5(my_filters)
my_cascade(some_image)
print()
my_filters[0] = make_blur(5)
my_cascade(some_image)


#################### image_without_seam

# code review:
# what's good?
# what to improve?
# buggy?

def image_without_seam(image, seam):
    """Given a (color) image and a list of indices to be removed from the
    image, return a new image (without modifying the original) that
    contains all the pixels from the original image except those
    corresponding to the locations in the given list.
    """
    pixels = image['pixels']
    for index in seam:
        pixels.pop(index)  # or: del pixels[index]

    return {
        'width': image['width'] - 1,
        'height': image['height'],
        'pixels': pixels,
    }

inp = { 'width': 2, 'height': 2, 'pixels': [ 0, 51, 0, 52 ] }
out = image_without_seam(inp, [0, 2])  # remove zero's at idx 0 & 2



## how about this version?

def image_without_seam(image, seam):
    """Given a (color) image and a list of indices to be removed from the
    image, return a new image (without modifying the original) that
    contains all the pixels from the original image except those
    corresponding to the locations in the given list.
    """
    new_pixels = image['pixels'].copy()

    # remove the specified pixels in decreasing order of index, so
    # that removing a pixel doesn't change any of the indices we still
    # have to remove
    for index in reversed(sorted(seam)):
        del new_pixels[index]

    return {
        'width': image['width'] - 1,
        'height': image['height'],
        'pixels': new_pixels,
    }

inp = { 'width': 2, 'height': 2, 'pixels': [ 0, 51, 0, 52 ] }
out = image_without_seam(inp, [0, 2])  # remove zero's at idx 0 & 2



## functional-programming approach -- don't mutate anything, just create a new thing
def image_without_seam(image, seam):
     return {'width': image['width'] - 1,
             'height': image['height'],
             'pixels': [pixel
                        for index, pixel in enumerate(image['pixels'])
                        if index not in seam]}

inp = { 'width': 2, 'height': 2, 'pixels': [ 0, 51, 0, 52 ] }
out = image_without_seam(inp, [0, 2])  # remove zero's at idx 0 & 2



## faster! membership test (index not in seam) is much faster when
## seam is a set rather than a list
def image_without_seam(image, seam):
    seam_set = set(seam)
    return { 'width': image['width']-1,
             'height': image['height'],
             'pixels': [pixel
                        for index, pixel in enumerate(image['pixels'])
                        if index not in seam_set]}

inp = { 'width': 2, 'height': 2, 'pixels': [ 0, 51, 0, 52 ] }
out = image_without_seam(inp, [0, 2])  # remove zero's at idx 0 & 2


