import heapq
import math
import time
from queue import Queue, PriorityQueue
import random

# Answer tracker
goalState = 12345678
maxDepth = 0
nodesExpanded = 1
isFound = False
runTime = 0

# Game state class
class GameState:
    def __init__(self, parent, move, state, depth, cost=0):
        self.parent = parent
        self.move = move
        self.state = state
        self.depth = depth
        self.cost = cost + self.depth

    def __eq__(self, another):
        return self.state == another.state

    def __str__(self):
        stateStr = str(self.state)  # Convert Parent state from integer to string
        # if 0 is first element it will add it to the string
        stateStr = stateStr if len(stateStr) > 8 else "0" + "".join(stateStr)
        return stateStr

    def __hash__(self):
        return hash(self.__str__())

    def __lt__(self, other):
        return self.cost < other.cost

def __get__children(parent):
    stateStr = parent.__str__()
    index = stateStr.index("0")  # get the index of the zero (Blank Space)
    row = int(index / 3)  # get  the row in which the blank space lies
    column = index % 3  # get  the column in which the blank space lies
    children = []
    if row == 0:
        # Move down only as first row elements can't go up the board
        children.append(GameState(parent, 'Down', __move__down(stateStr), parent.depth + 1))
    elif row == 1:
        # Move up and down
        children.append(GameState(parent, 'Down', __move__down(stateStr), parent.depth + 1))
        children.append(GameState(parent, 'Up', __move__up(stateStr), parent.depth + 1))
    else:
        # Move up only as first row elements can't down up the board
        children.append(GameState(parent, 'Up', __move__up(stateStr), parent.depth + 1))

    if column == 0:
        # Move right as as the element is at the far left
        children.append(GameState(parent, 'Right', __move__right(stateStr), parent.depth + 1))
    elif column == 1:
        # Move left and right
        children.append(GameState(parent, 'Left', __move__left(stateStr), parent.depth + 1))
        children.append(GameState(parent, 'Right', __move__right(stateStr), parent.depth + 1))
    else:
        # Move left as the element is at the far right
        children.append(GameState(parent, 'Left', __move__left(stateStr), parent.depth + 1))
    return children

# Breadth first search
def bfs(root):
    # start the timer
    start_time = time.time()
    # create a set for the explored and a queue containing the frontier states
    global nodesExpanded, maxDepth, isFound, runTime
    __reset__()
    explored = set()
    frontier = Queue()
    frontier.put(root)
    expanded = set()
    expanded.add(root)
    # iterate over frontier until goal is found or the tree is exhausted
    while not frontier.empty():
        node = frontier.get()
        explored.add(node)  # start exploring current state
        if node.state == goalState:
            isFound = True
            end_time = time.time()
            runTime = end_time - start_time
            return node  # if goal is found, exit and return state
        # else, start expanding by getting its children and enqueuing them
        children = __get__children(node)
        for child in children:
            if child not in expanded:
                frontier.put(child)
                expanded.add(child)
                nodesExpanded += 1
                maxDepth = maxDepth if maxDepth > child.depth else child.depth
    isFound = False
    end_time = time.time()
    runTime = end_time - start_time
    return

def __move__down(state):
    index = state.index('0')  # get the index of the zero (Blank Space)
    temp = state
    x = list(temp)  # Converting String to list for easier swap
    x[index], x[index + 3] = x[index + 3], x[index]
    temp = "".join(x)  # Converting the list back to string
    return int(temp)


def __move__up(state):
    index = state.index('0')  # get the index of the zero (Blank Space)
    temp = state
    x = list(temp)  # Converting String to list for easier swap
    x[index], x[index - 3] = x[index - 3], x[index]
    temp = "".join(x)  # Converting the list back to string
    return int(temp)


def __move__right(state):
    index = state.index('0')  # get the index of the zero (Blank Space)
    temp = state
    x = list(temp)  # Converting String to list for easier swap
    x[index], x[index + 1] = x[index + 1], x[index]
    temp = "".join(x)  # Converting the list back to string
    return int(temp)


def __move__left(state):
    index = state.index('0')  # get the index of the zero (Blank Space)
    temp = state
    x = list(temp)  # Converting String to list for easier swap
    x[index], x[index - 1] = x[index - 1], x[index]
    temp = "".join(x)  # Converting the list back to string
    return int(temp)

# saves iteratively the path into a list in order to display path in correct (non reversed) order
def iterative_get_path_(game_state):
    if game_state is not None:
        path = [game_state]
        i = 0
        while path[i].parent:
            path.append(path[i].parent)
            i += 1
        path.reverse()
        return path
    return False

# Reset all global variables
def __reset__():
    global nodesExpanded, maxDepth, runTime, isFound
    maxDepth = 0
    nodesExpanded = 1
    isFound = False
    runTime = 0

def random_game_state():
    str_var = list("123456780")
    random.shuffle(str_var)
    state = int(''.join(str_var))
    return state

def solution(gameState, algorithm):
    answer = None
    if algorithm == 'BFS':
        answer = bfs(gameState)
    if isFound:
        return answer
    else:
        return None