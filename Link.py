from ODU2 import ODU2
from ODU_link import ODU_LINK
from math import ceil

class Link:
    _link_id = 0
    grooming = False



    def __init__(self, starting_node, ending_node):
        Link._link_id += 1
        self._link_id = Link._link_id
        self.starting_node = starting_node
        self.ending_node = ending_node
        self.used_odus = 0
        self.odu2s = []
        self.services = []
        self.max_odu = 5 * 40

    def __str__(self):
        return (f"Link(link_id={self._link_id}, "
                f"starting_node={self.starting_node._node_id}, "
                f"ending_node={self.ending_node._node_id}, "
                f"used_odus={self.used_odus},"
                f"light_path={ceil(self.used_odus/5)}/40)")

    def ODU_overflow(self):
        if self.used_odus > self.max_odu:
            return KeyError

    def add_service(self, client_service):
        if self.grooming:
            add_service = False
            for odu in self.odu2s:
                if odu.used_capacity < odu.max_capacity and client_service.rate == 10:
                    odu.add_service(client_service)
                    add_service = True
            if add_service == False and self.used_odus < self.max_odu:
                link_odu = ODU_LINK()
                link_odu.add_service(client_service=client_service)
                self.odu2s.append(link_odu)
                add_service = True
            if add_service:
                self.services.append(client_service)
            self.used_odus = len(self.odu2s)
            if not add_service:
                return KeyError
        else:
            self.service_grouping(client_service=client_service)

        if self.used_odus > self.max_odu:
            return KeyError

    def service_grouping(self, client_service):
      self.services.append(client_service)
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
              if self.used_odus < self.max_odu:
                odu2 = ODU2()
                for serv in group:
                    odu2.add_service(serv)
                self.odu2s.append(odu2)  # Store the grouped services ODU2
              else:
                self.services.remove(client_service)
                return KeyError

      self.used_odus = len(self.odu2s)