from random import randint

'''
Necessary properties of node

node.terminal: return true if the node is a final node (if it has no children
node.value: returns the value of the node (this is what we are maximizing)
node.__iter__: returns the children of the node
'''


class NodeExample:
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def __iter__(self):
        return iter(self.children)

    @property
    def terminal(self):
        return len(self.children) == 0


def create_tree(n, d, x):
    if n == 1:
        return NodeExample(randint(0, d), tuple())
    children = tuple(create_tree(n-1, d, x) for _ in range(x))
    tree = NodeExample(None, children)
    return tree


def alphabeta(node, depth, a=float('-inf'), b=float('inf'), maximizingPlayer=True):
    if depth == 0 or node.terminal:  # is a terminal node
        return node.value
    if maximizingPlayer:
        v = float('-inf')
        for child in node:
            v = max(v, alphabeta(child, depth - 1, a, b, False))
            a = max(a, v)
            if b <= a:
                break  # b cut-off
        return v
    else:
        v = float('inf')
        for child in node:
            v = min(v, alphabeta(child, depth - 1, a, b, True))
            b = min(b, v)
            if b <= a:
                break  # a cut-off
        return v
