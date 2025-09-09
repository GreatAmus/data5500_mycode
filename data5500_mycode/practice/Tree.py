class Node:

	# Constructor to create a new node
	def __init__(self, key):
		self.key = key
		self.left = None
		self.right = None

class Tree:

	def __init__(self):
		self.__root = None

	@property
	def root(self):
		return self.__root

	@root.setter
	def root(self, node):
		self.__root = node

	def insert(self, node, key):
		if node is None:
			node = Node(key)
			if self.root is None:
				self.root = node
			return node
		elif node.key <= key:
			node.left = self.insert(node.left, key)
		else:
			node.right = self.insert(node.right, key)
