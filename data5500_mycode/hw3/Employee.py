"""
2.  Create a class called Employee with attributes name and salary. 
Implement a method within the class that increases the salary of the employee by a given percentage. 
Instantiate an object of the Employee class with name = "John" and salary = 5000, 
increase the salary by 10%, and print the updated salary.

ChatGPT link: https://chatgpt.com/share/68ac9700-f200-8010-befe-d90a297704de
"""

# Employee class with name and salary
class Employee:
    def __init__ (self, name: str, salary: float):
        self.name = name
        if salary < 0:
            raise ValueError("Salary must be non-negative")
        self.salary = salary

    # Method to increase the salary
    # Increase is passed in as percent, not a decimal
    def increase_salary(self, increase : float) -> float:
        if increase < -100:
            raise ValueError("Percentage cannot reduce salary below 0")
        self.salary += increase/100 * self.salary
        return self.salary

# Create a new employee
e = Employee("John", 5000)
print(f"Current salary: {e.salary}")

# Increase the employee's salary and print the new salary
e.increase_salary(10)
print(f"New salary: {e.salary}")
