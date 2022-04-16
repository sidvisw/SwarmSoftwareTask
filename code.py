import sys
from api import *
from time import sleep
import numpy as np

#######    YOUR CODE FROM HERE #######################
grid = []
neigh = [[-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1]]


class Node:
    def __init__(self, value, point):
        self.value = value  # 0 for blocked,1 for unblocked
        self.point = point
        self.parent = None
        self.move = None
        self.H = 0
        self.G = 0


def isValid(pt):
    return pt[0] >= 0 and pt[1] >= 0 and pt[0] < 200 and pt[1] < 200


def neighbours(point):  # returns valid neighbours
    global grid, neigh
    x, y = point.point
    links = []
    for i in range(len(neigh)):
        newX = x+neigh[i][0]
        newY = y+neigh[i][1]
        if not isValid((newX, newY)):
            continue
        links.append((i+1, grid[newX][newY]))
    return links


def diagonal(point, point2):
    return max(abs(point.point[0] - point2.point[0]), abs(point.point[1]-point2.point[1]))


def aStar(start, goal):
    openset = set()
    closedset = set()
    current = start
    openset.add(current)
    while openset:
        current = min(openset, key=lambda o:o.G + o.H)
        openset.remove(current)
        closedset.add(current)
        if current == goal:
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
                if(current.point==start.point):
                    path.append(current)
                    return path[::-1]
        for move,node in neighbours(current):
            if node in closedset:
                continue
            if node.value==0:
                continue
            if node in openset:
                new_g = current.G + 1
                if node.G > new_g:
                    node.G = new_g
                    node.parent = current
                    node.move=move
            else:
                node.G = current.G + 1
                node.H = diagonal(node, goal)
                node.parent = current
                node.move=move
                openset.add(node)

def navigateBot(botId):
    from json import loads
    global grid
    botsPose = [get_botPose_list()[botId]]
    obstaclePose = get_obstacles_list()
    greenZone = get_greenZone_list()
    redZone = get_redZone_list()
    originalGreenZone = get_original_greenZone_list()
    for i in range(200):
        grid.append([])
        for j in range(200):
            grid[i].append(Node(1, (i, j)))
    for pt in obstaclePose:
        for i in range(pt[0][0], pt[2][0]+1):
            for j in range(pt[0][1], pt[2][1]+1):
                grid[i][j] = Node(0, (i, j))
    goal = []
    if botId == 0:
        f = open("goals.txt", "w")
        for vertices in get_greenZone_list():
            goal.append([int((vertices[0][0]+vertices[2][0])/2),int((vertices[0][1]+vertices[2][1])/2)])
        f.write(str(goal))
        f.close()
    else:
        sleep(1)
    while get_greenZone_list():
        botsPose = [get_botPose_list()[botId]]
        start = grid[botsPose[0][0]][botsPose[0][1]]
        f = open("goals.txt")
        try:
            goal = loads(f.read())
        except Exception as e:
            print(e)
        f.close()
        if len(goal) == 0:
            for vertices in get_greenZone_list():
                goal.append([int((vertices[0][0]+vertices[2][0])/2),int((vertices[0][1]+vertices[2][1])/2)])
        targetgoal = min(goal, key=lambda g: (botsPose[0][0]-g[0])**2+(botsPose[0][1]-g[1])**2)
        goal.remove(targetgoal)
        f = open("goals.txt", "w")
        f.write(str(goal))
        f.close()
        targetgoal = grid[targetgoal[0]][targetgoal[1]]
        path = aStar(start, targetgoal)
        pos = [get_botPose_list()[botId]]
        try:
            for i in range(1, len(path)):
                successful_move, mission_complete = send_command(
                    botId, path[i].move)
                pos = get_botPose_list()
                if successful_move:
                    print("YES")
                else:
                    print("NO")
                if mission_complete:
                    print("MISSION COMPLETE")
                    exit()
                pos = [get_botPose_list()[botId]]
                print(pos[0])
        except Exception as e:
            print("-----------------Invalid Path--------------------")


def level1(botId):
    navigateBot(botId)


def level2(botId):
    navigateBot(botId)


def level3(botId):
    navigateBot(botId)


def level4(botId):
    navigateBot(botId)


def level5(botId):
    pass


def level6(botId):
    pass


#######    DON'T EDIT ANYTHING BELOW  #######################

if __name__ == "__main__":
    botId = int(sys.argv[1])
    level = get_level()
    if level == 1:
        level1(botId)
    elif level == 2:
        level2(botId)
    elif level == 3:
        level3(botId)
    elif level == 4:
        level4(botId)
    elif level == 5:
        level5(botId)
    elif level == 6:
        level6(botId)
    else:
        print("Wrong level! Please restart and select correct level")