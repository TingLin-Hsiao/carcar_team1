import pandas as pd
import heapq
from itertools import combinations, permutations
import time

start_time = time.time()


# === 讀取 CSV 並建立圖 ===
file_path = "C:/Users/edwin/carcar_team1/midterm_project/big_maze_113.csv"  # maze 檔案名稱
df = pd.read_csv(file_path, header=0)
df.columns = ["index", "North", "South", "West", "East", "ND", "SD", "WD", "ED"]
df = df[df["index"] != "index"]
df["index"] = df["index"].astype(int)

graph = {}
graph_directions = {}  # 用來記錄每個節點的四個方向對應哪個節點

for _, row in df.iterrows():
    node = int(row["index"])
    neighbors = {}
    directions = {}
    for dir_key, dist_key in zip(["North", "South", "West", "East"], ["ND", "SD", "WD", "ED"]):
        if pd.notna(row[dir_key]) and pd.notna(row[dist_key]):
            neighbor = int(row[dir_key])
            distance = int(row[dist_key])
            neighbors[neighbor] = distance
            directions[dir_key.lower()] = neighbor

            # === 加入反向邊 ===
            if neighbor not in graph:
                graph[neighbor] = {}
            graph[neighbor][node] = distance

    graph[node] = neighbors
    graph_directions[node] = directions


# === Dijkstra 最短路徑算法 ===
def dijkstra(graph, start, goal):
    heap = [(0, start, [start])]
    visited = set()
    while heap:
        cost, current, path = heapq.heappop(heap)
        if current == goal:
            return path, cost
        if current in visited:
            continue
        visited.add(current)
        for neighbor, weight in graph.get(current, {}).items():
            if neighbor not in visited:
                heapq.heappush(heap, (cost + weight, neighbor, path + [neighbor]))
    return [], float('inf')

# === 貪婪法拜訪所有寶藏點 ===
'''
def greedy_path_through_treasures(graph, start_node, treasure_nodes):
    remaining = set(treasure_nodes)
    current = start_node
    full_path = [current]
    total_distance = 0
    visit_order = []

    while remaining:
        closest_target = None
        closest_dist = float('inf')
        best_path = []

        for target in remaining:
            path, dist = dijkstra(graph, current, target)
            if path and dist < closest_dist:
                closest_target = target
                closest_dist = dist
                best_path = path

        if closest_target is None:
            break

        visit_order.append(closest_target)
        full_path += best_path[1:]
        total_distance += closest_dist
        current = closest_target
        remaining.remove(closest_target)

    return {
        "起點": start_node,
        "拜訪順序": visit_order,
        "完整路徑": full_path,
        "總距離": total_distance,
        "剩餘未達成寶藏": list(remaining)
    }
'''
# === 相對方向轉換 ===
direction_order = ['north', 'east', 'south', 'west']

def get_absolute_direction(from_node, to_node):
    for dir_name, neighbor in graph_directions.get(from_node, {}).items():
        if neighbor == to_node:
            return dir_name
    return None

def get_relative_direction(prev_facing, new_facing):
    if prev_facing is None:
        return 'f'
    i = direction_order.index(prev_facing)
    j = direction_order.index(new_facing)
    delta = (j - i) % 4
    return ['f', 'r', 'b', 'l'][delta]

def get_relative_direction_list(path):
    facing = None
    direction_list = []
    for i in range(len(path) - 1):
        abs_dir = get_absolute_direction(path[i], path[i + 1])
        rel_dir = get_relative_direction(facing, abs_dir)
        direction_list.append(rel_dir)
        facing = abs_dir
    return direction_list


def get_position(node_id, rows, cols):
    row = (node_id - 1) // cols
    col = cols - 1 - ((node_id - 1) % cols)
    return (row, col)

def compute_scores(start, treasures, cols,rows):
    sx, sy = get_position(start,rows, cols)
    scores = {}
    for t in treasures:
        tx, ty = get_position(t,rows, cols)
        scores[t] = 30*(abs(sx-tx)+abs(ty-sy))
    return scores



def build_all_pairs_shortest_paths_with_time(graph, nodes):
    shortest_paths = {}
    time_cache = {}
    for i in nodes:
        for j in nodes:
            if i == j:
                continue
            path, _ = dijkstra(graph, i, j)
            shortest_paths[(i, j)] = path
            time_cache[(i, j)] = compute_total_time(path)
    return shortest_paths, time_cache

def compute_total_time(path):
    total_time = 0.0
    facing = None
    for i in range(len(path) - 1):
        abs_dir = get_absolute_direction(path[i], path[i+1])
        rel_dir = get_relative_direction(facing, abs_dir)
        if rel_dir == 'f':
            total_time += t_f
        elif rel_dir in ['l', 'r']:
            total_time += t_f + t_l  # 轉彎完再直走
        elif rel_dir == 'b':
            total_time += t_b + t_f  # 迴轉完再直走
        facing = abs_dir
    return total_time



def best_path_within_time(start_node, treasures, scores, path_cache, time_cache, max_time):
    best_path = []
    best_score = 0
    best_total_time = 0

    for r in range(1, len(treasures)+1):
        for subset in combinations(treasures, r):
            for perm in permutations(subset):
                path = [start_node]
                current = start_node
                total_score = 0
                total_time = 0
                visited = set()
                valid = True

                for target in perm:
                    if (current, target) not in path_cache:
                        valid = False
                        break

                    segment = path_cache[(current, target)]
                    segment_time = time_cache[(current, target)]
                    total_time += segment_time
                    if total_time > max_time:
                        valid = False
                        break

                    path += segment[1:]
                    if target not in visited:
                        total_score += scores.get(target, 0)
                        visited.add(target)
                    current = target

                if valid and total_score > best_score:
                    best_path = path
                    best_score = total_score
                    best_total_time = total_time

    return {
        "最佳路徑": best_path,
        "方向列": get_relative_direction_list(best_path),
        "總分數": best_score,
        "總時間": best_total_time
    }
 

# === 執行範例 ===
t_f = 0.5  
t_l = 1       
t_r = 1
t_b = 2   

start_node = 24
cols = 6
rows = 8
treasures = [8,12,14,18, 30,31,43,44,48]
scores = compute_scores(start_node, treasures ,cols ,rows)
max_time = 45
all_nodes = [start_node] + treasures
all_pairs , time_cache = build_all_pairs_shortest_paths_with_time(graph, all_nodes)


result = best_path_within_time(start_node, treasures, scores, all_pairs, time_cache,max_time)
shortest_path = result["方向列"]

end_time = time.time()
print("執行時間：", end_time - start_time, "秒")

# === 輸出 ===
print("最佳節點路徑：", result["最佳路徑"])
print("對應方向列：", result["方向列"])
print("總分數：", result["總分數"])
print("總時間：", result["總時間"])

