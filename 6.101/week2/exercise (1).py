# Class exercise

# stubs of some lab 1/2 filters, just for demonstration 
def invert(image):
    print('inverting')
    return image

def make_blur(n):
    def blur(image):
        print(f'blur {n}')
        return image
    return blur

some_image = {'width': 0, 'height': 0, 'pixels': []}


def filter_cascade(filters):
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

# What gets printed by the following?
my_filters = [ invert, make_blur(3) ]
my_cascade = filter_cascade(my_filters)
my_cascade(some_image)

# And what gets printed by the following?
my_filters[0] = make_blur_filter(5)
my_cascade(some_image)
