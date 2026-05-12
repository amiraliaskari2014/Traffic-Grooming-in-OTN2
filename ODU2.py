class ODU2:
    _odu_id = 0
    max_capacity = 100

    def __init__(self):
        ODU2._odu_id += 1
        self._odu_id = ODU2._odu_id
        self.services = []
        self.used_capacity = 0
        self.services_rate = 0


    def add_service(self, service):
        if self.used_capacity + service.rate <= self.max_capacity:
            self.services.append(service)
            self.used_capacity += service.rate
            self.services_rate = service.rate

    def __del__(self):
        pass