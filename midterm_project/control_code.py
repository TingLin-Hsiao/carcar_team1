import pandas as pd
import heapq
from itertools import combinations, permutations
import time

start_time = time.time()


# === 讀取 CSV 並建立圖 ===
file_path = "big_maze_113.csv"  #maze的檔案名稱
df = pd.read_csv(file_path, header=0)
df.columns = ["index", "North", "South", "West", "East", "ND", "SD", "WD", "ED"]
df = df[df["index"] != "index"]
df["index"] = df["index"].astype(int)

graph = {}
graph_directions = {}  # 每個節點的四個方向對應哪個節點

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


#   Dijkstra 最短路徑算法 ===
def dijkstra(graph, start, goal,t_f,t_l,t_b,t_r):
    heap = [(0.0, start, [start], None)]  # (累積時間, 當前節點, 路徑, 當前朝向)
    visited = {}

    while heap:
        total_time, current, path, facing = heapq.heappop(heap)

        if (current, facing) in visited and visited[(current, facing)] <= total_time:
            continue
        visited[(current, facing)] = total_time

        if current == goal:
            return path, total_time

        for neighbor in graph.get(current, {}):
            abs_dir = get_absolute_direction(current, neighbor)
            rel_dir = get_relative_direction(facing, abs_dir)

            if rel_dir == 'F':
                step_time = t_f
            elif rel_dir == 'L':
                step_time = t_l + t_f
            elif rel_dir == 'R':
                step_time = t_r + t_f
            elif rel_dir == 'B':
                step_time = t_b + t_f
            else:
                continue  # 無法判斷方向

            heapq.heappush(heap, (
                total_time + step_time,
                neighbor,
                path + [neighbor],
                abs_dir
            ))

    return [], float('inf')



# === 相對方向轉換 ===
direction_order = ['north', 'east', 'south', 'west']

def get_absolute_direction(from_node, to_node):
    for dir_name, neighbor in graph_directions.get(from_node, {}).items():
        if neighbor == to_node:
            return dir_name
    return None

def get_relative_direction(prev_facing, new_facing):
    if prev_facing is None:
        return 'F'
    i = direction_order.index(prev_facing)
    j = direction_order.index(new_facing)
    delta = (j - i) % 4
    return ['F','R', 'B', 'L'][delta]

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



def build_all_pairs_shortest_paths_with_time(graph, nodes,t_f,t_l,t_b,t_r):
    shortest_paths = {}
    time_cache = {}
    for i in nodes:
        for j in nodes:
            if i == j:
                continue
            path, _ = dijkstra(graph, i, j,t_f,t_l,t_b,t_r)
            shortest_paths[(i, j)] = path
            time_cache[(i, j)] = compute_total_time(path,t_f,t_l,t_b,t_r)
    return shortest_paths, time_cache

def compute_total_time(path,t_f,t_l,t_b,t_r):
    total_time = 0.0
    facing = None
    for i in range(len(path) - 1):
        abs_dir = get_absolute_direction(path[i], path[i+1])
        rel_dir = get_relative_direction(facing, abs_dir)
        if rel_dir == 'F':
            total_time += t_f
        elif rel_dir =='L':
            total_time += t_f + t_l  # 轉彎完再直走
        elif rel_dir =='R':
            total_time += t_f + t_r
        elif rel_dir == 'B':
            total_time += t_b + t_f  # 迴轉完再直走
        facing = abs_dir
    return total_time



def best_path_within_time(start_node, treasures, scores, path_cache, time_cache, max_time):
    best_path = []
    best_score = 0
    best_total_time = float('inf')
    best_treasure_path = []
    best_score_sequence = []

    for r in range(1, len(treasures)+1):
        for subset in combinations(treasures, r):
            for perm in permutations(subset):
                temp_path = [start_node]
                current = start_node
                total_score = 0
                total_time = 0
                visited = set()
                valid = True
                score_sequence = []

                for target in perm:
                    if (current, target) not in path_cache:
                        valid = False
                        break

                    segment = path_cache[(current, target)]
                    segment_time = time_cache[(current, target)]

                    if total_time + segment_time > max_time:
                        valid = False
                        break

                    total_time += segment_time
                    temp_path += segment[1:]
                    if target not in visited:
                        score = scores.get(target, 0)
                        total_score += score
                        score_sequence.append(score)
                        visited.add(target)
                    else:
                        score_sequence.append(0)
                    current = target

                if not valid:
                    continue

                # 排序順序：
                # 1. 總分數高
                # 2. 寶藏分數順序比（類似字典序）
                # 3. 總時間少
                if (total_score > best_score) or \
                   (total_score == best_score and score_sequence > best_score_sequence) or \
                   (total_score == best_score and score_sequence == best_score_sequence and total_time < best_total_time):
                    best_path = temp_path
                    best_score = total_score
                    best_total_time = total_time
                    best_treasure_path = list(perm)
                    best_score_sequence = score_sequence

    return {
        "最佳路徑": best_path,
        "方向列": get_relative_direction_list(best_path),
        "總分數": best_score,
        "總時間": best_total_time,
        "拜訪寶藏順序": best_treasure_path
    }
 



 

# === 執行範例 ===
t_f = 1
t_l = 0.5    
t_r = 0.5
t_b = 1 

start_node = 24
cols = 6
rows = 8
treasures = [8,12,14,18, 30,31,43,44,48]

max_time = 90   #最大時間


def get_path(t_f=1, t_l=0.5, t_r=0.5, t_b=1,start_node=24,cols=6,rows=8,treasures= [8,14,18,30,31,43,44,48],max_time=90):
    scores = compute_scores(start_node, treasures ,cols ,rows)
    all_nodes = [start_node] + treasures
    all_pairs , time_cache = build_all_pairs_shortest_paths_with_time(graph, all_nodes,t_f,t_l,t_b,t_r)
    result = best_path_within_time(start_node, treasures, scores, all_pairs, time_cache,max_time)
    
    return result["方向列"][1:]
    
    





# end_time = time.time()
# print("執行時間：", end_time - start_time, "秒")

# === 輸出 ===
# print("最佳節點路徑：", result["最佳路徑"])
# print("對應方向列：", result["方向列"])
# print("總分數：", result["總分數"])
# print("總時間：", result["總時間"])


if __name__ == "__main__":
    
    scores = compute_scores(start_node, treasures ,cols ,rows)
    all_nodes = [start_node] + treasures
    all_pairs , time_cache = build_all_pairs_shortest_paths_with_time(graph, all_nodes,t_f,t_l,t_b,t_r)
    result = best_path_within_time(start_node, treasures, scores, all_pairs, time_cache,max_time)
    shortest_path = result["方向列"]
    best_path = get_path()
    print("最佳節點路徑：", result["最佳路徑"])
    print(best_path)
    print("總分數：", result["總分數"])
    print("總時間：", result["總時間"])
    print (result["拜訪寶藏順序"])
    
