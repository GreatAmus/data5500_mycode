'''
2. Implement a Python function to search for a value in a binary search tree. 
The method should take the root of the tree and the value to be searched as parameters. 
It should return True if the value is found in the tree, and False otherwise.
'''
from print_tree import  *

# Nodes of the tree as a class object
# Node branches left for smaller keys and right for larger keys
class Node:

	# Constructor to create a new node
	def __init__(self, key):
		self.key = key
		self.left = None
		self.right = None

# Insert a new node in the tree
# Takes a node value and key, then recursivly traces down the key until it finds an open spot
# Move left if the key is lower than the current node and right if higher
def insert(node, key):
    if node is None:            # empty spot in tree - insert key - base case
        return Node(key)
    elif key <= node.key:       # key is less than current node so shift left
        node.left = insert(node.left, key)
    else:                       # key is more than current node so shift right
        node.right = insert(node.right, key)
    return node

# find a specific key in the tree
# takes a node and key as input and returns True if found and False if not found
def find(node, key):
    if node is None:        # Node is empty so the value does not exist in the tree - base case 1
        return False
    elif node.key == key:   # Node matches the key so the value is found - base case 2
        return True
    elif node.key > key:    # Node is more than the key so shift left
        return find(node.left, key)
    else:                   # Node is less than the key so shift right
        return find(node.right, key)

    
root = Node(11)
insert(root,14)
insert(root,3)
insert(root,7)
insert(root,26)

val = int(input("What key would you like to find? "))
print("Result:", find(root, val))


