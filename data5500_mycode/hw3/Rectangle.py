"""
1.    Create a class called Rectangle with attributes length and width. 
Implement a method within the class to calculate the area of the rectangle. 
Instantiate an object of the Rectangle class with length = 5 and width = 3, and print its area.

ChatGPT link: https://chatgpt.com/share/68ac9700-f200-8010-befe-d90a297704de
"""

# Class object for rectangle. 
class Rectangle:
    def __init__(self, length: float, width:float):
        if length <= 0 or width <= 0:
            raise ValueError("Length and width must be positive numbers.")
        self.length = length
        self.width = width
    
    # Calculate the area of a rectangle as length * width
    def area(self) -> float:
        return self.length * self.width

# Create a new rectangle with length = 5 and width = 3
r = Rectangle(5, 3)

# print the area
print("Area of the rectangle:", r.area())