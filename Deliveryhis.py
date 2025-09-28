class DelRouteNode:
    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination
        self.left = None
        self.right = None

    def __str__(self):
        return f"{self.origin} -> {self.destination}"


class DelHistory:
    def __init__(self):
        self.root = None

    def _compare(self, route1, route2):
        return (route1.origin + route1.destination) < (route2.origin + route2.destination)

    def insert(self, origin, destination):
        new_node = DelRouteNode(origin, destination)
        if not self.root:
            self.root = new_node
        else:
            self._insert_recursive(self.root, new_node)

    def _insert_recursive(self, current, new_node):
        if self._compare(new_node, current):
            if current.left:
                self._insert_recursive(current.left, new_node)
            else:
                current.left = new_node
        else:
            if current.right:
                self._insert_recursive(current.right, new_node)
            else:
                current.right = new_node

    def inorder_traversal(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(str(node))
            self._inorder(node.right, result)


def DelRecords(history_tree, origin, destination, status):
    if status.lower() == "completed":
        history_tree.insert(origin, destination)
