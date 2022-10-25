import pygame
import pygame_gui
from colors import *
from main import *

APPLICATION_TITLE = "8 Puzzle Solver Using BFS & ASTAR Algo"

ALERTLABELEVENT = pygame.USEREVENT + 2

pygame.init()

BASICFONT = pygame.font.SysFont('Arial Bold', BASICFONTSIZE)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# The UI manager handles calling the update, draw and event handling
manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT),'theme.json')

pygame.display.set_caption(APPLICATION_TITLE)

class Tile:

    def __init__(self, number, tile_width, tile_height, index_x, index_y):
        self.number = number
        self.x = 0
        self.y = 0
        self.width = tile_width
        self.height = tile_height
        self.index_x = index_x
        self.index_y = index_y

    # returns a tuple of 4 values for the purpose of drawing
    def tileStats(self):
        return self.x, self.y, self.width, self.height

# a rect object to store the information for Rects used to create buttons
class ButtonRect:
    def __init__(self, id, ):
        self.Rect = pygame.Rect(
            (WINDOW_WIDTH - BUTTON_AREA_WIDTH + BUTTON_MARGIN, id * BUTTON_HEIGHT + 1),
            (BUTTON_WIDTH, BUTTON_HEIGHT))
        self.id = id

def alert_label(message):
    alertLabel.set_text(message)
    pygame.time.set_timer(ALERTLABELEVENT, WAIT_TIME)

def newState(state):
    gameState = GameState(None, None, state, 0)
    stateStr = str(gameState)
    initial_tiles_list = []

    # the tile that will be left blank - represented by 0
    blankTileLocal = Tile("0", TILE_WIDTH - 2, TILE_HEIGHT - 2, 0, 0)

    for i, num in enumerate(stateStr):
        index_x = (i // 3)
        index_y = (i % 3)

        if num != '0':
            tile = Tile(num, TILE_WIDTH - 2, TILE_HEIGHT - 2, index_x, index_y)
            tile.x = index_y * TILE_WIDTH + 1
            tile.y = index_x * TILE_HEIGHT + 1

            initial_tiles_list.append(tile)
        else:
            blankTileLocal.x = index_y * TILE_WIDTH + 1
            blankTileLocal.y = index_x * TILE_HEIGHT + 1
            blankTileLocal.index_x = index_x
            blankTileLocal.index_y = index_y
            initial_tiles_list.append(blankTileLocal)

    return gameState, initial_tiles_list, blankTileLocal

# swap blank tile and target tile
def updateBoard(direction):
    i, j = blankTile.index_x, blankTile.index_y
    list_index = 0
    if direction == 'Left':
        list_index = i * 3 + (j - 1)
    elif direction == 'Up':
        list_index = (i - 1) * 3 + j
    elif direction == 'Down':
        list_index = (i + 1) * 3 + j
    elif direction == 'Right':
        list_index = i * 3 + (j + 1)

    target_tile = numbered_tiles_list[list_index]
    blankTile_list_index = i * 3 + j

    # swapping location on board and index. 
    target_tile.x, blankTile.x = blankTile.x, target_tile.x
    target_tile.y, blankTile.y = blankTile.y, target_tile.y
    target_tile.index_x, blankTile.index_x = blankTile.index_x, target_tile.index_x
    target_tile.index_y, blankTile.index_y = blankTile.index_y, target_tile.index_y

    # swap the blank tile and target tile in the tile list.
    numbered_tiles_list[list_index], numbered_tiles_list[blankTile_list_index] \
        = numbered_tiles_list[blankTile_list_index], numbered_tiles_list[list_index]

def swapTiles(mousePosition):
    x, y = mousePosition
    index_y = x // TILE_WIDTH
    index_x = y // TILE_HEIGHT

    # distance between blank tile and target tile in terms of x and y axis
    distance = abs(blankTile.index_x - index_x) + abs(blankTile.index_y - index_y)

    # there is a valid swap move
    if distance == 1:
        if blankTile.index_y < index_y: 
            updateBoard("Right")
        elif blankTile.index_y > index_y:  
            updateBoard("Left")
        elif blankTile.index_x < index_x:
            updateBoard("Down")
        elif blankTile.index_x > index_x:
            updateBoard("Up")

# Random tiles button
randomStateButtonRect = ButtonRect(4)
randomStateButton = pygame_gui.elements.UIButton(
    relative_rect=randomStateButtonRect.Rect, text="RANDOM", manager=manager
)
#Shows option for solution
solveChoiceRect = ButtonRect(5)
solveChoice = pygame_gui.elements.UIDropDownMenu(
    ["BFS", "A*"], "ALGORITHM",
    relative_rect=solveChoiceRect.Rect, manager=manager)

# Solves the puzzle button
solveButtonRect = ButtonRect(6)
solveButton = pygame_gui.elements.UIButton(
    relative_rect=solveButtonRect.Rect, text="SOLVE", manager=manager
)
#alerts if no solution found
alertLabelRect = ButtonRect(7)
alertLabel = pygame_gui.elements.UILabel(
    relative_rect=alertLabelRect.Rect, manager=manager, text=" "
)

initialState, numbered_tiles_list, blankTile = newState(12345678)
solutionExists = False
solutionStepsList = []
solutionIndex = 0

clock = pygame.time.Clock()

time_counter = 0
running = True
while running:

    time_delta = clock.tick(60) / 1000
    time_counter += time_delta * 1000

    # when a solution exists, start updating the board
    if time_counter > 500 / 1 and solutionExists:
        updateBoard(solutionStepsList[solutionIndex].move)
        time_counter = 0
        solutionIndex += 1
        if solutionIndex == len(solutionStepsList):
            solutionExists = False
            initialState, numbered_tiles_list, blankTile = newState(12345678)
            solutionStepsList = []
            
    events = pygame.event.get()

    for event in events:    
        # specific to the UI library. all events related to pygame_gui go here
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == randomStateButton:
                    state = random_game_state()
                    initialState, numbered_tiles_list, blankTile = newState(state)
                    solveButton.enable()
                    solutionExists = False
                elif event.ui_element == solveButton:
                    if initialState.state != goalState:
                        type_of_search = solveChoice.selected_option
                        answer = solution(initialState, type_of_search)
                        path_to_goal = iterative_get_path_(answer)
                        solveButton.disable()
                        if path_to_goal:
                            solutionExists = True
                            solutionIndex = 0
                            solutionStepsList = path_to_goal[1:]
                        else:  
                            alert_label("No solution!")     
                            solveButton.enable()

        if event.type == ALERTLABELEVENT:
            alertLabel.set_text(" ")
            pygame.time.set_timer(ALERTLABELEVENT, 0)

        if event.type == pygame.QUIT:
            running = False
            break

        manager.process_events(event)


    manager.update(time_delta)
    window.fill(BACKGROUND_COLOR)

    # Draw rectangles representing the tiles of the 8-puzzle except blank
    for tile in numbered_tiles_list:
        pygame.draw.rect(window, PURPLE, tile.tileStats())

        # display the tile number on the tile as text
        textSurf = BASICFONT.render(tile.number, True, WHITE, PURPLE)
        textRect = textSurf.get_rect()
        textRect.center = tile.x + TILE_WIDTH // 2, tile.y + TILE_HEIGHT // 2
        window.blit(textSurf, textRect)

    pygame.draw.rect(window, BACKGROUND_COLOR, blankTile.tileStats())


    manager.draw_ui(window)
    pygame.display.update()


pygame.quit()
