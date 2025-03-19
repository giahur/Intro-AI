"""
File: State.py
Author: Gia Hur (gxh221)
Due: 09/09/2024
"""

import random
from collections import deque
import copy
import heapq

class State:
    def __init__(self):
        self.state = ['0', '1', '2', '3', '4', '5', '6', '7', '8']
        #random.seed(221)
        
    def setState(self, state):
        if(len(state) != 9) or (set(state) != set("012345678")):
            print("Error: invalid puzzle state")
        else:
            self.state = state

    def printState(self):
        for i in range(0, 9, 3):
            print(self.state[i:i+3])

    def findZero(self):
        return self.state.index("0")
        
    def move(self, direction):
        if direction not in ["left", "right", "up", "down"]:
            print("Error: invalid move, must be 'left', 'right', 'up', 'down'")
            return False
        else:
            zeroIndex = self.findZero()
            x, y = divmod(zeroIndex, 3)
            if direction == "left" and y > 0:
                newIndex = zeroIndex - 1
            elif direction == "right" and y < 2:
                newIndex = zeroIndex + 1
            elif direction == "up" and x > 0:
                newIndex = zeroIndex -3
            elif direction == "down" and x < 2:
                newIndex = zeroIndex + 3
            else:
                print("Error: invalid move")
                return False
            
            self.state[zeroIndex], self.state[newIndex] = self.state[newIndex], self.state[zeroIndex]
            return True

    def scrambleState(self, n):
        if(len(n) != 1) or not (n[0].isdigit()):
            print("Error: invalid number of scrambles, must be integer")
        else: 
            self.setState(['0', '1', '2', '3', '4', '5', '6', '7', '8'])
            for i in range(int(n[0])): 
                valid = False
                while not valid:
                    valid = self.move(random.choice(["left", "right", "up", "down"]))
    
    def dfs(self, maxNodes=1000):
        stack = deque([(self.state, [])])
        visited = set([tuple(self.state)])
        numNodes = 1
        
        while stack and numNodes < maxNodes:
            current, path = stack.pop()
            if current == ['0', '1', '2', '3', '4', '5', '6', '7', '8']:
                print("Nodes created during search: ", numNodes)
                print("Solution length: ", len(path))
                print("Move sequence: ")
                for move in path:
                    print(f"move {move}")
                self.effectiveBranchingFactor(numNodes, len(path))
                return
            
            for move in ["down", "up", "right", "left"]:
                child = State()
                child.setState(copy.deepcopy(current)) 
                
                zeroIndex = child.findZero()
                x, y = divmod(zeroIndex, 3)
                
                if (move == "left" and y > 0) or (move == "right" and y < 2) or (move == "up" and x > 0) or (move == "down" and x < 2):
                    child.move(move)
                    newPath = path + [move]
                    numNodes += 1
                    
                    if tuple(child.state) not in visited:
                        stack.append((child.state, newPath))
                        visited.add(tuple(child.state))
                        print("stack:", " ".join(str(stack[i][1]) for i in range(len(stack))))

                    else:
                        print("visited: ", newPath)
        print("Error: maxNodes limit", maxNodes, "reached")
            
    def bfs(self, maxNodes=1000):
        q = deque([(self.state, [])])
        visited = set([tuple(self.state)])
        numNodes = 1

        while q and numNodes < maxNodes:
            current, path = q.popleft()
            if current == ['0', '1', '2', '3', '4', '5', '6', '7', '8']:
                print("Nodes created during search: " + str(numNodes))
                print("Solution length: " + str(len(path)))
                print("Move sequence: " + ' '.join(path))
                
                self.effectiveBranchingFactor(numNodes, len(path))
                return

            for move in ["left", "right", "up", "down"]:
                child = State()
                child.setState(copy.deepcopy(current))

                zeroIndex = child.findZero()
                x, y = divmod(zeroIndex, 3)

                if(move == "left" and y > 0) or (move == "right" and y < 2) or (move == "up" and x > 0) or (move == "down" and x < 2):
                    child.move(move)
                    newPath = path + [move]
                    numNodes += 1

                    if child.state == ['0', '1', '2', '3', '4', '5', '6', '7', '8']:
                        print("Nodes created during search: " + str(numNodes))
                        print("Solution length: " + str(len(newPath)))
                        print("Move sequence: ")
                        for move in newPath:
                            print(f"move {move}")

                        self.effectiveBranchingFactor(numNodes, len(newPath))
                        return
                    
                    if tuple(child.state) not in visited:
                        q.append((child.state, newPath))
                        visited.add(tuple(child.state))
        print("Error: maxnodes limit (" + str(maxNodes) + ") reached")

    def h1(self):
        goalState = ['0', '1', '2', '3', '4', '5', '6', '7', '8']
        misplacedTiles = 0
        # iterates through puzzle
        for i in range(9):
            # upping count when tile is out of place (besides blank tile)
            if self.state[i] != goalState[i] and self.state[i] != '0':
                misplacedTiles += 1
        return(misplacedTiles)

    def h2(self):
        manhattanDistance = 0
        # iterates through puzzle
        for i in range(9): 
            if self.state[i] != "0":
                # finds indices of current and goal state
                goalX, goalY = divmod(int(self.state[i]), 3)
                currX, currY = divmod(i, 3)

                # adds absolute difference between values to manhattan distance
                manhattanDistance += abs(currX - goalX) + abs(currY - goalY)
        return(manhattanDistance)

    def aStar(self, heuristic, maxNodes=1000):
        visited = {} # dictionary so we can search by state and path cost can be updated
        pq = [] # priority queue
        g = 0 
        if heuristic == "h1":
            h = self.h1()
        else:
            h = self.h2()
        numNodes = 1 
         # compares cost then numNodes: will never be equal, so state will never be compared
        heapq.heappush(pq, (g + h, numNodes, self.state, []))

        while pq and numNodes < int(maxNodes):
            _, _, current, path = heapq.heappop(pq)
            # checks if initial puzzle is goal state
            if current == ['0', '1', '2', '3', '4', '5', '6', '7', '8']:
                print("Nodes created during search: " + str(numNodes))
                print("Solution length: " + str(len(path)))
                print("Move sequence: " + ' '.join(path))

                self.effectiveBranchingFactor(numNodes, len(path))
                return
            
            # checks if state is visited AND that path cost is more than original
            if tuple(current) in visited and visited[tuple(current)] <= g+h:
                continue
            
            # adds new state OR updates path cost
            visited[tuple(current)] = g+h

            for move in ["left", "right", "up", "down"]:
                child = State()
                child.setState(copy.deepcopy(current))

                zeroIndex = child.findZero()
                x, y = divmod(zeroIndex, 3)

                # if move is valid
                if(move == "left" and y > 0) or (move == "right" and y < 2) or (move == "up" and x > 0) or (move == "down" and x < 2):
                    child.move(move)
                    newPath = path + [move]
                    g = len(newPath)

                    if heuristic == "h1":
                        h = child.h1()
                    else:
                        h = child.h2()

                    # checks child is not visited OR has better path cost
                    if tuple(child.state) not in visited or g+h < visited[tuple(child.state)]:
                        numNodes += 1
                        heapq.heappush(pq, (g + h, numNodes, child.state, newPath))
                        # adds new child OR updates 
                        visited[tuple(current)] = g+h
                        
                    # only finishes if goal state is the state with lowest cost (front of queue)
                    if pq[0][2] == ['0', '1', '2', '3', '4', '5', '6', '7', '8']:
                        print("Nodes created during search: " + str(numNodes))
                        print("Solution length: " + str(len(newPath)))
                        print("Move sequence: ")
                        for move in newPath:
                            print(f"move {move}")

                        self.effectiveBranchingFactor(numNodes, len(newPath))
                        return
        print("Error: maxnodes limit (" + str(maxNodes) + ") reached")
    
    def effectiveBranchingFactor(self, n, d):
        low, high = 0, n**(1/d)
        # while diff between high are low is less than tolerance
        while(high - low >= 1e-10):
            mid = (high + low) / 2
            # expression with +1 omitted
            nodes = sum(mid**i for i in range(1, d+1))
            # if less than goal, raise lower bound
            if nodes < n:
                low = mid
            # otherwise lower upper bound
            else:
                high = mid
        # return average (accurate due to small tolerance)
        print((high + low)/2)

    def cmd(self, commandString: str):
        resultArray = commandString.split()
        stringName = resultArray[0]
        resultArray.pop(0)

        match stringName:
            case "setState":
                self.setState(resultArray)
            case "printState":
                self.printState()
            case "move":
                if len(resultArray) != 1:
                    print("Error: invalid move, must be 'left', 'right', 'up', 'down'")
                else:
                    self.move(resultArray[0])
            case "scrambleState":
                self.scrambleState(resultArray)
            case "solve":
                if len(resultArray) == 1: # A* needs heuristic
                    algo = resultArray[0]
                    if(algo == "BFS"):
                        self.bfs()
                        return
                    if(algo == "DFS"):
                        self.dfs()
                        return
                    else:
                        print("Error: invalid solve command")
                        return
                elif len(resultArray) == 2:
                    algo = resultArray[0]
                    if algo not in ["BFS", "DFS", "A*"]:
                        print("Error: invalid solve command")
                        return
                    if algo == "A*":
                        heuristic = resultArray[1]
                        if heuristic not in ["h1", "h2"]:
                            print("Error: invalid heuristic")
                            return
                        self.aStar(heuristic)
                        return
                    maxNodes = resultArray[1][9:]
                    if maxNodes.isdigit():
                        if(algo == "BFS"):
                            self.bfs(int(maxNodes))
                            return
                        if(algo == "DFS"):
                            self.dfs(int(maxNodes))
                            return
                    else:
                        print("Error: invalid maxNodes value")
                        return
                elif len(resultArray) == 3: #if maxNodes given
                    algo = resultArray[0]
                    if algo != "A*":
                        print("Error: invalid solve command")
                        return
                    heuristic = resultArray[1]
                    if heuristic not in ["h1", "h2"]:
                        print("Error: invalid heuristic")
                        return
                    maxNodes = resultArray[2][9:]
                    if maxNodes.isdigit(): #check maxNodes is int
                        self.aStar(heuristic, maxNodes)
                        return
                    else:
                        print("Error: invalid maxNodes value")
                else:
                    print("invalid solve command")
                    return
            case "h1":
                self.h1()
                print(self.h1()) # For testing: so it doesn't print during A*
            case "h2":
                self.h2()
                print(self.h2())
            case "#" | "//":
                pass
            case _:
                s = "Error: invalid command: " + stringName + " " + ' '.join(resultArray)
                print(s)
    
    def cmdfile(self, fileName):
        try:
            with open(fileName, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line: 
                        print(line)
                        self.cmd(line)
        except FileNotFoundError:
            print("Error: file not found")

def main():
    hw1 = State()
    hw1.cmdfile("testcmds.txt")

if __name__=="__main__":
    main()