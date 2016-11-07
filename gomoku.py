 
def is_empty(board):
    for i in range (len(board)):
        for j in range(len(board)):
            if board[i][j]!=" ":
                return False
    return True
    
    
def is_bounded(board, y_end, x_end, length, d_y, d_x):
    x_bound_start = x_end-d_x*(length)
    y_bound_start = y_end-d_y*(length)
    x_bound_end = x_end + d_x
    y_bound_end = y_end + d_y
    size=len(board)
    bounded_start,bounded_end=False,False
    if (x_bound_start<0 or y_bound_start<0) or (x_bound_start>=size or y_bound_start>=size):
        bounded_start=True
    elif board[y_bound_start][x_bound_start]!=" ":
        bounded_start=True
    if (x_bound_end<0 or y_bound_end<0) or (x_bound_end>=size or y_bound_end>=size):
        bounded_end=True
    elif board[y_bound_start][x_bound_start]!=" ":
        bounded_end=True
    if bounded_start and bounded_end:
        return "CLOSED"
    elif (not bounded_start) and (not bounded_end):
        return "OPEN"
    else:
        return "SEMIOPEN"        

def detect_col(board,col,y_start, x_start, length, d_y,d_x):
    for i in range (length):
        if board[y_start+d_y*i][x_start+d_x*i]!=col: 
            return False
    if (y_start-d_y)>=0 and (x_start-d_x)>=0 and (x_start-d_x)<len(board):
        if board[y_start-d_y][x_start-d_x]==col:
            return False
    if (y_start+d_y)<len(board) and (x_start+d_x)>=0 and (x_start+d_x)<len(board):
        if board[y_start+d_y*length][x_start+d_x*length]==col:
            return False        
    return True

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count,semi_open_seq_count=0,0
    i=0 
    while y_start+d_y*(i + length-1) < len(board) and x_start+d_x*(i+length-1)<len(board) and x_start + d_x*(i+length-1)>=0: 
        if detect_col(board,col,y_start+d_y*i,x_start+d_x*i,length,d_y,d_x):
            status=is_bounded(board,y_start + (i + length-1)*d_y,x_start + (i + length-1)*d_x,length, d_y, d_x)
            if status == "OPEN":
                    open_seq_count+=1
            elif status=="SEMIOPEN":
                    semi_open_seq_count+=1 
        i+=1
            
    return open_seq_count, semi_open_seq_count
    
def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0
    for i in range (len(board)):
        count = detect_row(board, col, 0, i , length, 1, 0)
        open_seq_count += count[0]
        semi_open_seq_count +=count[1]
        count = detect_row(board, col, i, 0 , length, 0, 1)
        open_seq_count += count[0]
        semi_open_seq_count +=count[1] 
        count = detect_row(board, col, 0, i , length, 1, 1)
        open_seq_count += count[0]
        semi_open_seq_count +=count[1]
        count = detect_row(board, col, i+1, 0 , length, 1, 1)
        open_seq_count += count[0]
        semi_open_seq_count +=count[1]     
        count = detect_row(board, col, 0, i , length, 1, -1)
        open_seq_count += count[0]
        semi_open_seq_count +=count[1]
        count = detect_row(board, col, i+1, len(board)-1 , length, 1, -1)
        open_seq_count += count[0]
        semi_open_seq_count +=count[1] 
    return open_seq_count, semi_open_seq_count
    
def search_max(board):
    move_y,move_x=0,0
    max_score = -100000
    for ycoor in range (len(board)):
        for xcoor in range(len(board)):
            if board[ycoor][xcoor] == " ":
                board[ycoor][xcoor]='b'
                cur_score = score(board)
                if cur_score > max_score:
                    max_score = cur_score
                    move_y,move_x = ycoor,xcoor 
                board[ycoor][xcoor]=' '
    
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

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j]==" ":
                return False
    return True
    
def is_win(board):
    res = detect_rows(board,'w',5)
    if res[0]>=1 or res[1]>=1:
        return "White won"
    res = detect_rows(board,'b',5)
    if res[0]>=1 or res[1]>=1:
        return "Black won"
    if is_full(board):
        return "Draw"
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


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

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
    play_gomoku(8)
    
