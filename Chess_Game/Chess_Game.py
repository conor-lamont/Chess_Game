import Piece_constants
import Board_constants
import Player_constants
import math
import copy


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

DNE = -50


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

def find_king(board, player):
    '''find_king(board, player) returns a list containing the row and column of the co-ordinates of player's king [row, col]'''
    row = 0
    while (row <= 7):
        col = 0
        while (col <= 7):
            if board[row][col] == (player * king):
                return [row, col]
            col = col + 1
        row = row + 1
    return [DNE, DNE]
    

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

    
    board2 = copy.deepcopy(board)
    start_val = board2[start_row][start_col]
    print("start_val1 is" + str(start_val))
    board2[start_row][start_col] = 0
    
    if (player == 1) and start_val == pawn and end_row == 7:
        start_val = queen

    if player == -1 and start_val == -1 * pawn and end_row == 0:
        start_val = -1 * queen

    board2[end_row][end_col] = start_val
    if (player == 1) and start_val == pawn and end_row == 7:
        start_val = queen

    print('equal boards' + str(board == board2))
    return board2




def legal_move(board, start_col, start_row, end_col, end_row, player):
    ''' legal_move(board, start_col, start_row, end_col, end_row, player) determines if the move from 
    board[start_row][start_col] to board[end_row][end_col] is a legal one done by player '''
    
    if ((start_row >= 8) or (start_row < 0) 
        or (start_col >= 8) or (start_col < 0)
        or (end_row >= 8) or (end_row < 0)
        or (end_col >= 8) or (end_col < 0)) :
        
        return False
            
    piece = board[start_row][start_col]
    print("piece is" + str(piece))
    print("player is" + str(player))
    end_piece = board[end_row][end_col]
    i = 1
    good_start_posn = False
    self_interfere_end = False
    while (i < 7) :
        if (piece == player * i):
            good_start_posn = True
        if (end_piece == (player * i)):
            print("self interf end")
            self_interfere_end = True
        i = i + 1
    if (not(good_start_posn) or (self_interfere_end)):
        print("start posn/good is:" + str(good_start_posn))
        return False
    legality = False
    if abs(piece) == pawn :
        legality = legal_move_pawn(board, start_col, start_row, end_col, end_row, player)
    if abs(piece) == rook :
        legality = legal_move_rook(board, start_col, start_row, end_col, end_row, player)
    if abs(piece) == bishop :
        legality = legal_move_bishop(board, start_col, start_row, end_col, end_row, player)
    if abs(piece) == knight :
        print("knight start")
        legality = legal_move_knight(board, start_col, start_row, end_col, end_row, player)
        print("legal knight is" + str(legality))
    if abs(piece) == queen :
        legality = legal_move_queen(board, start_col, start_row, end_col, end_row, player)
    if abs(piece) == king :
        legality = legal_move_king(board, start_col, start_row, end_col, end_row, player)

    if legality == False:
        return False

    
    board2 = perform_move(board,start_col,start_row,end_col,end_row,player)
    print('bb equal' + str(board == board2))
    friendly_king_posn = find_king(board2, player)
    friendly_king_safety = king_is_safe(board2,player, friendly_king_posn[0],friendly_king_posn[1])
    if (friendly_king_safety == False):
        return False
    print("done this")
   


    

    # continue to check if each piece move is legal, then check with function (king_is_safe) with a pietheoretical board,
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
    
    if rows_moved_up < 1:
       return False
   # max_row represents the max num of rows the pawn can move up 
    max_row = 1

    if (start_row == 1 and board[start_row][start_col] == pawn) or (start_row == 6 and board[start_row][start_col] == -1 * pawn) :
        max_row = 2

    if (rows_moved_up > max_row):
        # too many move-ups
        
        return False

    if (abs(cols_moved) > 0):
        #can ever only move one column at most (diagonal once)
        if abs(cols_moved) > 1 or not(rows_moved_up == 1):
            
            return False
        else:
            # must be opposite sided pieces diagonal to pawn to move diagonal
            
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
    if (abs(rows_moved) == 2 and abs(cols_moved) == 1) or (abs(rows_moved) == 1 and abs(cols_moved) == 2):
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

    if move_type == 0:
        return False
    if move_type == bishop:
        return legal_move_bishop(board, start_col, start_row, end_col, end_row, player)
    else:
        return legal_move_rook(board, start_col, start_row, end_col, end_row, player)

