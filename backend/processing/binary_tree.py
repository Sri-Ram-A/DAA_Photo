from loguru import logger 

class TreeNode:
    def __init__(self, key:str, meta):
        self.key = key
        self.meta = meta
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key, meta):
        self.root = self._insert_recursive(self.root, key, meta)
        logger.success("Meta Data inserted in tree🌳")

    def _insert_recursive(self, node, key, meta):
        if not node:
            return TreeNode(key, meta,  )
        if key < node.key:
            node.left = self._insert_recursive(node.left, key, meta)
        else:
            node.right = self._insert_recursive(node.right, key, meta)
        return node

    def inorder_traversal(self, node=None):
        if node is None:
            node = self.root
        if node:
            self.inorder_traversal(node.left)
            print(f"Key: {node.key} ")
            self.inorder_traversal(node.right)
    
    def search(self, key):
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node, key):
        if node is None:
            return None
        if key == node.key:
            return node.meta
        elif key < node.key:
            return self._search_recursive(node.left, key)
        else:
            return self._search_recursive(node.right, key)

