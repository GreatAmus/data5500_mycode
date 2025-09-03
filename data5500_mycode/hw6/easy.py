'''
1. Given an array of integers, write a function to calculate the sum of all elements in the array.

Analyze the time complexity of your solution using Big O notation, 
especially what is the Big O notation of the code you wrote, and include it in the comments of your program.
###
'''


import random 

# sum_integer takes a list of integeres and sums up the array
# returns 0 if the array is empty
# Time complexity is O(n) as there is a single loop over the entire array
def sum_integers(arr):     
    total = 0
    for i in arr:
        total += i
    return total


# Generate a random array
size = random.randint(2,20)
arr = [random.randint(0,100) for i in range(size)]

# print ("Test:", sum_integers([]))
# print the array and total
print("Array:", arr)
print("Sum:", sum_integers(arr))

