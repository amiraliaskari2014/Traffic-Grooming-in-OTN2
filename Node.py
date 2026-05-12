class Node:

    max_ports = 70
    max_odus = 100
    _node_id = 0

    def __init__(self):
        Node._node_id += 1
        self._node_id = Node._node_id
        self.max_capacity = 0
        self.num_io_cards = 0
        self.used_capacity = 0
        self.used_ports = 0
        self.used_odus = 0
        self.num_services = 0
        self.node_type = ''

    def __str__(self):
        return (f"Node(node_id = {self._node_id}, "
                f"node_type = {self.node_type}, "
                f"max_capacity={self.max_capacity}, "
                f"used_capacity={self.used_capacity}, "
                f"used_ports={self.used_ports}/{self.max_ports}, "
                f"used_odus={self.used_odus}/{self.max_odus}, "
                f"num_services={self.num_services}, "
                f"num_io_cards={self.num_io_cards})")