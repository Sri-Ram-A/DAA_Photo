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
    
    def visualize(self, filename="bst"):
        from graphviz import Digraph
        dot = Digraph(comment='Binary Search Tree')
        self._add_nodes_edges(self.root, dot)
        dot.render(f'{filename}.gv', view=True)
        print(f"✅ BST visualization saved to {filename}.gv.pdf ")
        return filename+".gv"+".pdf"

    def _add_nodes_edges(self, node, dot, parent_key=None):
        if node:
            # Create a label string showing key and meta data nicely
            meta_text = "\\n".join(f"{k}: {v}" for k, v in node.meta.items())
            label = f"{node.key}\\n{meta_text}"
            # Add node
            dot.node(node.key, label)
            # Add edge from parent to this node
            if parent_key:
                dot.edge(parent_key, node.key)
            # Recurse left and right
            self._add_nodes_edges(node.left, dot, node.key)
            self._add_nodes_edges(node.right, dot, node.key)

    