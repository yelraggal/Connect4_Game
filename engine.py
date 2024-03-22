import math
import random
import numpy as np
# from collections import defaultdict
import time

ROW_COUNT = 6
COLUMN_COUNT = 7

min_tree = {} # For agent (agent fills it and return it)
saved_states = {} # {state (string) : mintree {} }
 
def convert_from_string_to_grid(state):
    grid = [[0] * 7 for _ in range(6)]
    for i in range(0, 6):
        for j in range(0, 7):
            grid[i][j] = int(state[i * 7 + j]) 
    return grid

def convert_from_grid_to_string(grid):
    state = ""
    for i in range(0, 6):
        for j in range(0, 7):
            state += str(grid[i][j])
    return state

def drop_piece(state, col, piece): #byshof awl row fady fel column da
    # piece dy 3bra 3n eh
    for row in range(5, -1, -1):
        if state[row * 7 + col] == "0":
            newstate = (
                state[: row * 7 + col] + str(piece)[0] + state[row * 7 + col + 1 :]
            )
            break
    return newstate

def is_valid_location(state, col): # l string bymlha b row l fo2 l awl
    return state[col] == "0"


def get_valid_locations(state): # state here is string
    locations = [] # contains column l ynf3 ahot fyha
    for col in range(7):
        if is_valid_location(state, col):
            locations.append(col)
    return locations

def get_score(state, col, piece, depth, option):
    # state is string here
    # option 1 mini max  && option 2 is pruning && option 3 expected
    # piece 0 -> empty , 1 -->    , 2--> 

    # hna ana akni max w hnadi 3l min 
    # if (state in max_value_of_state): # check if we already calculate max value for this state before
    #     print("saved state")
    #     return max_value_of_state(state)
    next_state = drop_piece(state, col, piece)

    if option == 1: # minimax
        new_dict = {
            # this our NODE (dictionary representaion)
            next_state: {
                "depth": depth - 1,
                "value": 0,
                "childs": [],
            }
        }
        value = minimax(next_state, depth - 1, piece % 2 + 1, False, new_dict) # send false l2n da el child bta3i
        # new_dict[next_state]["value"] = value
        new_dict[next_state]["value"] = f"{value:.2f}"

        min_tree[state]["childs"].append(new_dict)
        # max_value_of_state[state]=value
        return value
    elif option == 2: # prune
        new_dict = {
            next_state: {
                "depth": depth - 1,
                "value": 0,
                "childs": [],
            }
        }
        value = minimax_alpha_beta(next_state, depth - 1, -math.inf, math.inf, piece % 2 + 1, False, new_dict)
        # new_dict[next_state]["value"] = value
        new_dict[next_state]["value"] = f"{value:.2f}"

        min_tree[state]["childs"].append(new_dict)
        return value
    else : # oprion 3 : Expected Minimax
        new_dict = {
            next_state: {
                "depth": depth - 1,
                "value": 0,
                "childs": [],
            }
        }
        value = expected_minimax(next_state, depth - 1, piece % 2 + 1, False, new_dict) # send false l2n da el child bta3i
        # new_dict[next_state]["value"] = value
        new_dict[next_state]["value"] = f"{value:.2f}"

        min_tree[state]["childs"].append(new_dict)
        return value



 
def evaluate_window(window, piece):
    score = 0
    if piece == 2 :
        opponent_piece=1
    else:
        opponent_piece=2

    opponent_consecutive = window.count(opponent_piece)
    consecutive_pieces = window.count(piece)
    free_slots = window.count(0)

    if consecutive_pieces == 4:
        score += 2000 # Win condition
    elif consecutive_pieces == 3 and free_slots == 1:
        score += random.randint(8,11)  # Strong winning opportunity
    elif consecutive_pieces == 2 and free_slots == 2:
        score += random.randint(1, 3)  # Potential winning connection


    if opponent_consecutive == 4:
        score -= 1000  # Win oponent condition
    # oponent 
    elif opponent_consecutive == 3 and free_slots == 1:
        score -= random.randint(8,11)
    elif opponent_consecutive == 2 and free_slots == 2:
        score -= random.randint(1,3)
    return score


