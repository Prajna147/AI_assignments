import numpy as np
import matplotlib.pyplot as plt
import heapq
import time

N = 70
START = (2, 2)
GOAL = (67, 67)
DENSITY = 0.20
SENSOR = 1
UPDATE = 20
NEW_OBS = 2

np.random.seed(42)

true = (np.random.rand(N, N) < DENSITY).astype(int)
true[START[1], START[0]] = 0
true[GOAL[1], GOAL[0]] = 0

known = np.full((N, N), -1)
known[START[1], START[0]] = 0


def sense(pos):
    x, y = pos

    for dx in range(-SENSOR, SENSOR + 1):
        for dy in range(-SENSOR, SENSOR + 1):
            nx, ny = x + dx, y + dy

            if 0 <= nx < N and 0 <= ny < N:
                known[ny, nx] = true[ny, nx]


def dijkstra(start, goal):
    dist = {start: 0}
    prev = {start: None}
    q = [(0, start)]
    explored = 0

    while q:
        d, u = heapq.heappop(q)
        explored += 1

        if u == goal:
            break

        if d != dist[u]:
            continue

        x, y = u

        for v in [(x + 1, y), (x - 1, y),
                  (x, y + 1), (x, y - 1)]:

            a, b = v

            if not (0 <= a < N and 0 <= b < N):
                continue

            if known[b, a] == 1:
                continue

            nd = d + 1

            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                prev[v] = u
                heapq.heappush(q, (nd, v))

    if goal not in prev:
        return None, explored

    path = []
    u = goal

    while u is not None:
        path.append(u)
        u = prev[u]

    return path[::-1], explored


def add_obstacles(pos):
    free = np.argwhere(true == 0)

    free = [
        (x, y) for y, x in free
        if (x, y) not in [START, GOAL, pos]
    ]

    if free:
        for x, y in free[:NEW_OBS]:
            true[y, x] = 1


sense(START)

pos = START
actual_path = [pos]

replans = 0
events = 0
nodes = 0
steps = 0

start_time = time.perf_counter()

path, explored = dijkstra(pos, GOAL)
nodes += explored
replans += 1

while pos != GOAL and steps < 10000:

    if steps > 0 and steps % UPDATE == 0:
        add_obstacles(pos)
        sense(pos)
        events += 1

    if path is None:
        break

    if pos not in path:
        path, explored = dijkstra(pos, GOAL)
        nodes += explored
        replans += 1
        continue

    path = path[path.index(pos):]

    if len(path) < 2:
        break

    next_pos = path[1]

    if true[next_pos[1], next_pos[0]] == 1:
        known[next_pos[1], next_pos[0]] = 1

        path, explored = dijkstra(pos, GOAL)
        nodes += explored
        replans += 1
        continue

    pos = next_pos
    actual_path.append(pos)
    path = path[1:]
    steps += 1

    sense(pos)

    if any(known[y, x] == 1 for x, y in path):
        path, explored = dijkstra(pos, GOAL)
        nodes += explored
        replans += 1


execution_time = time.perf_counter() - start_time


print("\n========== DYNAMIC UGV ==========")
print("Goal reached:", pos == GOAL)
print("Path length:", len(actual_path) - 1, "km")
print("Movement steps:", steps)
print("Dynamic obstacle events:", events)
print("Replans:", replans)
print("Nodes explored:", nodes)
print("Execution time:", execution_time, "seconds")
print("Final position:", pos)


x = [p[0] for p in actual_path]
y = [p[1] for p in actual_path]

plt.figure(figsize=(8, 8))
plt.imshow(true, cmap="gray_r", origin="lower")
plt.plot(x, y, linewidth=2, label="UGV Path")
plt.scatter(*START, s=100, label="Start")
plt.scatter(*GOAL, s=100, marker="X", label="Goal")

plt.xlabel("X (km)")
plt.ylabel("Y (km)")
plt.title("UGV Dynamic Unknown Environment")
plt.legend()
plt.show()
