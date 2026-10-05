import numpy as np
import matplotlib.pyplot as plt
import heapq
import time

GRID_SIZE = 70
START = (2, 2)
GOAL = (67, 67)
DENSITIES = [0.10, 0.20, 0.30]
MAX_ATTEMPTS = 1000

np.random.seed(42)


def create_grid(density):
    grid = np.zeros((GRID_SIZE, GRID_SIZE))
    random_values = np.random.random((GRID_SIZE, GRID_SIZE))
    grid[random_values < density] = 1

    grid[START[1], START[0]] = 0
    grid[GOAL[1], GOAL[0]] = 0

    return grid


def dijkstra(grid, start, goal):
    distances = {start: 0}
    previous = {start: None}
    priority_queue = [(0, start)]
    nodes_explored = 0

    while priority_queue:
        current_distance, current = heapq.heappop(priority_queue)
        nodes_explored += 1

        if current == goal:
            break

        if current_distance > distances[current]:
            continue

        x, y = current

        neighbors = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1)
        ]

        for neighbor in neighbors:
            nx, ny = neighbor

            if nx < 0 or nx >= GRID_SIZE or ny < 0 or ny >= GRID_SIZE:
                continue

            if grid[ny, nx] == 1:
                continue

            new_distance = current_distance + 1

            if neighbor not in distances or new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current
                heapq.heappush(priority_queue, (new_distance, neighbor))

    if goal not in previous:
        return None, nodes_explored

    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()
    return path, nodes_explored


def generate_valid_environment(density):
    attempts = 0

    while attempts < MAX_ATTEMPTS:
        attempts += 1
        grid = create_grid(density)
        path, _ = dijkstra(grid, START, GOAL)

        if path is not None:
            return grid, path, attempts

    return None, None, attempts


def main():
    results = []

    for density in DENSITIES:
        print("\n======================================")
        print("Testing obstacle density:", density * 100, "%")
        print("======================================")

        grid, path, attempts = generate_valid_environment(density)

        if path is None:
            print("Could not find a valid environment.")
            print("Attempts:", attempts)
            continue

        start_time = time.perf_counter()
        path, nodes_explored = dijkstra(grid, START, GOAL)
        execution_time = time.perf_counter() - start_time

        path_length = len(path) - 1

        print("Path found: Yes")
        print("Path length:", path_length, "km")
        print("Number of cells:", len(path))
        print("Nodes explored:", nodes_explored)
        print("Execution time:", execution_time, "seconds")
        print("Environment attempts:", attempts)

        results.append([
            density * 100,
            path_length,
            len(path),
            nodes_explored,
            execution_time,
            attempts,
            "Yes"
        ])

        plt.figure(figsize=(8, 8))
        plt.imshow(grid, cmap="gray_r", origin="lower")

        plt.scatter(
            START[0], START[1],
            marker="o", s=100, label="Start"
        )

        plt.scatter(
            GOAL[0], GOAL[1],
            marker="X", s=100, label="Goal"
        )

        path_x = [point[0] for point in path]
        path_y = [point[1] for point in path]

        plt.plot(
            path_x, path_y,
            linewidth=2, label="Shortest Path"
        )

        plt.title(
            "UGV Static Environment - "
            + str(int(density * 100))
            + "% Obstacles"
        )
        plt.xlabel("X (km)")
        plt.ylabel("Y (km)")
        plt.legend()
        plt.tight_layout()
        plt.show()

    print("\n\n==============================================")
    print("             FINAL RESULTS")
    print("==============================================")

    print(
        f"{'Density':<12}"
        f"{'Path Length':<15}"
        f"{'Cells':<12}"
        f"{'Nodes':<12}"
        f"{'Time (sec)':<15}"
        f"{'Attempts':<12}"
        f"{'Success':<10}"
    )

    print("-" * 74)

    for result in results:
        density, path_length, cells, nodes, execution_time, attempts, success = result

        print(
            f"{density:<12.0f}"
            f"{path_length:<15}"
            f"{cells:<12}"
            f"{nodes:<12}"
            f"{execution_time:<15.6f}"
            f"{attempts:<12}"
            f"{success:<10}"
        )


if __name__ == "__main__":
    main()
