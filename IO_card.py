class IO_card:
    max_ports = 10
    _card_id = 0


    def __init__(self, node):
        self.node = node
        IO_card._card_id += 1
        self._id_counter = IO_card._card_id
        self.services = []
        self.used_ports = 0


    def add_service(self, service):
        if service.rate == 100:
            self.used_ports = self.max_ports
            self.services.append(service)

        elif service.rate == 10:
            self.used_ports += 1
            self.services.append(service)
            for serv in self.services:
                serv.group_services = {mate for mate in self.services if serv != mate}