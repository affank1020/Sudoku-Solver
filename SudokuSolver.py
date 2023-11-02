from ctypes import sizeof
from ctypes.wintypes import tagRECT
import math
from multiprocessing.heap import Arena
from operator import truediv 

def LookFor(target, row, col):
    targetFound = False
    #print("Looking for ", target)
    for r in range(row, row + area):
        for c in range(col, col + area):
            #print("Checking - Row: ", r, " Column: ", c, end='')
            if (grid[r][c] == target):
                #print(' - Target is already in area')
                targetFound = True
            #else:
                #print(' - Not here')  
                
    return targetFound

def AreaCoords(areaNum):
    startRow = 0
    startCol = 0
    if (areaNum == 1):
        return startRow, startCol
    else:
        for i in range(1, areaNum):
            startCol += area
            if (startCol >= size):
                startCol = 0
                startRow += area
        return startRow, startCol

def IsSquareEmpty(row, col):
    if(grid[row][col] == 0):
        return True
    else:
        return False

def CheckRow(rowToCheck, target):
    for c in range(0, size):
        #print("Checking - Row: " + str(rowToCheck) + " Column: " + str(c), end='')
        if (grid[rowToCheck][c] == target):
            #print(" - Target is already in row")
            return True
        #else:
            #print(" - Not here")
    return False

def CheckCol(colToCheck, target):
    for r in range(0, size):
        #print("Checking - Row: " + str(r) + " Column: " + str(colToCheck), end='')
        if (grid[r][colToCheck] == target):
            #print(" - Target is already in column")
            return True
        #else:
            #print(" - Not here")
    return False

def ShowGrid(grid):
    for row in grid:
        print(row)
def FindMyArea(curRow, curCol):
    across = (curCol // 3)
    down = (curRow // 3)
    areaCode = 1 + (down * 3) + across
    return areaCode

grid = [[0, 0, 0, 1], [0, 2, 0, 0], [0, 0, 4, 0], [3, 0, 0, 0]]
grid = [[7, 0, 0, 0, 3, 4, 8, 0, 0], [8, 0, 4, 6, 0, 0, 0, 0, 0], [0, 3, 9, 0, 5, 0, 0, 0, 0], [1, 0, 0, 5, 0, 0, 6, 0, 0], [0, 4, 0, 7, 0, 9, 0, 3, 0], [0, 0, 3, 0, 0, 8, 0, 0, 9], [0, 0, 0, 0, 7, 0, 3, 2, 0], [0, 2, 6, 0, 0, 1, 9, 0, 5], [0, 0, 7, 9, 2, 0, 0, 0, 4]]

b = True
while (b):
    size = len(grid)
    area = int(math.sqrt(size))
    ShowGrid(grid)

    print("1: Input new grid")
    print("2: Solve puzzle")
    print("3: Exit")
    choice = input("Enter choice: ")

    if (choice == str(1)):
        grid.clear()
        dimensions = input("Enter the side length dimensions: ")
        print("Enter each row of numbers, using a 0 for blank spaces")
        for i in range(0, int(dimensions)):
            nums = input()
            while (len(nums) != int(dimensions)):
                nums = input("Input should be " + dimensions + " numbers long: ")
            numArr = [*nums]
            for i in range(0, len(numArr)):
                numArr[i] = int(numArr[i])
            grid.append(numArr)

    elif (choice == str(2)):
        updated = True
        for i in range(0, 50):
            for curNum in range(1, size + 1): #Change to size + 1
                print("----------------------")
                print("Placing Target: " + str(curNum))
                for a in range(1, size + 1):
                    print("-------------------")
                    print("Searching Area: " + str(a))
                    row = AreaCoords(a)[0]
                    col = AreaCoords(a)[1]
                    exists = LookFor(curNum, row, col)
                    if (exists == False):
                        print("Target: " + str(curNum) + " is not in Area: " + str(a))
                        print("")
                        print("Checking possible placements for target: " + str(curNum) + " in area: " + str(a))

                        #Create an empty list to store possible placement positions for target value
                        possiblePlacements = []

                        #Check each square in the current area
                        row = AreaCoords(a)[0]
                        col = AreaCoords(a)[1]
                        for r in range(row, row + area):
                            for c in range(col, col + area):
                                print("----Now verifying placement for row: " + str(r) + " col: " + str(c) + "----")
                                #If the square is empty
                                if(IsSquareEmpty(r, c)):
                                    #Check the entire row for the target value
                                    print("Checking row: " + str(r))
                                    existsInRow = CheckRow(r, curNum)

                                    #Check the entire column for the target value
                                    print("Checking column: " + str(r))
                                    existsInCol = CheckCol(c, curNum)

                                    #If the target value is not in either the entire row, nor the entire column we update the list and store that square position as a possible place to put the target value
                                    if(existsInRow == False and existsInCol == False):
                                        possiblePlacements.append([r, c])
                                        print("YES - So row: " + str(r) + " and col: " + str(c) + " is a possible placement")
                                    else:
                                        print("NO - Can't place target: " + str(curNum) + " in row: " + str(r) + " col: " + str(c))
                        
                        #After all squares have been checked for the area, we count how many possible placement positions are in the list. If there is only one possibility we can place the target value in the grid.
                        print("//////")
                        print("All squares in area: " + str(a) + " have been checked")
                        print("There are " + str(len(possiblePlacements)) + " possible placements")
                        if(len(possiblePlacements) == 1):
                            print("This means we can place target: " + str(curNum) + " in row: " + str(possiblePlacements[0][0]) + " col: " + str(possiblePlacements[0][1]))
                            grid[possiblePlacements[0][0]][possiblePlacements[0][1]] = curNum
                            ShowGrid(grid)
                            updated = True
                        else:
                            print("We can't place target: " + str(curNum) + " anywhere, checking other areas")
                            updated = False
                    else:
                        print("Target: " + str(curNum) + " is in Area: " + str(a))

        print("")
        print("")
        ShowGrid(grid)
        print("*********Now applying second algorithm*********")
        for i in range(0, 10):
            for r in range(0, size):
                for c in range(0, size):
                    if(IsSquareEmpty(r, c)):
                        possibleN = []
                        areaCode = FindMyArea(r, c)
                        startR = AreaCoords(areaCode)[0]
                        startC = AreaCoords(areaCode)[1]
                        for n in range(1, size):
                            if (CheckRow(r, n) == False and CheckCol(c, n) == False and LookFor(n, startR, startC) == False):
                                possibleN.append(n)

                        print("Values of n that can go in row: " + str(r) + " col: " + str(c) + " area:")
                        for num in possibleN:
                            print(num)
                        if(len(possibleN) == 1):
                            print("CAN PLACE - Since there is only 1 possible value")
                            grid[r][c] = possibleN[0]
                            ShowGrid(grid)


        print("")
        print("$$$$$$$$$$$$$$$$")
        print("Sudoku puzzle solved")
        ShowGrid()
        input("Press Enter to continue")
        

    elif (choice == str(3)):
        b = False
        print("Bye")