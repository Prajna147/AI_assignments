import csv
import heapq


def load_graph(filename):
    graph = {}

    with open(filename, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            source = row["Origin"]
            destination = row["Destination"]
            distance = int(row["Distance"])

            # Add source city
            if source not in graph:
                graph[source] = []

            # Add destination city
            if destination not in graph:
                graph[destination] = []

            # Add road
            graph[source].append((destination, distance))

    return graph


def dijkstra(graph, source):

    # Initially, distance to every city is infinity
    distances = {}

    # Store previous city to reconstruct the path
    previous = {}

    for city in graph:
        distances[city] = float("inf")
        previous[city] = None

    # Distance from source to itself is 0
    distances[source] = 0

    # Priority queue
    # Stores: (distance, city)
    priority_queue = [(0, source)]

    while priority_queue:

        current_distance, current_city = heapq.heappop(priority_queue)

        # Ignore outdated entries
        if current_distance > distances[current_city]:
            continue

        # Check all neighboring cities
        for neighbor, road_distance in graph[current_city]:

            new_distance = current_distance + road_distance

            # If a shorter path is found
            if new_distance < distances[neighbor]:

                distances[neighbor] = new_distance
                previous[neighbor] = current_city

                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbor)
                )

    return distances, previous


def get_path(previous, source, destination):

    path = []
    current = destination

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()

    # If source is not the first city,
    # destination is unreachable
    if path[0] != source:
        return []

    return path


def main():

    filename = "indian_cities.csv"

    graph = load_graph(filename)

    print("======================================")
    print("   INDIA CITY DIJKSTRA ROUTE FINDER")
    print("======================================")

    print("\nAvailable cities:\n")

    cities = sorted(graph.keys())

    for city in cities:
        print("-", city)

    print("\n--------------------------------------")

    source = input("\nEnter source city: ").strip()
    destination = input("Enter destination city: ").strip()

    # Check whether cities exist
    if source not in graph:
        print("\nSource city not found.")
        return

    if destination not in graph:
        print("\nDestination city not found.")
        return

    # Run Dijkstra
    distances, previous = dijkstra(graph, source)

    # Get shortest path
    path = get_path(previous, source, destination)

    if not path:
        print("\nNo route found.")
        return

    print("\n======================================")
    print("             RESULT")
    print("======================================")

    print("\nSource      :", source)
    print("Destination :", destination)

    print("\nShortest distance:",
          distances[destination], "km")

    print("\nShortest path:")

    print(" -> ".join(path))

    print("\n======================================")


if __name__ == "__main__":
    main()