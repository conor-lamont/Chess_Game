import Piece_constants
import Board_constants
import Player_constants
import math

no_piece = Piece_constants.no_piece
king = Piece_constants.king
queen = Piece_constants.queen
rook = Piece_constants.rook
bishop = Piece_constants.bishop
knight = Piece_constants.knight
pawn = Piece_constants.pawn

a = 0
b = 1
c = 2
d = 3
e = 4
f = 5
g = 6
h = 7

alph_low = 'abcdefgh'
alph_up = 'ABCDEFGH'

player1 = 1
player2 = -1
right = 1
left = -1
up = 1
down = -1


empty_board = [[0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0]]

start_board = [
               [rook   ,knight ,bishop ,queen  ,king   ,bishop ,knight  ,rook   ],
               [pawn   ,pawn   ,pawn   ,pawn   ,pawn   ,pawn   ,pawn    ,pawn   ],
               [0      ,0      ,0      ,0      ,0      ,0      ,0       ,0      ],
               [0      ,0      ,0      ,0      ,0      ,0      ,0       ,0      ],
               [0      ,0      ,0      ,0      ,0      ,0      ,0       ,0      ],
               [0      ,0      ,0      ,0      ,0      ,0      ,0       ,0      ],
               [-pawn  ,-pawn  ,-pawn  ,-pawn  ,-pawn  ,-pawn  ,-pawn   ,-pawn  ],
               [-rook  ,-knight,-bishop,-queen ,-king  ,-bishop,-knight ,-rook  ],
               
               ]

def print_board(board, player_turn):
    ''' print_board(board player_turn) prints each piece in board'''
    
    player = ""
    if player_turn == 1:
        player = "White"
    elif player_turn == -1:
        player = "Black"
    print("          ", end = '')
    for i in (range(0,8)):
        print(alph_up[i] + '  ', end = '')
    print('\n')
    print('\n')
   
    r = 7
    while (r >= 0):
        print('[' + str(r+1) + ']', end = '')
        print("       ", end = '')
        col = 0
        while (col <= 7):
            cur_piece = board[r][col]
            if cur_piece < 0 :
                ## Black pieces have value of -(piece val)
                print("B", end = '')
            elif cur_piece == 0:
                print("0 ", end = '')
            else :
                # White pieces have value of (piece val)
                print("W", end = '')
            
            cur_piece = abs(cur_piece)
            if cur_piece == king:
                print('K', end = '')
            elif cur_piece == queen:
                print('Q', end = '')

            elif cur_piece == bishop:
                print('b', end = '')

            elif cur_piece == knight:
                print('h', end = '')
            elif cur_piece == pawn:
                print("p", end = '')
            elif cur_piece == rook:
                print('r', end = '')

            print(' ', end = '')
            col = col + 1
        print('\n')
        r = r - 1
    print('\n')
    print('\n')
    print("It is " + str(player) + ''''s turn''')






def perform_move(board, start_col, start_row, end_col, end_row, player):
    '''perform_move(board, start_col, start_row, end_col, end_row, player) moves the piece from 
   (start_row, start_col) to (end_row, end_col) on board, then returns that board'''
    start_val = board[start_row][start_col]
    print("start_val1 is" + str(start_val))
    board[start_row][start_col] = 0
    print("start_val2 is" + str(start_val))
    board[end_row][end_col] = start_val

    return board;




