# Given the definition of the Rectangle class, complete the definition
# of the Square class by only implementing its __init__ method.

class Rectangle(Shape):
    def __init__(self, color, lower_left, upper_right):
        super().__init__(color)  # or Shape.__init__(self, color)
        self.lower_left = lower_left    # tuple (x, y)
        self.upper_right = upper_right  # tuple (x, y)
        self.bbox = BoundingBox(
            lower_left[0], upper_right[0],  # min_x, max_x
            lower_left[1], upper_right[1]   # min_y, max_y
        )

    def __contains__(self, item):
        return ( item[0] >= self.lower_left[0] and item[0] <= self.upper_right[0] and
                 item[1] >= self.lower_left[1] and item[1] <= self.upper_right[1] )

    def center(self):
        return ( (self.lower_left[0] + self.upper_right[0]) / 2,
                 (self.lower_left[1] + self.upper_right[1]) / 2 )

    def __repr__(self):
        return f"Rectangle({self.lower_left}, {self.upper_right})"


class Square(Rectangle):
    def __init__(self, color, mid, side):
        ...


    
