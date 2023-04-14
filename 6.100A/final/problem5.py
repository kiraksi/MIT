class myDict(object):
    """ Implements a dictionary without using a dictionary """
    def __init__(self):
        """ initialization of your representation """
        #FILL THIS IN
        self.__dict__ = {}
        
    def assign(self, k, v):
        """ k (the key) and v (the value), immutable objects  """
        self.__dict__[k] = v
        
    def getval(self, k):
        """ k, immutable object  """
        return self.__dict__[k]
        
    def delete(self, k):
        """ k, immutable object """   
        #FILL THIS IN
        del self.__dict__[k]
