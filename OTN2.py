from Node import Node
from IO_card import IO_card
from ODU2 import ODU2
from math import ceil

class OTN2(Node):

    grooming = False


    def __init__(self):
        super().__init__()
        self.max_capacity = 12000
        self.node_type = 'OTN2'
        self.io_cards = []
        self.num_transponders = 0
        self.odu2s = []
        self.links = []
        self.services = []
        self.serv1 = False
        self.serv2 = False



    def compute_transponders(self):
        self.num_transponders = 0
        for link in self.links:
            self.num_transponders += ceil(link.used_odus/5)


    def capacity_overflow(self):
        self.used_capacity = 0
        self.compute_transponders()
        self.used_capacity += len(self.io_cards) * 100 # the capacity used by io cards
        self.used_capacity += self.num_transponders * 500 # the capacity used by transponders
        if self.used_capacity > self.max_capacity:
            return False

    def ODU_overflow(self):
        self.used_odus = len(self.odu2s)
        if self.used_odus > self.max_odus:
            return False


    def add_link(self, link):
      # here we want to add a link between two nodes to build the topology
      if self.used_capacity + 500 <= self.max_capacity:
        #self.used_capacity += self.transponders * 500
        self.used_ports += 1
        self.links.append(link)
      else:
        return KeyError


    def add_electrical_connection(self):
        # here we want to add a connection between OTN1 and OTn2 to take the client service to level2
        if self.used_capacity + 100 <= self.max_capacity:
            new_io = IO_card(node=self._node_id)
            self.used_capacity += 100
            self.num_io_cards += 1
            self.used_ports += 1
            self.io_cards.append(new_io)
            return new_io

        else:
            return KeyError




    def service_grouping(self):
      self.odu2s.clear()  # Properly clear existing ODU2s

      visited = set()

      for service in self.services:
          if service not in visited:
              group = set()
              stack = [service]  # Use a stack for explicit grouping

              while stack:
                  current = stack.pop()
                  if current not in visited:
                      visited.add(current)
                      group.add(current)
                      # Add only explicitly defined `group_services`
                      stack.extend(mate for mate in current.group_services if mate not in visited)

              # Create a new ODU2 and assign the grouped services
              odu2 = ODU2()
              for serv in group:
                  odu2.add_service(serv)
              self.odu2s.append(odu2)  # Store the grouped services ODU2





    def apply_grooming(self):
        for odu2 in self.odu2s:
            del odu2
        self.odu2s.clear()

        for service in self.services:
            odu2 = ODU2()
            self.odu2s.append(service)





    def add_service(self, client_service):
            service_add = False
            if self.max_capacity <= self.used_capacity + client_service.rate:
                return KeyError
            # first we sould decide wether the service is from IO card or transponder
            matching_index = [index for index, node in enumerate (client_service.path_nodes) if self._node_id == node._node_id]
            if client_service.path_nodes[matching_index[0] - 1].node_type == 'OTN1':
                if client_service.rate == 10:
                  if self.io_cards != []:
                    for io_card in self.io_cards:
                        if io_card.used_ports < io_card.max_ports:
                            # add service to the existing io card
                            io_card.add_service(client_service)
                            service_add = True
                            break
                        else:
                          return KeyError
                  elif self.num_io_cards < self.max_ports:
                    new_io = self.add_electrical_connection()# create a new io card
                    new_io.add_service(client_service)
                    service_add = True
                  else:
                    return KeyError

                elif client_service.rate == 100:
                    new_io = self.add_electrical_connection()
                    new_io.add_service(client_service)
                    service_add = True


            if service_add == True:
                self.services.append(client_service)
                self.num_services += 1

            else:
                self.services.append(client_service)
                self.num_services += 1
                service_add = True

            if not self.grooming:
                self.service_grouping()
            if self.grooming:
                self.apply_grooming()
            # now we check the constraints for capacity and ODU if it was not ok we remove the service
            if self.capacity_overflow() or self.ODU_overflow():
                self.services.remove(client_service)
                service_add = False


            if not service_add:
                return KeyError