def legal_move(board, start_col, start_row, end_col, end_row, player):
    ''' legal_move(board, start_col, start_row, end_col, end_row, player) determines if the move from 
    board[start_row][start_col] to board[end_row][end_col] is a legal one done by player '''
    
    if ((start_row > 8) or (start_row < 0) 
        or (start_col > 8) or (start_col < 0)
        or (end_row > 8) or (end_row < 0)
        or (end_col > 8) or (end_col < 0)) :
        print("bad row")
        return False;
            
    piece = board[start_row][start_col]
    print("piece is" + str(piece))
    end_piece = board[end_row][end_col]
    i = 1
    good_start_posn = False
    self_interfere_end = False
    while (i < 7) :
        if (piece == player * i):
            good_start_posn = True
        if (end_piece == (player * i)):
            self_interfere_end = True
        i = i + 1
    if (not(good_start_posn) or (self_interfere_end)):
        print("no goood start")
        return False

    if abs(piece) == pawn :
        return legal_move_pawn(board, start_col, start_row, end_col, end_row, player)
    if abs(piece) == rook :
        return legal_move_rook(board, start_col, start_row, end_col, end_row, player)
    if abs(piece) == bishop :
        return legal_move_bishop(board, start_col, start_row, end_col, end_row, player)
    if abs(piece) == knight :
        return legal_move_knight(board, start_col, start_row, end_col, end_row, player)
    if abs(piece) == queen :
        return legal_move_queen(board, start_col, start_row, end_col, end_row, player)

    

    # continue to check if each piece move is legal, then check with function (king_is_safe) with a theoretical board,
    #  board2, with current proposed move implemented.

    return True
 


def legal_move_pawn(board, start_col, start_row, end_col, end_row, player):
    ''' legal_move_pawn(board, start_col, start_row, end_col, end_row, player) determines 
    if move from (start_row, start_col) -> (end_row, end_col) where the starting piece is a pawn is legal
    
    requires: end position must be valid(i.e. not a friendly piece, different than start position)
              start position must have a pawn from player
    '''
               
    rows_moved_up = player * (end_row - start_row)
    cols_moved = end_col - start_col
    end_piece_init = board[end_row][end_col]
    opposite_piece = end_piece_init * board[start_row][start_col] < 0
    print('rows moved up is' + str(rows_moved_up))

   # max_row represents the max num of rows the pawn can move up 
    max_row = 1

    if (start_row == 1 and board[start_row][start_col] == pawn) or (start_row == 6 and board[start_row][start_col] == -1 * pawn) :
        max_row = 2

    if (rows_moved_up > max_row):
        # too many move-ups
        print("too may rows ")
        return False

    if (abs(cols_moved) > 0):
        #can ever only move one column at most (diagonal once)
        if abs(cols_moved) > 1 or not(rows_moved_up == 1):
            print("too many cols")
            return False
        else:
            # must be opposite sided pieces diagonal to pawn to move diagonal
            print("no diag pawn kill")
            return ((rows_moved_up == 1) and (player * end_piece_init < 0))
    elif (opposite_piece == True):
        return False

    if (rows_moved_up == 2):
        # if moving 2 rows up, the intermittent spot must have no piece
        
       return (board[start_row + 1*player][start_col] ==  no_piece)
    return True


def legal_move_rook(board, start_col, start_row, end_col, end_row, player):
    ''' legal_move_rook(board, start_col, start_row, end_col, end_row, player)  determines 
    if move from (start_row, start_col) -> (end_row, end_col) where the starting piece is a rook is legal
    
    requires: end position must be valid(i.e. not a friendly piece, different than start position)
              start position must have a rook from player
    '''
    rows_moved = (end_row - start_row)
    cols_moved = end_col - start_col
    interfere = False

    

    if (abs(rows_moved) > 0 and abs(cols_moved) > 0):
        return False
    elif abs(rows_moved) > 0:
        if rows_moved > 0:
          start_idx = start_row
          end_idx = end_row
        else:
          end_idx= start_row
          start_idx = end_row
        for i in range(start_idx  + 1, end_idx):
            if board[i][start_col] != 0: 
                interfere = True
    else:
        if cols_moved > 0:
          start_idx = start_col
          end_idx = end_col
        else:
          end_idx= start_col
          start_idx = end_col
        for i in range(start_idx + 1, end_idx):
            if board[start_row][i] != 0:
                interfere = True
    if interfere == True:
        return False
    else: 
        return True

