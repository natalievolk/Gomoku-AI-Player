# -*- coding: utf-8 -*-

"""Gomoku game
Implements a basic AI opponent for Gomoku 

Author(s): Natalie Volk, using starter code from Michael Guerzhoy and Siavash Kazemian.  Last modified: Nov. 18, 2020
"""

def is_empty(board):
    for i in range(len(board)):
        for k in range(len(board)):
            if board[i][k] != " ":
                return False
    return True
    
    
def is_bounded(board, y_end, x_end, length, d_y, d_x):
    # making x, y variables to indicate start of sequence
    y_start = y_end - (length - 1) * d_y
    x_start = x_end - (length - 1) * d_x
    
    boundedness = [False, False]
    
    if 8 > x_start - d_x >= 0 and 8 > y_start - d_y >= 0:
        if board[y_start - d_y][x_start - d_x] == " ":
            boundedness[0] = True
    
    if 8 > x_end + d_x >= 0 and 8 > y_end + d_y >= 0:
        if board[y_end + d_y][x_end + d_x] == " ":
            boundedness[1] = True
        
    if boundedness[0] == boundedness[1] == True:
        return "OPEN"
    elif boundedness[0] == boundedness[1] == False:
        return "CLOSED"
    else:
        return "SEMIOPEN"
        
    
def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    
    count_semiopen, count_open = 0, 0
    
    i = 0
    while i < len(board):
        
        y_curr = y_start + i * d_y
        x_curr = x_start + i * d_x
        
        count = 1
        
        if not ((0 <= y_curr < 8) and (0 <= x_curr < 8)):
            break
        
        while (board[y_curr][x_curr] == col) and (0 <= y_curr + d_y < 8) and (0 <= x_curr + d_x < 8):
            if board[y_curr + d_y][x_curr + d_x] != col:
                break
            y_curr += d_y
            x_curr += d_x
            count += 1
        
        i += count
        
        if count != length:
            continue
        
        if is_bounded(board, y_curr, x_curr, length, d_y, d_x) == "SEMIOPEN":
                count_semiopen += 1
        elif is_bounded(board, y_curr, x_curr, length, d_y, d_x) == "OPEN":
            count_open += 1
    
    return count_open, count_semiopen
    
def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0
    
    for i in range(len(board)):
        # check left to right
        ltr = detect_row(board, col, i, 0, length, 0, 1)
        open_seq_count += ltr[0]
        semi_open_seq_count += ltr[1]
        #print("ltr " + str(ltr[0]) + " open and " + str(ltr[1]) + " semi")
        
        # check top to bottom
        ttb = detect_row(board, col, 0, i, length, 1, 0)
        open_seq_count += ttb[0]
        semi_open_seq_count += ttb[1]
        #print("ttb " + str(ttb[0]) + " open and " + str(ttb[1]) + " semi")
        
        #check upper left to lower right
        diag_ltr1 = detect_row(board, col, 0, i, length, 1, 1)
        open_seq_count += diag_ltr1[0]
        semi_open_seq_count += diag_ltr1[1]
        
        #print("diag_ltr1 " + str(diag_ltr1[0]) + " open and " + str(diag_ltr1[1]) + " semi")
        
        # so that there isn't a repeat in the (0.0) diagonal
        if i > 0:
            diag_ltr2 = detect_row(board, col, i, 0, length, 1, 1)
            open_seq_count += diag_ltr2[0]
            semi_open_seq_count += diag_ltr2[1]
            #print("diag_ltr2 " + str(diag_ltr2[0]) + " open and " + str(diag_ltr2[1]) + " semi")
        
        # check upper right to lower left
        diag_rtl1 = detect_row(board, col, i, len(board)-1, length, 1, -1)
        open_seq_count += diag_rtl1[0]
        semi_open_seq_count += diag_rtl1[1]
        #print("diag_rtl1 " + str(diag_rtl1[0]) + " open and " + str(diag_rtl1[1]) + " semi")
        
        if i != 7:
            diag_rtl2 = detect_row(board, col, 0, i, length, 1, -1)
            open_seq_count += diag_rtl2[0]
            semi_open_seq_count += diag_rtl2[1]
            #print("diag_rtl2 " + str(diag_rtl2[0]) + " open and " + str(diag_rtl2[1]) + " semi")
       
    
    return open_seq_count, semi_open_seq_count

