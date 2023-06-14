import random
import numpy as ny
import pygame
import pickle
import sys
import math


NO_ROWS = 6
NO_COLUMNS = 7

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
NAME_YELLOW = (245, 190, 0)
BLACK = (0, 0, 0)

'''
Indexes for the Connect 4 Board:

(3,0) (3,1) (3,2) (3,3)
(2,0) (2,1) (2,2) (2,3)
(1,0) (1,1) (1,2) (1,3)
(0,0) (0,1) (0,2) (0,3)
'''



# Connect 4 Functions

def win_exists(board, player):
    # Horizontal Win
    for row in board:
        for tile in range(NO_COLUMNS - 3): # To not try and access indices outside the list
            if row[tile] == player and row[tile + 1] == player and row[tile + 2] == player and row[tile + 3] == player:
                return True
            
    # Vertical Win
    for column in range(NO_COLUMNS):
        for row in range(NO_ROWS - 3): # To not try and access indices outside the list
            if board[row][column] == player and board[row + 1][column] == player and board[row + 2][column] == player and board[row + 3][column] == player:
                return True

    # Positive Diagonal Win
    for column in range(NO_COLUMNS - 3): # To not try and access indices outside the list
        for row in range(NO_ROWS - 3): # To not try and access indices outside the list
            if board[row][column] == player and board[row + 1][column + 1] == player and board[row + 2][column + 2] == player and board[row + 3][column + 3] == player:
                return True

    # Negative Diagonal Win
    for column in range(NO_COLUMNS - 3): # To not try and access indices outside the list
        for row in range(3, NO_ROWS): # Starting from 3rd row so we can count down and right to check for connects
            if board[row][column] == player and board[row - 1][column + 1] == player and board[row - 2][column + 2] == player and board[row - 3][column + 3] == player:
                return True 

    else:
        return False

def board_create(): # Create a nested list of zeros to represent the board
    board = ny.zeros((NO_ROWS, NO_COLUMNS))
    return board

def next_open_row(board, column): # Returns the index of the row with an empty slot
    for row in range(NO_ROWS):
        if board[row][column] == 0:
            return row
    else:
        pass # Account for filled column!

def is_valid_column(board, column):
    if column >= NO_COLUMNS:
        return False
    elif board[NO_ROWS - 1][column] == 0:
        return True
    else:
        return False

