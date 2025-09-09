''' 
Write a Python function to insert a value into a binary search tree. 
The function should take the root of the tree and the value to be inserted as parameters.
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


root = Node(11)
insert(root,14)
insert(root,3)
insert(root,7)
insert(root,26)
display(root)

