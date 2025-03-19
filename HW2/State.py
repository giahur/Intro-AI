"""
File: State.py
Author: Gia Hur (gxh221)
Due: 09/09/2024
"""

import random
from collections import deque
import copy

class State:
    def __init__(self):
        self.state = ['0', '1', '2', '3', '4', '5', '6', '7', '8']
        random.seed(221)
        
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
        numNodes = 1

        if self.state == ['0', '1', '2', '3', '4', '5', '6', '7', '8']:
            print("Nodes created during search: " + str(numNodes))
            print("Solution length: 0")
            print("Move sequence: ")
            return

        zeroIndex = self.findZero()
        x, y = divmod(zeroIndex, 3)

        if(y>0):
            stack.append((self.state, ["left"]))
        if(y<2):
            stack.append((self.state, ["right"]))
        if(x>0):
            stack.append((self.state, ["up"]))
        if(x<2):
            stack.append((self.state, ["down"]))

        while stack and numNodes < maxNodes:
            current, path = stack.pop()
            if current == ['0', '1', '2', '3', '4', '5', '6', '7', '8']:
                print("Nodes created during search: " + str(numNodes))
                print("Solution length: " + str(len(path)))
                print("Move sequence: ")
                for move in path:
                    print(f"move {move}")
                return
            
            child = State()
            child.setState(copy.deepcopy(current))

            zeroIndex = child.findZero()
            x, y = divmod(zeroIndex, 3)
            if(y>0):
                child.move("left")
                newPath = path + ["left"]
                stack.append((child.state, newPath))
                numNodes += 1
            if(y<2):
                child.move("right")
                newPath = path + ["right"]
                stack.append((child.state, newPath))
                numNodes += 1
            if(x>0):
                child.move("up")
                newPath = path + ["up"]
                stack.append((child.state, newPath))
                numNodes += 1
            if(x<2):
                child.move("down")
                newPath = path + ["down"]
                stack.append((child.state, newPath))
                numNodes += 1
            if child.state == ['0', '1', '2', '3', '4', '5', '6', '7', '8']:
                print("Nodes created during search: " + str(numNodes))
                print("Solution length: " + str(len(newPath)))
                print("Move sequence: ")
                for move in newPath:
                    print(f"move {move}")
                return 
        print("Error: maxnodes limit (" + str(maxNodes) + ") reached")
            
    def bfs(self, maxNodes=1000):
        q = deque([(self.state, [])])
        numNodes = 1
        while q and numNodes < maxNodes:
            current, path = q.popleft()

            if current == ['0', '1', '2', '3', '4', '5', '6', '7', '8']:
                print("Nodes created during search: " + str(numNodes))
                print("Solution length: " + str(len(path)))
                print("Move sequence: " + ' '.join(path))
                return

            for move in ["left", "right", "up", "down"]:
                child = State()
                child.setState(copy.deepcopy(current))

                zeroIndex = child.findZero()
                x, y = divmod(zeroIndex, 3)

                if(move == "left" and y > 0) or (move == "right" and y < 2) or (move == "up" and x > 0) or (move == "down" and x < 2):
                    child.move(move)
                    newPath = path + [move]
                    q.append((child.state, newPath))
                    numNodes += 1
                    if child.state == ['0', '1', '2', '3', '4', '5', '6', '7', '8']:
                        print("Nodes created during search: " + str(numNodes))
                        print("Solution length: " + str(len(newPath)))
                        print("Move sequence: ")
                        for move in newPath:
                            print(f"move {move}")
                        return
        print("Error: maxnodes limit (" + str(maxNodes) + ") reached")

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
                if len(resultArray) == 1:
                    if(resultArray[0] == "BFS"):
                        self.bfs()
                        return
                    if(resultArray[0] == "DFS"):
                        self.dfs()
                        return
                    else:
                        print("Error: invalid solve command, must be BFS or DFS")
                        return
                elif(len(resultArray) == 2):
                    algo = resultArray[0]
                    maxNodes = resultArray[1][9:]
                    if algo not in ["BFS", "DFS"]:
                        print("Error: invalid solve command, must be BFS or DFS")
                        return
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
                else:
                    print("invalid solve command, must be BFS or DFS")
                    return
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