def legal_move_king(board, start_col, start_row, end_col, end_row, player):
    ''' legal_move_pawn(board, start_col, start_row, end_col, end_row, player) determines 
    if move from (start_row, start_col) -> (end_row, end_col) where the starting piece is a king is legal
    
    requires: end position must be valid(i.e. not a friendly piece, different than start position)
              start position must have a king from player
    '''
    rows_moved = end_row - start_row
    cols_moved = end_col - start_col

    good_move = False
    if (abs(rows_moved) <= 1 and abs(cols_moved) <= 1):
        good_move = True

    return good_move

def king_is_safe(theor_board, player, king_row, king_col):
    ''' king_is_safe(theor_board, player, king_row, king_col) determines if the player's king
    located at (king_row, king_col) is valid.
    requires: player's king is at (king-row, king_col)
    '''
    safe = True
    row = 0
    while row <= 7:
        col = 0
        while col <= 7:
            cur_piece = theor_board[row][col]
            if abs(cur_piece) > 0:
                if cur_piece / abs(cur_piece) == -1 * player:
                    if legal_move(theor_board,col,row,king_col,king_row, -1 * player):
                        safe = False
            col = col + 1
        row = row + 1
    return safe


def poss_rook_moves(board, rook_row, rook_col, player):
    ''' poss_rook_moves(board, rook_row, rook_col, player) returns whether
    player's rook at (rook_row, rook_col) has any legal moves
    '''
    
    right = rook_col + 1
    while(right <= 7):

        if legal_move(board, rook_col, rook_row, right, rook_row, player):
                return True
        
        if abs(board[rook_row][right]) > 0:
            break
        
        right = right + 1

    left = rook_col - 1
    while(left >= 0):
        if legal_move(board, rook_col, rook_row, left, rook_row,  player):
            return True
        if abs(board[rook_row][left]) > 0:
            break
        left = left - 1

    up = rook_row + 1
    while (up <= 7):
        if legal_move(board, rook_col, rook_row, rook_col, up,  player):
            return True
        if abs(board[up][rook_col]) > 0:
            break
        up = up + 1


    down = rook_row - 1
    while (down >= 0):
        if legal_move(board, rook_col, rook_row, rook_col, down,  player):
            return True
        if abs(board[down][rook_col]) > 0:
            break
        down = down - 1

    return False


def poss_pawn_moves(board, pawn_row, pawn_col, player):
    ''' poss_pawn_moves(board, pawn_row, pawn_col, player) returns whether
    player's rook at (pawn_row, pawn_col) has any legal moves
    '''

    if ((legal_move(board, pawn_col, pawn_row, pawn_col, pawn_row + 1, player)) or
    legal_move(board, pawn_col, pawn_row, pawn_col + 1, pawn_row + 1, player) or
    (legal_move(board, pawn_col, pawn_row, pawn_col - 1, pawn_row + 1, player)) or 
    legal_move(board, pawn_col, pawn_row, pawn_col, pawn_row + 2, player)):
        return True
    return False


def poss_bishop_moves(board, bishop_row, bishop_col, player):
    ''' poss_bishop_moves(board, bishop_row, bishop_col, player) returns whether
    player's bishop at (bishop_row, bishop_col) has any legal moves
    '''
    
    up = bishop_row + 1
    right = bishop_col + 1
    while(right <= 7 and up <= 7):

        if legal_move(board, bishop_col, bishop_row, right, up,  player):
            return True
        
        if abs(board[up][right]) > 0:
            break
        
        right = right + 1
        up = up + 1

    left = bishop_col - 1
    up = bishop_row + 1
    while(left >= 0 and up <= 7):
        if legal_move(board, bishop_col, bishop_row, left, up, player):
            return True
        if abs(board[up][left]) > 0:
            break
        left = left - 1
        up = up + 1


    down = bishop_row - 1
    left = bishop_col - 1
    while (down >= 0 and left >= 0):
        if legal_move(board, bishop_col, bishop_row, left, down, player):
            return True
        if abs(board[down][left]) > 0:
            break
        down = down - 1
        left = left - 1


    right = bishop_col + 1
    down = bishop_row - 1
    while (down >= 0 and right <= 7):
        if legal_move(board, bishop_col, bishop_row, down, right, player):
            return True
        if abs(board[down][right]) > 0:
            break
        right = right + 1
        down = down - 1

    return False



def poss_knight_moves(board, knight_row, knight_col, player):
    ''' poss_knight_moves(board, knight_row, knight_col, player) returns whether
    player's knight at (knight_row, knight_col) has any legal moves
    '''

    return (legal_move(board, knight_col, knight_row, knight_col - 1, knight_row + 2, player) or
           legal_move(board, knight_col, knight_row, knight_col + 1, knight_row + 2, player) or 
           legal_move(board, knight_col, knight_row, knight_col + 2, knight_row + 1, player) or
           legal_move(board, knight_col, knight_row, knight_col + 2, knight_row - 1, player) or
           legal_move(board, knight_col, knight_row, knight_col + 1, knight_row - 2, player) or 
           legal_move(board, knight_col, knight_row, knight_col - 1, knight_row - 2, player) or
           legal_move(board, knight_col, knight_row, knight_col - 2, knight_row - 1, player) or
           legal_move(board, knight_col, knight_row, knight_col - 2, knight_row + 1, player))