def score_position(state, piece):
    score = 0
    piece=int(piece)
    # if (piece == 1):
    #     print("magdy")
    # if (piece ==2):
    #     print("red")
    board= convert_from_string_to_grid(state)
    board=np.array(board)

    WINDOW_LENGTH=4
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)
            if ( c in [3,4,5]): # to encorage to play in middle
                score+=score*2.3
                
   # Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score posiive sloped diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
    return score


def is_terminal(state):
    # Check for draw
    if "0" not in state:
        return True
    return False


def minimax(state, depth, piece, maximizingPlayer, tree): # state (parent node)
    # state is string here  ,  tree (NODE) (Dictionary) of same state
    # piece 
    global NODE_EXPANDED
    NODE_EXPANDED += 1

    if depth == 0 or is_terminal(state):
        value = score_position(state, piece)
        return value
    
    valid_location = get_valid_locations(state)
    if maximizingPlayer:
        val = -math.inf
        for col in valid_location:
            child = drop_piece(state, col, piece)
            new_dict = {
                child: {
                    "value": 0,
                    "childs": [],
                }
            }
            value = minimax(child, depth - 1, piece % 2 + 1, False, new_dict)
            if value > val :
                val=value
            new_dict[child]["value"] = f"{value:.2f}"
            tree[state]["childs"].append(new_dict)
        return val
    else: # minimizing player
        val = math.inf
        for col in valid_location:
            child = drop_piece(state, col, piece)
            new_dict = {
                child: {
                    "value": 0,
                    "childs": [],
                }
            }
            value =  minimax(child, depth - 1, piece % 2 + 1, True, new_dict)
            if value < val:
                val=value

            new_dict[child]["value"] = f"{value:.2f}"            
            tree[state]["childs"].append(new_dict)
        return val

def minimax_alpha_beta(state, depth, alpha, beta, piece, maximizingPlayer, tree):
    global NODE_EXPANDED
    NODE_EXPANDED += 1
    if depth == 0 or is_terminal(state):
        return score_position(state, piece)
    valid_location = get_valid_locations(state)
    if maximizingPlayer:
        val = -math.inf
        for col in valid_location:
            child = drop_piece(state, col, piece)
            new_dict = {
                child: {
                    "depth": depth - 1,
                    "value": 0,
                    "childs": [],
                }
            }
            value = minimax_alpha_beta(
                    child, depth - 1, alpha, beta, piece % 2 + 1, False, new_dict
                )
            if value > val:
                val = value
            alpha = max(alpha, value)
            if beta <= alpha:
                print_note_dict = {
                    child: {
                        "depth": depth - 1,
                        "value": "v:" + str(value) + "a:" + str(alpha) + ", b: " + str(beta) + "",
                        "childs": [],
                    }
                }
                tree[state]["childs"].append(print_note_dict)
                break
            new_dict[child]["value"] = value
            tree[state]["childs"].append(new_dict)
        return val
    else:
        val = math.inf
        for col in valid_location:
            child = drop_piece(state, col, piece)
            new_dict = {
                child: {
                    "depth": depth - 1,
                    "value": 0,
                    "childs": [],
                }
            }
            value = minimax_alpha_beta(
                    child, depth - 1, alpha, beta, piece % 2 + 1, True, new_dict
                )
            if value < val:
                val = value
            beta = min(beta, value)
            if beta <= alpha:
                print_note_dict = {
                    child: {
                        "depth": depth - 1,
                        "value": "v:" + str(value) + "a:" + str(alpha) + ", b:" + str(beta) +
                                 "",
                        "childs": [],
                    }
                }
                tree[state]["childs"].append(print_note_dict)
                break
            new_dict[child]["value"] = value
            tree[state]["childs"].append(new_dict)
        return val