def five_in_a_row(board, col, y_start, x_start, d_y, d_x):
        
    i = 0
    while i < len(board):
        
        y_curr = y_start + i * d_y
        x_curr = x_start + i * d_x
        
        count = 1
        
        if not ((0 <= y_curr < 8) and (0 <= x_curr < 8)):
            break
        
        while (board[y_curr][x_curr] == col) and (0 <= y_curr + d_y < 8) and (0 <= x_curr + d_x < 8):
            if board[y_curr + d_y][x_curr + d_x] != col:
                break
            y_curr += d_y
            x_curr += d_x
            count += 1
        
        i += count
        
        if count != 5:
            continue
        
        return True
    return False

def five_in_any_row(board, col):
    
    for i in range(len(board)):
        # check left to right
        if five_in_a_row(board, col, i, 0, 0, 1):
            return True
        
        # check top to bottom
        if five_in_a_row(board, col, 0, i, 1, 0):
            return True
        
        #check upper left to lower right
        if five_in_a_row(board, col, 0, i, 1, 1) or five_in_a_row(board, col, i, 0, 1, 1):
            return True
        
        # check upper right to lower left
        if five_in_a_row(board, col, i, len(board)-1, 1, -1) or five_in_a_row(board, col, 0, i, 1, -1):
            return True
    
    return False
    
    
def search_max(board):
    max_score = 0
    move_y, move_x = 0,0
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == " ":
                board[y][x] = "b"
                if max_score < score(board):
                    max_score = score(board)
                    move_y, move_x = y, x
                board[y][x] = " "
                
    # makes sure the placeholder is empty (and replacing it if not) 
    if max_score == 0 and board[move_y][move_x] != " ":
        for y in range(len(board)):
            for x in range(len(board[0])):
                if board[y][x] == " ":
                    move_y, move_x = y, x
                    break
            break
            
    return move_y, move_x
    
def score(board):
    MAX_SCORE = 100000
    
    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}
    
    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)
        
    
    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE
    
    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE
        
    return (-10000 * (open_w[4] + semi_open_w[4])+ 
            500  * open_b[4]                     + 
            50   * semi_open_b[4]                + 
            -100  * open_w[3]                    + 
            -30   * semi_open_w[3]               + 
            50   * open_b[3]                     + 
            10   * semi_open_b[3]                +  
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])

    
def is_win(board):
    draw = True
    
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == " ":
                draw = False
    if draw:
        return "Draw"
    
    white_open, white_semi_open = detect_rows(board, 'w', 5)
    if white_open > 0 or white_semi_open > 0 or five_in_any_row(board, 'w'):
        return "White won"
    
    black_open, black_semi_open = detect_rows(board, 'b', 5)
    if black_open > 0 or black_semi_open > 0 or five_in_any_row(board, 'b'):
        return "Black won"
    
    return "Continue playing"


def print_board(board):
    
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"
    
    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1]) 
    
        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"
    
    print(s)
    

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board
                


def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))
        
    
    

        
    
def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    
    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)
            
        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
            
            
        
        
        
        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
        
            
            
def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col        
        y += d_y
        x += d_x


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    
    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")
        
def is_bounded_test_corner():
    board = make_empty_board(8)
    board[0][0] = "w"
    board[0][7] = "w"
    board[7][0] = "w"
    board[7][7] = "w"
    print_board(board)

    a,mini_test_count=0,0
    #checking (0,0)
    y,x=0,0
    if is_bounded(board,y,x,1,0,1)=="SEMIOPEN" and is_bounded(board,y,x,1,1,0)=="SEMIOPEN" and is_bounded(board,y,x,1,1,-1)=="CLOSED" and is_bounded(board,y,x,1,1,1)=="SEMIOPEN":
        mini_test_count+=4

    #checking (7,0)
    x,y=7,0
    if is_bounded(board,y,x,1,0,1)=="SEMIOPEN" and is_bounded(board,y,x,1,1,0)=="SEMIOPEN" and is_bounded(board,y,x,1,1,-1)=="SEMIOPEN" and is_bounded(board,y,x,1,1,1)=="CLOSED":
        mini_test_count+=4

    #checking (0,7)
    x,y=0,7
    if is_bounded(board,y,x,1,0,1)=="SEMIOPEN" and is_bounded(board,y,x,1,1,0)=="SEMIOPEN" and is_bounded(board,y,x,1,1,-1)=="SEMIOPEN" and is_bounded(board,y,x,1,1,1)=="CLOSED":
        mini_test_count+=4

    #checking (7,7)
    x,y=7,7
    if is_bounded(board,y,x,1,0,1)=="SEMIOPEN" and is_bounded(board,y,x,1,1,0)=="SEMIOPEN" and is_bounded(board,y,x,1,1,-1)=="CLOSED" and is_bounded(board,y,x,1,1,1)=="SEMIOPEN":
        mini_test_count+=4

    if mini_test_count == 16:
        print("TEST CASE for is_bounded PASSED!!!!")
    else:
        print("TEST CASE for is_bounded FAILED, passing", mini_test_count,"/16",":(")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

