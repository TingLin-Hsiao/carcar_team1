from collections import deque
import pandas as pd

'''
graph = {
    1: {4: 3},            
    2: {3: 3 , 5: 3},      
    3: {2: 3},           
    4: {1: 3, 5: 3, 7: 3},
    5: {2: 3, 4: 3,6: 3,8: 3},
    6: {9: 3},
    7: {4: 3, 10: 3},
    8: {5: 3, 11: 3},
    9: {6: 3, 12: 3},
    10: {7: 3},
    11: {8: 3, 12: 3},
    12: {9: 3, 11   : 3}
}
graph_direction = {
    1:{'w': 4},
    2: {'s':3, 'w':5},
    3: {'n':2},
    4: {'e':1,'s':5,'w': 7},
    5: {'e':2, 'n':4, 'w':8},
    6: {'w':3},
    7: {'e':4,'w':10},
    8: {'e':5,'w':11},
    9: {'e':6, 'w':12},
    10: {'e':7},
    11: {'w':8,'s':12},
    12: {'e':9,'n':11},
}
'''
df = pd.read_csv("maze (2).csv")
df.columns = ["index", "North", "South", "West", "East", "ND", "SD", "WD", "ED"]
df = df[df["index"] != "index"]
df["index"] = df["index"].astype(int)

graph = {}
graph_direction = {}
graph_length = {}
for _, row in df.iterrows():
    node = int(row["index"])
    neighbors = {}
    directions = {}
    for dir_key, dist_key ,short in zip(["North", "South", "West", "East"], ["ND", "SD", "WD", "ED"],["n", "s", "w", "e"]):
        if pd.notna(row[dir_key]) and pd.notna(row[dist_key]):
            neighbor = int(row[dir_key])
            distance = int(row[dist_key])
            neighbors[neighbor] = distance
            directions[short] = neighbor
    graph[node] = neighbors
    graph_direction[node] = directions
    
def  bfs(graph, start, goal):
    queue = deque([(start, [start])])
    visited = set() 
    
    while len(queue):
        current, path = queue.popleft()
        if current == goal:
            return path
        visited.add(current)
        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))
                visited.add(neighbor)
    return None
start_node = 3
goal_node = 45
    
shortest_path = bfs(graph, start_node, goal_node)
if shortest_path!=-1:
    shortest_distance = len(shortest_path)-1

def path_to_directions(path, graph_directions):
    directions = []
    facing = None

    for i in range(len(path) - 1):
        current = path[i]
        nxt = path[i + 1]

        for dir_name, neighbor in graph_directions.get(current, {}).items():
            if neighbor == nxt:
                if i == 0:
                    directions.append("front")
                    facing = dir_name
                else:
                    directions.append(get_relative_direction(facing, dir_name))
                    facing = dir_name
                break
    return directions

direction_order = ['n', 'e', 's', 'w']

def get_relative_direction(facing, target):
    f_idx = direction_order.index(facing)
    t_idx = direction_order.index(target)
    diff = (t_idx - f_idx) % 4
    if diff == 0:
        return "front"
    elif diff == 1:
        return "right"
    elif diff == 2:
        return "back"
    elif diff == 3:
        return "left"
def total_distance(path, graph):
    total = 0
    for i in range(len(path) - 1):
        current = path[i]
        next_node = path[i + 1]
        total += graph[current][next_node]
    return total
    
print ("enter starting node: ", start_node)
print ("enter end node: ", goal_node)

if (len(shortest_path)!=0):
    shortest_distance = len(shortest_path) - 1
    print("shortest path: ", shortest_path)
    print("shortest distance: ", shortest_distance)
    direction_list = path_to_directions(shortest_path, graph_direction)
    print("direction：", direction_list)
    print("total distance: ", total_distance(shortest_path, graph))
else:
    print("失敗了, yeeha")

    
