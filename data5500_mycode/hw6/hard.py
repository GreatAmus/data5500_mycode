'''
3. Write a function that takes an array of integers as input and returns 
the maximum difference between any two numbers in the array.

Analyze the time complexity of your solution using Big O notation, 
especially what is the Big O notation of the code you wrote, 
and include it in the comments of your program.

'''
# Chatgpt question:
# https://chatgpt.com/share/68b78f05-9b58-8010-be63-a0cfdf77e196

import random

# maximum_difference takes an array and finds the maximum difference between the two numbers
# I find the largest and smallest number and compare those two
# if there is one number then 0 is returned
# BIG O analysis: There is a single loop over the array
# The single loop makes the time O(n)
def maximum_difference(arr):
    if len(arr) < 2: 
        return 0

    # Set the largest and smallest values as the first and second elements
    if arr[0] > arr[1]:
        largest, smallest = arr[0], arr[1]
    else:
        largest, smallest = arr[1], arr[0]

    # Loop through the array to find the actual largest and smallest values
    for i in arr[2:]:
        if i > largest:
            largest = i
        elif i < smallest:
            smallest = i
   
    return largest-smallest


# Generate a random array
size = random.randint(2,10)
arr = [random.randint(0, 10) for i in range(size)]

# print the array and total
print("Array:", arr)
print("Max Difference:", maximum_difference(arr))