from compartment.Node import Node


class Compartment:
    node = None
    value = -1.0

    def __init__(self, node: Node, value: float):
        self.node = node
        self.value = value
