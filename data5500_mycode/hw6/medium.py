'''
2. Given an array of integers, 
write a function that finds the second largest number in the array.

Analyze the time complexity of your solution using Big O notation, 
especially what is the Big O notation of the code you wrote, 
and include it in the comments of your program.
'''

# Chatgpt question:
# https://chatgpt.com/share/68b78f05-9b58-8010-be63-a0cfdf77e196

import random

# second_largest takes an array and finds the second-largest value in the array
# In case of two numbers that are the same and the largest, the largest number is also the second largest and is returned
# BIG O analaysis: The function loops over the entire array 1 time
# Time is O(n)
def second_largest(arr):
    if len(arr) < 2: 
        raise ValueError("Insufficient integers")

    # Set the largest and second largest values as the first and second elements
    if arr[0] > arr[1]:
        first, second = arr[0], arr[1]
    else:
        first, second = arr[1], arr[0]

    # Loop through the array to get the actual largest and smallest values
    for i in arr[2:]:
        if i > first:
            second = first
            first = i
        elif i > second:
            second = i
   
    return second


# Generate a random array
size = random.randint(2,20)
arr = [random.randint(0, 10000) for i in range(size)]

#test = [4384, 4950, 2842, 3352, 1721, 1520]
#print("Test:", second_largest(test))

# print the array and total
print("Array:", arr)
print("Second Largest:", second_largest(arr))