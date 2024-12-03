import sys
import time


# This file should contain your code. It'll be invoked via
# python3 sliding.py <board file> <goal file>
# and should print the output or -1. E.g.,
# print("0 0 0 0")
# or
# print("-1")


class Board:  # class for the current State of the Board
    def __init__(self, blocks, moves, rows, cols):
        self.blocks = blocks  # list of block objects
        self.moves = moves  # 2d list of moves made to get to this state
        self.rows = rows  # height of the board
        self.cols = cols  # width of the board

    def __hash__(self):  # creates unique "code" for each board as an integer, using the list of blocks
        # sorting the blocks ensures that states with the same blocks, in different orders have the same hash value
        default = sorted((block.length, block.width, block.row, block.col) for block in self.blocks)
        self.hash = hash(tuple(default))  # only immutable objects can be hashed - default must be a tuple
        return self.hash

    def isNewState(self, blockIndex, newRow, newCol, seenStates):  # checks state is not already processed
        prevRow, prevCol = self.blocks[blockIndex].row, self.blocks[blockIndex].col  # saves previous block position
        self.blocks[blockIndex].row = newRow  # updates to new position temporarily
        self.blocks[blockIndex].col = newCol

        newHash = hash(self)

        self.blocks[blockIndex].row = prevRow  # restores original position
        self.blocks[blockIndex].col = prevCol
        hash(self)  # restores hash

        if newHash not in seenStates:  # if it's an unseen state,
            seenStates.update({newHash: newHash})  # add to collection
            return True
        return False  # otherwise return false since it's been seen before

    def isSolution(self, other):
        for block in other.blocks:  # loops through goal blocks
            if block not in self.blocks:  # if one of the goals isn't met,
                return False  # it can't have found the solution
        return True  # all goal blocks found :)

    def printSolution(self):
        for move in self.moves:
            print(" ".join(map(str, move)))


class Block:  # class for block objects
    def __init__(self, length, width, row, col):
        self.length = length  # dimensions of block
        self.width = width
        self.row = row  # position of block on the board
        self.col = col

    def __eq__(self, other):  # ensures blocks with the same dimensions and position are recognised as the same object
        return self.length == other.length and self.width == other.width and self.row == other.row and self.col == other.col


def bfs(initialState, goalState):  # breath first search of possible board states
    start = time.time()
    seenStates = {hash(initialState): initialState.hash}  # adds first state to seen, dict is accessed in O(1)
    queue = [initialState]  # initial state goes to the front of the queue
    while len(queue) > 0:  # queue isn't empty, there are still states to explore
        end = time.time()
        if end - start > 60:
            print(-1)
            return False  # time out after 60 seconds
        boardState = queue.pop(0)  # fetch and remove item at front of queue
        if boardState.isSolution(goalState):  # checks if goal is reached
            boardState.printSolution()  # prints moves to get to goal from the first state
            return True
        else:
            collisionBoard = makeCollisionBoard(boardState)  # 2d list showing which board cells are occupied by blocks
            counter = 0  # counts position in array of blocks
            for block in boardState.blocks:  # loop through all blocks in current state
                length, width, row, col = block.length, block.width, block.row, block.col  # get block attributes
                # checks if block can move up
                if checkMove(boardState, row - 1, col, width, collisionBoard, "upDown"):
                    if boardState.isNewState(counter, row - 1, col, seenStates):
                        newState = createNewState(counter, boardState, row - 1, col)
                        queue.append(newState)  # adds new state to back of queue
                # checks if block can move down
                if checkMove(boardState, row + length, col, width, collisionBoard, "upDown"):
                    if boardState.isNewState(counter, row + 1, col, seenStates):
                        newState = createNewState(counter, boardState, row + 1, col)
                        queue.append(newState)
                # checks if block can move left
                if checkMove(boardState, row, col - 1, length, collisionBoard, "leftRight"):
                    if boardState.isNewState(counter, row, col - 1, seenStates):
                        newState = createNewState(counter, boardState, row, col - 1)
                        queue.append(newState)
                # checks block can move right
                if checkMove(boardState, row, col + width, length, collisionBoard, "leftRight"):
                    if boardState.isNewState(counter, row, col + 1, seenStates):
                        newState = createNewState(counter, boardState, row, col + 1)
                        queue.append(newState)

                counter += 1
    else:  # if the queue is empty
        print(-1)  # then no solution exists
        return True


def checkMove(boardState, newRow, newCol, side, collisionBoard, direction):
    if direction == 'upDown':
        changeRow = 0
        changeCol = 1
    else:
        changeRow = 1
        changeCol = 0

    for cell in range(side):
        if not isCellFree(newRow + cell*changeRow, newCol + cell*changeCol, boardState, collisionBoard):
            return False
    return True


def isCellFree(row, col, boardState, collisionBoard):
    if row < 0 or row > boardState.rows - 1:  # checks cell isn't out the bounds of the board
        return False
    elif col < 0 or col > boardState.cols - 1:
        return False
    else:
        return collisionBoard[row][col] is False  # checks cell isn't taken


def createNewState(blockIndex, prevBoardState, newRow, newCol):
    newBlocks = [block for block in prevBoardState.blocks]  # shallow copy of the block list
    prevBlock = prevBoardState.blocks[blockIndex]  # gets attributes of current position
    length, width = prevBlock.length, prevBlock.width
    movedBlock = Block(length, width, newRow, newCol)  # makes new block object for new position
    newBlocks[blockIndex] = movedBlock  # swaps out the block

    newMoves = [move for move in prevBoardState.moves]  # shallow copy of moves
    newMoves.append([prevBlock.row, prevBlock.col, newRow, newCol])  # records move

    newState = Board(newBlocks, newMoves, prevBoardState.rows, prevBoardState.cols)  # makes new state
    hash(newState)
    return newState


def makeCollisionBoard(boardState):  # creates map of positions of blocks on the board
    collisionBoard = [[False] * boardState.cols for i in range(boardState.rows)]  # false for empty
    for block in boardState.blocks:
        for row in range(block.row, block.row + block.length):  # loops through rows that a block occupies
            for col in range(block.col, block.col + block.width):  # loops through columns that a block occupies
                collisionBoard[row][col] = True  # true for occupied
    return collisionBoard


def createInitialState(f):  # reads board file
    file = open(f, "r")
    rows, columns = map(int, file.readline().split())  # reads first line
    blocks = []
    for line in file:
        length, width, bRow, bCol = map(int, line.split())  # reads each block line
        blocks.append(Block(length, width, bRow, bCol))  # creates block object
    file.close()
    return Board(blocks, [], rows, columns)  # creates board object


def readGoalFile(f):
    file = open(f, "r")
    blocks = []
    for line in file:
        length, width, bRow, bCol = map(int, line.split())
        blocks.append(Block(length, width, bRow, bCol))
    file.close()
    return blocks


def main(boardFile, goalFile):
    initialState = createInitialState(boardFile)

    goalBlocks = readGoalFile(goalFile)
    goalState = Board(goalBlocks, None, initialState.rows, initialState.cols)  # creates goal board

    return bfs(initialState, goalState)


#main(sys.argv[1], sys.argv[2])
