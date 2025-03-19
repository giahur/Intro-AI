"""
File: State.py
Author: Gia Hur (gxh221)
Due: 09/02/2024
"""

import random

class State:
    def __init__(self):
        self.state = "0 1 2 3 4 5 6 7 8"
        random.seed(221) # for scrambleState
        
    def setState(self, state):
        if(len(state) != 9) or (set(state) != set("012345678")):
            print("Error: invalid puzzle state")
        else:
            self.state = state
            print("Puzzle state set")
            #self.printState()

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
            x, y = divmod(zeroIndex, 3) # essentially finds coordinates of values

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
            print("Move successful")
            #self.printState()
            return True

    def scrambleState(self, n):
        if(len(n) != 1) or not (n[0].isdigit()):
            print("Error: invalid number of scrambles, must be integer")
        else: 
            for i in range(int(n[0])): # until n VALID moves made
                valid = False
                while not valid:
                    valid = self.move(random.choice(["left", "right", "up", "down"]))
            print("Puzzle scrambled")
            #self.printState()

    def cmd(self, commandString: str):
        resultArray = commandString.split()
        stringName = resultArray[0]
        resultArray.pop(0)

        match stringName:
            case "setState":
                self.setState(resultArray)
            case "printState":
                self.printState()
            case "move" :
                if len(resultArray) != 1:
                    print("Error: invalid move, must be 'left', 'right', 'up', 'down'")
                else:
                    self.move(resultArray[0])
            case "scrambleState":
                self.scrambleState(resultArray)
            case "#" | "//":
                pass
            case _:
                s = "Error: invalid command: " + stringName + " " + ' '.join(resultArray)
                print(s)
    
    def cmdfile(self, fileName):
        try:
            with open(fileName, 'r') as file: # read mode
                for line in file:
                    line = line.strip() # remove trailing, leading whitespace
                    if line: 
                        self.cmd(line)
        except FileNotFoundError:
            print("Error: file not found")

def main():
    hw1 = State()
    hw1.cmdfile("testcmds.txt")

if __name__=="__main__":
    main()