def draw_board(board):
    board = ny.flipud(current_board)
    for c in range(NO_COLUMNS):
        for r in range(NO_ROWS):
            pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + 2 * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if board[r][c] == 0:
                pygame.draw.circle(screen, WHITE, (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + 2 * SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)
            elif board[r][c] == 1:
                pygame.draw.circle(screen, RED, (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + 2 * SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + 2 * SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)
                
    pygame.display.update()



# Tournament Functions

def perfect_player_count(count):
    while count >= 1:
        if count == 1:
            return True
        count /= 2

    return False

def player_details():
    with open("Players.dat", "wb") as players:
        while True:
            try:
                n = int(input("How many players will participate? (power of 2 only for perfect pairing) "))
                if perfect_player_count(n):  # If user count is an power of 2 for perfect pairing
                    names = []
                    player_ids = []
                    for i in range(n):
                        while True:
                            name = input("Player " + str(i + 1) + " (Please limit length of name to 12 letters) : ")
                            if len(name) < 13:
                                break
                            else:
                                print("Please limit length of name to 5 letters")
                        names.append(name)
                        player_ids.append(i + 1)
                    random.shuffle(names)  # To randomize pairings
                    matchings = dict(zip(player_ids, names)) # Each name will correspond to a matching player_id
                    pickle.dump(matchings, players)
                    break
                else:
                    continue
            except:
                continue


def id_to_pairings(ids):
    pairings = []
    match = []
    if len(ids) == 1:
        return False
    for i in range(len(ids)):
        if (i + 1) % 2 == 0:
            match.append(ids[i])
            pairings.append(match)
            match = []
        else:
            match.append(ids[i])
    return pairings


def id_to_name(id_value):
    for i in range(len(participant_ids)):
        if i == id_value:
            return participants[i]



    
if __name__ == "__main__":
    current_board = board_create()
    print(ny.flipud(current_board))

    tournament_over = False
    turn = 0 # Keeps a track of whose turn it is

    pygame.init()

    SQUARE_SIZE = 100
    RADIUS = SQUARE_SIZE // 2 - 5

    width = NO_COLUMNS * SQUARE_SIZE
    height = (NO_ROWS + 2) * SQUARE_SIZE + 50 # A row for header, a row to chose where to drop the tile, and a small row at the bottom for column counts

    size = (width, height)

    screen = pygame.display.set_mode(size)
    draw_board(current_board)
    myfont = pygame.font.SysFont("monospace", 40)

    # Creating tournament pairings

    player_details()
    
    with open("Players.dat", "rb") as players:
        participants = pickle.load(players)
        
    print(participants)
    initial_pairings = id_to_pairings(list(participants.keys()))
    current_round = initial_pairings
    print("Participant IDs:", str(list(participants.keys())))
    print("Initial Pairings:", str(initial_pairings))

    while not tournament_over:

        next_round = []

        for i in current_round:

            winner_exists = False # To stop the while loop when winner is found

            winner = 0

            pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARE_SIZE))
            pygame.draw.rect(screen, WHITE, (0, 0, width, 2 * SQUARE_SIZE))
            pygame.display.update()

            # Display Current Game Match Up
            while True:
                label = myfont.render(participants[i[0]] + " vs " + participants[i[1]], 1, GREEN)
                text_rect = label.get_rect(center = (width/2, 40))
                screen.blit(label, text_rect)
                pygame.display.update()
                clicked = False
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        clicked = True
                if clicked:
                    break
    
            while not winner_exists: # Play until there's a winner

                for event in pygame.event.get():
                    pygame.draw.rect(screen, BLUE, (0, height - 50, width, SQUARE_SIZE))
                    
                    subfont = pygame.font.SysFont("monospace", 10)

                    label = subfont.render("By Faheem and Rohan", 1, BLACK)
                    text_rect = label.get_rect(center = (width - 60, height - 15))
                    screen.blit(label, text_rect)

                    subfont = pygame.font.SysFont("monospace", 40)
                    
                    label = subfont.render("1", 1, WHITE)
                    text_rect = label.get_rect(center = (SQUARE_SIZE / 2, height - 35))
                    screen.blit(label, text_rect)
                    
                    label = subfont.render("2", 1, WHITE)
                    text_rect = label.get_rect(center = ((SQUARE_SIZE / 2) + (SQUARE_SIZE * 1), height - 35))
                    screen.blit(label, text_rect)
                    
                    label = subfont.render("3", 1, WHITE)
                    text_rect = label.get_rect(center = ((SQUARE_SIZE / 2) + (SQUARE_SIZE * 2), height - 35))
                    screen.blit(label, text_rect)
                    
                    label = subfont.render("4", 1, WHITE)
                    text_rect = label.get_rect(center = ((SQUARE_SIZE / 2) + (SQUARE_SIZE * 3), height - 35))
                    screen.blit(label, text_rect)
                    
                    label = subfont.render("5", 1, WHITE)
                    text_rect = label.get_rect(center = ((SQUARE_SIZE / 2) + (SQUARE_SIZE * 4), height - 35))
                    screen.blit(label, text_rect)
                    
                    label = subfont.render("6", 1, WHITE)
                    text_rect = label.get_rect(center = ((SQUARE_SIZE / 2) + (SQUARE_SIZE * 5), height - 35))
                    screen.blit(label, text_rect)
                    
                    label = subfont.render("7", 1, WHITE)
                    text_rect = label.get_rect(center = ((SQUARE_SIZE / 2) + (SQUARE_SIZE * 6), height - 35))
                    screen.blit(label, text_rect)
                    
                    if event.type == pygame.QUIT:
                        sys.exit()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        print(event.pos)
                        xval = event.pos[0]
                        column = xval // SQUARE_SIZE
                        pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARE_SIZE))
                        
                        if turn == 0: # Player 1's Turn
                            print(participants[i[0]] + "'s Turn")
                            if is_valid_column(current_board, column):
                                # Dropping the piece for P1
                                # Retrieves next free row using next_open_row function
                                current_board[next_open_row(current_board, column)][column] = 1
                                
                                if win_exists(current_board, 1): # Winner Detection
                                    winner = i[0]
                                    next_round.append(winner)
                                    label = myfont.render(participants[i[0]] + " wins!!", 1, RED)
                                    text_rect = label.get_rect(center = (width/2, 40))
                                    screen.blit(label, text_rect)
                                    winner_exists = True
                                

                        else: # Player 2's Turn
                            print(participants[i[1]] + "'s Turn")
                            if is_valid_column(current_board, column):
                                # Dropping the piece for P2
                                # Retrieves next free row using next_open_row function
                                current_board[next_open_row(current_board, column)][column] = 2

                                if win_exists(current_board, 2): # Winner Detection
                                    winner = i[1]
                                    next_round.append(winner)
                                    label = myfont.render(participants[i[1]] + " wins!!", 1, NAME_YELLOW)
                                    text_rect = label.get_rect(center = (width/2, 40))
                                    screen.blit(label, text_rect)
                                    winner_exists = True

                        turn += 1
                        turn %= 2 # Converts 2 to 0 and keeps 1 as 1

                        draw_board(current_board)
                        print(ny.flipud(current_board)) # Print board flipped across x- axis

                        if winner_exists:
                            pygame.time.wait(3000)
                        
                    if event.type == pygame.MOUSEMOTION: # To track the mouse          
                        pygame.draw.rect(screen, WHITE, (0, 0, width, 2 * SQUARE_SIZE)) # To erase the earlier drawn circle
                        posx = event.pos[0]

                        # Display which player's turn
                        if turn == 0:   
                            label = myfont.render(participants[i[0]] + "'s Turn", 1, RED)
                            text_rect = label.get_rect(center = (width/2, 40))
                            screen.blit(label, text_rect)
                            
                        else:
                            label = myfont.render(participants[i[1]] + "'s Turn", 1, NAME_YELLOW)
                            text_rect = label.get_rect(center = (width/2, 40))
                            screen.blit(label, text_rect)
                        
                        # Draw a red/yellow circle (depending on whose turn it is) at the x-value of the mouse above the board
                        if turn == 0:
                            pygame.draw.circle(screen, RED, (posx, (SQUARE_SIZE + SQUARE_SIZE // 2)), RADIUS)
                        else:
                            pygame.draw.circle(screen, YELLOW, (posx, (SQUARE_SIZE + SQUARE_SIZE // 2)), RADIUS)
                            
                    pygame.display.update()
                        

            current_board = board_create()
            draw_board(current_board)
            print("Next Round:", str(next_round))

        current_round = id_to_pairings(next_round)
        print("Current Round:", str(current_round))
        if not current_round:
            tournament_over = True
            
            subfont = pygame.font.SysFont("monospace", 45)
            pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARE_SIZE))
            label = subfont.render((participants[next_round[0]] + " wins overall!"), 1, RED)
            text_rect = label.get_rect(center = (width/2, 40))
            screen.blit(label, text_rect)
            pygame.display.update()
            
            print("Congratulations", participants[next_round[0]] + "! You win the tournament!")

sys.exit()
print("Thank you for running our game :D")