def poss_queen_moves(board, queen_row, queen_col, player):
    ''' poss_queen_moves(board, queen_row, queen_col, player) returns whether
    player's queen at (queen_row, queen_col) has any legal moves
    '''
    return (poss_bishop_moves(board, queen_row, queen_col, player) or poss_rook_moves(board, queen_row, queen_col, player))


def poss_king_moves(board, king_row, king_col, player):
    ''' poss_queen_moves(board, king_row, king_col, player) returns whether
    player's queen at (king_row, king_col) has any legal moves
    '''
    return (legal_move(board, king_col, king_row, king_col - 1, king_row - 1, player) or
            legal_move(board, king_col, king_row, king_col - 1, king_row , player) or 
            legal_move(board, king_col, king_row, king_col - 1, king_row + 1, player) or 
            legal_move(board, king_col, king_row, king_col, king_row + 1, player) or
            legal_move(board, king_col, king_row, king_col + 1, king_row + 1, player) or
            legal_move(board, king_col, king_row, king_col + 1, king_row, player) or
            legal_move(board, king_col, king_row, king_col + 1, king_row - 1, player) or
            legal_move(board, king_col, king_row, king_col, king_row - 1, player))


def checkmate(board, player_under_attack):
    row = 0
    king_under_attack_cords = find_king(board, player_under_attack)
    king_row = king_under_attack_cords[0]
    king_col = king_under_attack_cords[1]
    print("cm check, king row is" + str(king_row) + "col is" + str(king_col))
    


    while (row <= 7):
        col = 0
        while col <= 7 :
            if board[row][col] == player_under_attack * king:
                if (True == poss_king_moves(board, row, col, player_under_attack)):
                    return False
            elif board[row][col] == player_under_attack * queen:
                if (True == poss_queen_moves(board, row, col, player_under_attack)):
                    return False
            elif board[row][col] == player_under_attack * knight:
                if (True == poss_knight_moves(board, row, col, player_under_attack)):
                    return False
            elif board[row][col] == player_under_attack * bishop:
                if (True == poss_bishop_moves(board, row, col, player_under_attack)):
                    return False
            elif board[row][col] == player_under_attack * pawn:
                if (True == poss_pawn_moves(board, row, col, player_under_attack)):
                    return False
            elif board[row][col] == player_under_attack * rook:
                if (True == poss_rook_moves(board, row, col, player_under_attack)):
                    return False
            col = col + 1
        row = row + 1


    return True
                 
                
                


        

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
board = copy.deepcopy(start_board);
player = player1
end = False

while (end == False):
        if player == player1:
            player_name = 'White'
        else: 
            player_name = 'Black'
        invalid_string = True
        while(invalid_string == True):
            move_string = input(player_name + ", what is your move?: ")
            if (len(move_string) == 5 and (move_string[0] in alph_up) and (move_string[1] in "12345678")
            and (move_string[2] == ' ') and (move_string [3] in alph_up) and move_string[4] in "12345678"):
                invalid_string = False


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
        #board_init = board.copy()
        #board_init2 = board.copy()
        #print("legality is" + str(legal_move(board, start_col, start_row, end_col, end_row, player)))
        if (legal_move(board, start_col, start_row, end_col, end_row, player) == True):
            illegal_Move = False
            board = perform_move(board, start_col, start_row, end_col, end_row, player)
            
            enemy_king_posn = find_king(board, (-1 * player))
            print("enemy player is" + str(-1 * player))
            print('enemy king posn is' + str(enemy_king_posn))
            enemy_king_safety = king_is_safe(board, (-1 * player), enemy_king_posn[0], enemy_king_posn[1])

            if (enemy_king_safety == False):
                  # temporary code:
                  chkm = checkmate(board, -1 * player)
                  if (chkm == True):
                        print("Checkmate! " + player_name + " won!")
                        inval = True
                        while (inval == True):
                            play_again = input("Would you like to play again?: (Type YES or NO): ")
                            if play_again == ("YES"):
                                inval = False
                                board = copy.deepcopy(start_board)
                                print_board(board, player)
                                player = player1
                            if play_again == "NO":
                                end = True
                  else:
                        player = -1 * player
                        print_board(board, player)
                        
            else:
                player = -1 * player
                print_board(board, player)
        else:
            print("illegal move, try again")
        
    
