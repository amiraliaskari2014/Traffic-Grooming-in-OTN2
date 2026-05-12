from Node import Node
from IO_card import IO_card

class OTN1(Node):
    def __init__(self):
        super().__init__()
        self.max_capacity = 1200
        self.node_type = 'OTN1'
        self.io_cards = []



    def check_constraints(self, client_service):
        service_add = False
        if self.used_odus < self.max_odus and self.used_capacity + client_service.rate <= self.max_capacity:
            # then the port constraint
            if client_service.rate == 10:
              if self.io_cards != []:
                for io_card in self.io_cards:
                    if io_card.used_ports < io_card.max_ports:
                        # add service to the existing io card
                        service_add = True
                        return io_card, 0
                    else:
                      new_io = IO_card(node=self._node_id)# create a new io card
                      self.num_io_cards += 2
                      self.used_ports += 2
                      new_io.add_service(client_service)
                      self.io_cards.append(new_io)
                      service_add = True
                      return new_io, 1

              elif self.num_io_cards < self.max_ports:
                new_io = IO_card(node=self._node_id)# create a new io card.
                self.num_io_cards += 2
                self.used_ports += 2
                new_io.add_service(client_service)
                self.io_cards.append(new_io)
                service_add = True
                return new_io, 1

              else:
                return service_add,0

            elif not service_add and self.num_io_cards < self.max_ports and client_service.rate == 100:
                # here all the constraints are checked and the service will be added
                new_io = IO_card(node=self._node_id)# create a new io card
                self.num_io_cards += 2
                self.used_ports += 2
                new_io.add_service(client_service)
                self.io_cards.append(new_io)
                service_add = True
                return new_io, 1

            else:
                return service_add,0
        else:
            return service_add,0




    def add_service(self, client_service):
        # we have a new service on OTN1 => first we check the constraints =>
        io_card, is_new= self.check_constraints(client_service)
        if io_card:
            io_card.add_service(client_service)
            self.used_odus += 1
            if is_new:
                self.used_capacity += 200
            #self.used_capacity += client_service.rate
            self.num_services += 1
            return True
        else:
            return False