def expected_minimax(state, depth, piece, maximizingPlayer, tree): 
    global NODE_EXPANDED
    NODE_EXPANDED += 1

    if depth == 0 or is_terminal(state):
        value = score_position(state, piece)
        return value
    
    col_val_max = {}
    col_val_min = {}
    valid_location = get_valid_locations(state)

    if maximizingPlayer:
        for col in valid_location:
            child = drop_piece(state, col, piece)
            new_dict = {
                child: {
                    "value": 0,
                    "childs": [],
                }
            }
            value = expected_minimax(child, depth - 1, piece % 2 + 1, False, new_dict)
            col_val_max[col] = value 
            new_dict[child]["value"] = f"{value:.2f}"
            tree[state]["childs"].append(new_dict)
            
        max_value = -math.inf
        for (col, value) in col_val_max.items():
            if col_val_max.get(col - 1, 0) == 0:
                val = (0.6 * value) + (0.4 * col_val_max.get(col + 1, 0))
                if val > max_value:
                    max_value = val
            elif col_val_max.get(col + 1, 0) == 0:
                val = (0.6 * value) + (0.4 * col_val_max.get(col - 1, 0))
                if val > max_value:
                    max_value = val
            else:
                val = (0.6 * value) + (0.2 * col_val_max.get(col - 1, 0)) + (0.2 * col_val_max.get(col + 1, 0))
                if val > max_value:
                    max_value = val  

        return max_value
    else:
        # Remaining part of the function remains the same as before

        for col in valid_location:
            child = drop_piece(state, col, piece)
            new_dict = {
                child: {
                    "value": 0,
                    "childs": [],
                }
            }
            value = expected_minimax(child, depth - 1, piece % 2 + 1, True, new_dict)
            col_val_min[col]=value

            new_dict[child]["value"] = f"{value:.2f}"
            tree[state]["childs"].append(new_dict)

        min_value=math.inf
        for (col ,value) in col_val_min.items() :
            if col_val_min.get(col-1 , 0 )   ==  0 : # ml2ash l column l ablo
                val = (0.6 * value) + (0.4 * col_val_min.get(col+1 , 0 ))
                if val < min_value :
                    min_value  = val  
            elif col_val_min.get(col + 1 , 0 )   ==  0 :
                val = (0.6 * value) + (0.4 * col_val_min.get(col-1 , 0 ))
                if val < min_value :
                    min_value  = val  
            else :
                val = (0.6 * value) + (0.2 * col_val_min.get(col-1 , 0 )  ) + (0.2 * col_val_min.get(col+1 , 0 ))
                if val < min_value :
                    min_value  = val 

        # print("min value", min_value)
        # tree[state]["value"]=min_value

        return min_value

elapsed_times = []

def agent(grid, depth, option):
    global NODE_EXPANDED
    global elapsed_times
    NODE_EXPANDED = 0
    min_tree.clear()
    state = convert_from_grid_to_string(grid)
 
    min_tree[state] = {
        "depth": depth,
        "value": 0,
        "childs": [],
    }
    valid_moves = get_valid_locations(state)
    start_time = time.time()  # Record start time

    if option == 1:  # Minimax
        scores = dict(zip(valid_moves, [get_score(state, col, 2, depth, option) for col in valid_moves]))
        max_cols = [key for key in scores.keys() if scores[key] == max(scores.values())]
        res = random.choice(max_cols)
    elif option == 2:  # Pruning Minimax
        scores = dict(zip(valid_moves, [get_score(state, col, 2, depth, option) for col in valid_moves]))
        max_cols = [key for key in scores.keys() if scores[key] == max(scores.values())]
        res = random.choice(max_cols)
    elif option == 3:  # Expected Minimax
        scores = dict(zip(valid_moves, [get_score(state, col, 2, depth, option) for col in valid_moves]))
        max_cols = [key for key in scores.keys() if scores[key] == max(scores.values())]
        res = random.choice(max_cols)
    else:
        raise ValueError("Invalid option. Please choose 1, 2, or 3.")

    # min_tree[state]["value"] = scores[res]
    min_tree[state]["value"] = f"{scores[res]:.2f}"

    
    end_time = time.time()  # Record end time
    elapsed_time = end_time - start_time

    if option == 1:
        print("Time of minimax is:", elapsed_time)
    elif option == 2:
        print("Time of pruning minimax is:", elapsed_time)
    elif option == 3:
        print("Time of expected minimax is:", elapsed_time)

    # Append the elapsed time to the list
    elapsed_times.append(elapsed_time)

    if len(elapsed_times) == 21:
        # Calculate the average time when the list size becomes 21
        average_time = sum(elapsed_times) / len(elapsed_times)
        print("Average time after 21 iterations:", average_time)
        elapsed_times = []

    return res, min_tree, NODE_EXPANDED  # res : col
