from std_msgs.msg import String, Bool
from cse_190_assi_3.msg import AStarPath, PolicyList
import Queue as queue
from read_config import read_config
#from read_config import read_config
def manhattanDistance (a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def getPossibleMoves(config, current):
    moves = []
    for c, v in config["move_list"]:
        moves.append((current[0] + c, current[1] + v))
    return moves

def getPath(start, end, paths):
    path = [end]
    while paths[path[-1]][0] != start:
        path.append(paths[path[-1]][0])
    path.append(start)
    path.reverse()
    print path
    return path

def validMove(config, current):
    if current[0] < 0 or current[0] > config["map_size"][0]:
        return False
    elif current[1] < 0 or current[1] > config["map_size"][1]:
        return False
    return True
    
def astar(config):
    start = config["start"]
    start = (start[0], start[1])
    end = config["goal"]
    end = (end[0], end[1])
    if start == end:
        return [start]
    paths = {}
    q = queue.PriorityQueue()
    q.put((0, start))
    while not q.empty():
        currentCost, currentNode = q.get()
        currentCost = currentCost + 1
        if currentNode == end:
            return getPath(start, end, paths)
        for child in getPossibleMoves(config, currentNode):
            childList = [child[0], child[1]]
            if childList in config["pits"] or childList in config["walls"] or not validMove(config, child):
                continue
            newCost = currentCost + manhattanDistance(end, child)
            if child not in paths or paths[child][1] >= newCost:
                paths[child] = (currentNode, newCost)
                q.put((newCost, child))
    return None

#result = astar(read_config())
