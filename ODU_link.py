class ODU_LINK:
    max_capacity = 100
    def __init__(self):
        self.services = []
        self.used_capacity = 0

    def add_service(self, client_service):
        if self.used_capacity + client_service.rate <= self.max_capacity:
            self.used_capacity += client_service.rate
            self.services.append(client_service)

        else:
            return KeyError