def legal_move_bishop(board, start_col, start_row, end_col, end_row, player):
    ''' legal_move_rook(board, start_col, start_row, end_col, end_row, player)  determines 
    if move from (start_row, start_col) -> (end_row, end_col) where the starting piece is a bishop is legal
    
    requires: end position must be valid(i.e. not a friendly piece, different than start position)
              start position must have a bishop from player
    '''
    cols_moved= end_col - start_col
    rows_moved = end_row - start_row

    if not(abs(cols_moved) == abs(rows_moved)):
        return False
    else:
        if rows_moved > 0:
            horiz_dir = right
        else: 
            horiz_dir = left
        
        if cols_moved > 0:
            vert_dir = up
        else:
            vert_dir = down

            
        counter = 1
        while (counter < abs(rows_moved)):
            if board[start_row + (counter * horiz_dir)][start_col + (counter * vert_dir)] != 0 :
                return False

            counter = counter + 1
        return True



def legal_move_knight(board, start_col, start_row, end_col, end_row, player):
    ''' legal_move_rook(board, start_col, start_row, end_col, end_row, player)  determines 
    if move from (start_row, start_col) -> (end_row, end_col) where the starting piece is a knight is legal
    
    requires: end position must be valid(i.e. not a friendly piece, different than start position)
              start position must have a knight from player
    '''

    cols_moved = end_col - start_col
    rows_moved = end_row - start_row

    good_move = False
    if (abs(rows_moved) == 2 and abs(cols_moved == 1)) or (abs(rows_moved) == 1 and abs(cols_moved == 2)):
        good_move = True

    return good_move

def legal_move_queen(board, start_col, start_row, end_col, end_row, player):
    ''' legal_move_rook(board, start_col, start_row, end_col, end_row, player)  determines 
    if move from (start_row, start_col) -> (end_row, end_col) where the starting piece is a queen is legal
    
    requires: end position must be valid(i.e. not a friendly piece, different than start position)
              start position must have a queen from player
    '''
    cols_moved = end_col - start_col
    rows_moved = end_row - start_row
    good_move = False
    move_type = 0

    if (abs(cols_moved) == abs(rows_moved)):
        move_type = bishop
    elif (rows_moved == 0 or cols_moved == 0):
        move_type = rook
    

print('''
Welcome to Python Chess!
First, some rules for the board being displayed.
The board has the co-ordinates printed as the top row and first column.
On the board, a W prefix marks a White piece, and a B prefix denotes a Black piece.
A knight is denoted by H (for horse), to differentiate from king, K.
A Queen is denoted by Q. Rook : r. Bishop : b. pawn : p.
A 0 represents an unoccupied space.
You will input a move as Co-ordinates, from start to end(no brackets or commas). For instance, 
to go from A1 to B4, one would input:
A1 B4



The only exception to this is when you would like to Castle. In this case, the input is CC 
followed by the co-ordinate of the rookto castle with. For instance, for black to Castle with 
the rook at H8, the input would be:
CC H8

Let's get started! Here is the initial board:
''')
print_board(start_board, 1)   

illegal_move = True
board = start_board;
player = player1

while (1 == 1):
    player_name = ''
    if player == player1:
        player_name = 'White'
    else: 
        player_name = 'Black'

    while (illegal_move == True):
        if player == player1:
            player_name = 'White'
        else: 
            player_name = 'Black'
        move_string = input(player_name + ", what is your move?: ")
        poss_start_row = move_string[1]
        poss_start_col = move_string[0]
        poss_end_row = move_string[4]
        poss_end_col = move_string[3]

        start_row = int(poss_start_row) - 1
        start_col = Board_constants.board_let_to_int(poss_start_col)
        end_row = int(poss_end_row) - 1
        end_col = Board_constants.board_let_to_int(poss_end_col)

        print("start position is " + str(start_row) + str(start_col))
        print("end position is " + str(end_row) + str(end_col))
        print("legality is" + str(legal_move(board, start_col, start_row, end_col, end_row, player)))
        if (legal_move(board, start_col, start_row, end_col, end_row, player) == True):
            illegal_Move = False
            new_board = perform_move(board, start_col, start_row, end_col, end_row, player)
            player = -1 * player
            print_board(new_board, player)  
        else:
            print("illegal move, try again")
        
    
    

        
    