"""
        
#I ADDED THIS IN
def test_detect_row2():
    board = make_empty_board(8)
    x = 2; y = 2; d_x = 1; d_y = 1; length = 3;
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,0,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row 2 PASSED")
    else:
        print("TEST CASE for detect_row 2 FAILED")
        
#I ADDED THIS IN
def test_detect_row3():
    board = make_empty_board(8)
    x = 0; y = 0; d_x = 1; d_y = 1; length = 4;
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,0,length,d_y,d_x) == (0,1):
        print("TEST CASE for detect_row 3 PASSED")
    else:
        print("TEST CASE for detect_row 3 FAILED")
        
#I ADDED THIS IN
def test_detect_row4():
    board = make_empty_board(8)
    x = 5; y = 2; d_x = 0; d_y = 1; length = 5;
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,5,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row 4 PASSED")
    else:
        print("TEST CASE for detect_row 4 FAILED")
        
#I ADDED THIS IN
def test_detect_row5():
    board = make_empty_board(8)
    x = 3; y = 2; d_x = 1; d_y = 1; length = 5;
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,1,length-2,d_y,d_x) == (0,0):
        print("TEST CASE for detect_row 5 PASSED")
    else:
        print("TEST CASE for detect_row 5 FAILED")
        
"""


def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")
        

"""
#I ADDED THIS IN
def test_detect_rows2():
    board = make_empty_board(8)
    x = 2; y = 2; d_x = 1; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows 2 PASSED")
    else:
        print("TEST CASE for detect_rows 2 FAILED")
        
#I ADDED THIS IN
def test_detect_rows3():
    board = make_empty_board(8)
    x = 4; y = 7; d_x = 1; d_y = 0; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    x = 0; y = 2; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows 3 PASSED")
    else:
        print("TEST CASE for detect_rows 3 FAILED")
"""

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

#I ADDED THIS        
def test_search_max2():
    board = make_empty_board(8)
    x = 0; y = 0; d_x = 0; d_y = 1; length = 1; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    #x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    #put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    print(search_max(board))
    if search_max(board) == (0, 1):
        print("TEST CASE for search_max 2 PASSED")
    else:
        print("TEST CASE for search_max 2 FAILED")
        
# ADDED THIS IN
def testing_win_5_closed():
    board = make_empty_board(8)
    board[2][2] = "w"
    y = 3;
    x = 2;
    d_x = 0;
    d_y = 1;
    length = 5
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    if is_win(board)=="Black won":
        print("PASSSSSSSSS")
    else:
        print("EPIC FAIL :(")
        # Expected output:
        # *0|1|2|3|4|5|6|7*
        # 0 | | | | | | | *
        # 1 | | | | | | | *
        # 2 | |w| | | | | *
        # 3 | |b| | | | | *
        # 4 | |b| | | | | *
        # 5 | |b| | | | | *
        # 6 | |b| | | | | *
        # 7 | |b| | | | | *
        # *****************
        # PASSSSSSSSS
        

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    
    y = 3; x = 5; d_x = -1; d_y = 1; length = 2
    
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #     
    
    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);
    
    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #        
    #        
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0


  
            
if __name__ == '__main__':
    print(play_gomoku(8))
    #board = make_empty_board(8)
    #print_board(board)
    #test_is_empty()
    #test_is_bounded()
    #test_detect_row()
    #test_detect_row2()
    #test_detect_row5()
    #test_detect_rows()
    #test_detect_rows2()
    #test_detect_rows3()
    #is_bounded_test_corner()
    #test_search_max2()
    #some_tests()
    #testing_win_5_closed()
    """
    board = [
    [' ', ' ', ' ', ' ', 'b', ' ', ' ', ' '],
    [' ', ' ', ' ', 'b', ' ', ' ', ' ', ' '],
    [' ', ' ', 'b', ' ', ' ', ' ', ' ', ' '],
    [' ', 'b', ' ', ' ', ' ', ' ', ' ', ' '],
    ['b', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
    """
    
    #print(is_win(board))
