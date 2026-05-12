# Optical Transport Network (OTN) Simulation

This project simulates an Optical Transport Network (OTN) infrastructure, evaluating capacity, network grooming, traffic, transponders, and lightpaths across a dynamically generated topology. It utilizes a combination of node classes (`OTN1`, `OTN2`) and optical links, managed and evaluated using the `networkx` library to compute shortest paths and visualize the network.

## Project Structure

- **`Main.py`**: The entry point of the simulation. It generates a random network topology of `OTN2` and `OTN1` nodes, runs Dijkstra's algorithm for shortest paths, processes grooming iterations (10G vs 100G granularity), and visualizes the network and node statistics via `matplotlib`.
- **`Node.py`**: A base class for network nodes defining maximum capacity, ports, used ODUs, and I/O cards.
- **`OTN1.py`**: Represents an OTN1 node aggregating client services. Includes specific hardware constraints for port and capacity utilization mapping.
- **`OTN2.py`**: Represents the core OTN2 node. It manages optical transponders, handles traffic grooming, and connects standard physical layer interfaces.
- **`Link.py`**: Represents physical links between nodes in the transport network, holding maximum capacity channels (ODUs) and grouping/grooming logic.
- **`Service.py`**: Defines client end-to-end demands / services with defined bit rates (e.g. 10G or 100G), source-destination pairs, and mapped paths.
- **`IO_card.py`**: Simulates specialized I/O processing cards handling 10G or 100G interfaces on the routing hardware.
- **`ODU_link.py` & `ODU2.py`**: Simulates Optical Data Units framing and limits, tracking bandwidth consumption and grooming services inside optical channels.

## Core Features

- **Network Topology Generation**: Random graph generation with nodes mapped using NetworkX layout algorithms (Kamada-Kawai layout).
- **Service Provisioning**: Traffic demands dynamically load into the network with 10G or 100G rates mapping shortest-path distances.
- **Capacity & constraint validation**: Verifies and rejects services based on maximum node capacity, IO card configurations, and transponder limits.
- **Node Failure Simulation**: Simulates failures and analyzes traffic impact/rerouting limits.
- **Network Grooming**: Groups smaller demands (10G) into larger channels (ODU2s).

## Dependencies

You need to ensure the following libraries are installed in your environment:
- `networkx`
- `matplotlib`
- `pandas`

## Usage

Run the primary simulation file:
```bash
python Main.py
```

The script will output path computations in the console, render a `matplotlib` graph showing the topology, and then render bar charts detailing Total Capacity, Occupied Channels, and Transponders under changing network loads.
