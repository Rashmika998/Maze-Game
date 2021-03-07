import queue
import time
import csv
from os import system, name 

#this programme will not check if there's a path exist in the given maze. It will print the shortest path which exists as it is asked to print the relevant
#path(after each step and final path) and not to check it and print.

filename = "maze3.csv" #input file name

#function to clear the terminal
def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 
  
#function to create a maze from (input) csv file
def createMaze():
    maze = []

    with open(filename,'r') as csvfile:
        csvreader = csv.reader(csvfile)

        for row in csvreader:
            maze.append(row)

    return maze

#function to display the maze
def displayMaze(maze, path=""):
    for a in range(len(maze)):
        for x, pos in enumerate(maze[a]):
            if pos == "S":
                startCol = x #column no where 'S' exists
                startRow = a  #row no where 'S' exists

            #change '1' in the file to '.' which represents the road
            if maze[a][x] == "1":
                maze[a][x] = "."

    clear() #clear the terminal

    for r, row in enumerate(maze):
            for c, col in enumerate(row):
                print(col + " ", end="")
            print()
    time.sleep(1)

    i = startCol
    j = startRow
    posRobot = set() #list consists of position of the robot
    finalPath = set() #list to display the final path
    posRobot.add((j, i))
    clear()
    
    for r, row in enumerate(maze):
            for c, col in enumerate(row):
                if (r, c) in posRobot:
                    print("R ", end="")
                else:
                    print(col + " ", end="")
            print()
    print()
    time.sleep(1)

    #check whether the coordinate is valid(no brick) and add it to the two lists
    for move in path:
        clear()
        posRobot.clear()
        if move == "L":
            i -= 1

        elif move == "R":
            i += 1

        elif move == "U":
            j -= 1

        elif move == "D":
            j += 1
        
        posRobot.add((j, i))
        finalPath.add((j,i))
  
        #display the robot path in each step
        for r, row in enumerate(maze):
            for c, col in enumerate(row):
                if (r, c) in posRobot:
                    print("R ", end="")
                else:
                    print(col + " ", end="")
            print()
        
        print()
        time.sleep(1)
    
    time.sleep(1)
    clear()
    print("\n\n\t\tROBOT HAS REACHED THE DESTINATION AND THE PATH IS\n")
    time.sleep(2)

    #display the final path indicating '+' sign
    for r, row in enumerate(maze):
            for c, col in enumerate(row):
                if (r, c) in finalPath and maze[r][c]!="D" :
                    print("+ ", end="")

                else:
                    print(col + " ", end="")
            print()
    print()    

#function to check whether the path is valid(check whether there is a brick/border/road) 
def validPath(maze, moves):
    for a in range(len(maze)):
        for x, pos in enumerate(maze[a]):
            if pos == "S":
                startCol = x #column no where 'S' exists
                startRow = a  #row no where 'S' exists

       
    i = startCol
    j = startRow
    for move in moves:
        if move == "L":
            i -= 1

        elif move == "R":
            i += 1

        elif move == "U":
            j -= 1

        elif move == "D":
            j += 1

        #if the path exceeds the boundary return False
        if not(0 <= i < len(maze[0]) and 0 <= j < len(maze)):
            return False

        #if there is a brick return False
        elif (maze[j][i] == "0"):
            return False

    return True


#function to find the destination
def findEnd(maze, moves):
    for a in range(len(maze)):
        for x, pos in enumerate(maze[a]):
            if pos == "S":
                startCol = x #column no where 'S' exists
                startRow = a  #row no where 'S' exists

    i = startCol
    j = startRow

    for move in moves:
        if move == "L":
            i -= 1

        elif move == "R":
            i += 1

        elif move == "U":
            j -= 1

        elif move == "D":
            j += 1

    #if the destination is found, then print and display the maze and return True and if not return False
    if maze[j][i] == "D":
        displayMaze(maze, moves)
        return True

    return False


#main function
a_file = open("welcome.txt")

lines = a_file.readlines()
clear()
for line in lines:
    print("\t\t\t\t\t"+line,end="")

input("\t\t\t\t\t\t\t  Press Enter to continue...")

path = queue.Queue() #create a queue of paths
path.put("") #add a blank string to it
currentPath = "" #stores the current path as a string("LRDDU..")
maze  = createMaze() #create a maze
    
#loop through whole map until the destination is found
while not findEnd(maze, currentPath): 
    currentPath = path.get() #get the first element of the queue
    for j in ["L", "R", "U", "D"]:
        if not(currentPath == ""):
            #neglect some steps such as when previous step is 'L' and current step is 'R' where there is a valid path to again 'L' from
            # 'R' without a brick.

            if j == "L" and currentPath[-1] == "R":
                continue

            elif j == "R" and currentPath[-1] == "L":
                continue

            elif j == "U" and currentPath[-1] == "D":
                continue

            elif j == "D" and currentPath[-1] == "U":
                continue


        tempPath = currentPath + j #add the one of the path to the temporary path 

        #check whether the added path(temporary path) is valid and if so add it to the queue
        if validPath(maze, tempPath):
            path.put(tempPath)