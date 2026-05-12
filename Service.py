class Service:
    used_odu = 1
    _service_id = 0

    def __init__(self, rate, sd_pair, path_nodes = [], path_edges = []):
        Service._service_id += 1
        self._service_id = Service._service_id
        self.rate = rate
        self.sd_pair = sd_pair
        self.path_nodes = path_nodes
        self.path_edges = path_edges
        self.group_services = {}


    def __str__(self):
        return (f"Service(service_id={self._service_id}, "
                f"rate={self.rate}, "
                f"sd_pair={self.sd_pair}, "
                f"path_nodes={[node._node_id for node in self.path_nodes]}, "
                f"path_edges={self.path_edges}, "
                f"used_odu={self.used_odu})")