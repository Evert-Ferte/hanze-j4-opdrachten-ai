"""

Othello is a turn-based two-player strategy board game.

-----------------------------------------------------------------------------
Board representation

We represent the board as a flat-list of 100 elements, which includes each square on
the board as well as the outside edge. Each consecutive sublist of ten
elements represents a single row, and each list element stores a piece. 
An initial board contains four pieces in the center:

    ? ? ? ? ? ? ? ? ? ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . o @ . . . ?
    ? . . . @ o . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? ? ? ? ? ? ? ? ? ?

The outside edge is marked ?, empty squares are ., black is @, and white is o.

This representation has two useful properties:

1. Square (m,n) can be accessed as `board[mn]`, and m,n means m*10 + n. This avoids conversion
   between square locations and list indexes.
2. Operations involving bounds checking are slightly simpler.
"""

# The black and white pieces represent the two players.
import random

EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
PIECES = (EMPTY, BLACK, WHITE, OUTER)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}

# To refer to neighbor squares we can add a direction to a square.
UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
# in total 8 directions.
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)

def squares():
    # list all the valid squares on the board.
    # returns a list of valid integers [11, 12, ...]; e.g. 19,20,21 are invalid
    # 11 means first row, first col, because the board size is 10x10
    return [i for i in range(11, 89) if 1 <= (i % 10) <= 8]

def initial_board():
    # create a new board with the initial black and white positions filled
    # returns a list ['?', '?', '?', ..., '?', '?', '?', '.', '.', '.', ...]
    board = [OUTER] * 100
    for i in squares():
        board[i] = EMPTY
    # the middle four squares should hold the initial piece positions.
    board[44], board[45] = WHITE, BLACK
    board[54], board[55] = BLACK, WHITE
    return board

def print_board(board):
    # get a string representation of the board
    # heading '  1 2 3 4 5 6 7 8\n'
    rep = ''
    rep += '  %s\n' % ' '.join(map(str, range(1, 9)))
    # begin,end = 11,19 21,29 31,39 ..
    for row in range(1, 9):
        begin, end = 10*row + 1, 10*row + 9
        rep += '%d %s\n' % (row, ' '.join(board[begin:end]))
    return rep

# -----------------------------------------------------------------------------
# Playing the game

# We need functions to get moves from players, check to make sure that the moves
# are legal, apply the moves to the board, and detect when the game is over.

# Checking moves. A move must be both valid and legal: it must refer to a real square,
# and it must form a bracket with another piece of the same color with pieces of the
# opposite color in between.

def is_valid(move):
    # is move a square on the board?
    # move must be an int, and must refer to a real square
    return isinstance(move, int) and move in squares()

def opponent(player):
    # get player's opponent piece
    return BLACK if player is WHITE else WHITE

def find_bracket(square, player, board, direction):
    # find and return the square that forms a bracket with square for player in the given
    # direction; returns None if no such square exists
    bracket = square + direction
    if board[bracket] == player:
        return None
    opp = opponent(player)
    while board[bracket] == opp:
        bracket += direction
    # if last square board[bracket] not in (EMPTY, OUTER, opp) then it is player
    return None if board[bracket] in (OUTER, EMPTY) else bracket

def is_legal(move, player, board):
    # is this a legal move for the player?
    # move must be an empty square and there has to be a bracket in some direction
    # note: any(iterable) will return True if any element of the iterable is true
    hasbracket = lambda direction: find_bracket(move, player, board, direction)
    return board[move] == EMPTY and any(hasbracket(x) for x in DIRECTIONS)

def make_move(move, player, board):
    # when the player makes a valid move, we need to update the board and flip all the
    # bracketed pieces.
    board[move] = player
    # look for a bracket in any direction
    for d in DIRECTIONS:
        make_flips(move, player, board, d)
    return board

def make_flips(move, player, board, direction):
    # flip pieces in the given direction as a result of the move by player
    bracket = find_bracket(move, player, board, direction)
    if not bracket:
        return
    # found a bracket in this direction
    square = move + direction
    while square != bracket:
        board[square] = player
        square += direction

def get_flip_count(move, player, board):
    flipCount = 0
    for d in DIRECTIONS:
        bracket = find_bracket(move, player, board, d)
        if not bracket:
            continue
        # found a bracket in this direction
        square = move + d
        while square != bracket:
            # board[square] = player
            flipCount += 1
            square += d
    return flipCount

# Monitoring players

# define an exception
class IllegalMoveError(Exception):
    def __init__(self, player, move, board):
        self.player = player
        self.move = move
        self.board = board
    
    def __str__(self):
        return '%s cannot move to square %d' % (PLAYERS[self.player], self.move)

def legal_moves(player, board):
    # get a list of all legal moves for player
    # legal means: move must be an empty square and there has to be is an occupied line in some direction
    return [sq for sq in squares() if is_legal(sq, player, board)]

def any_legal_move(player, board):
    # can player make any moves?
    return any(is_legal(sq, player, board) for sq in squares())

# Putting it all together. Each round consists of:
# - Get a move from the current player.
# - Apply it to the board.
# - Switch players. If the game is over, get the final score.

def play(black_strat, white_strat):
    # play a game of Othello and return the final board and score
    board = initial_board()
    curPlayer = BLACK if random.randint(0, 1) is 0 else WHITE
    curPlayer = WHITE  # TODO TEMP

    while curPlayer is not None:
        curPlayer = next_player(board, curPlayer)
        if curPlayer is not None:
            print(PLAYERS[curPlayer], 'turn')
        print(print_board(board))

        # Only continue if the next player is NOT None, meaning the next player CAN make a legal moves
        if curPlayer is not None:
            move = get_move(black_strat if curPlayer == BLACK else white_strat, curPlayer, board)
            make_move(move, curPlayer, board)
            print(PLAYERS[curPlayer], 'now has', score(curPlayer, board), 'points')

    scoreWhite = score(WHITE, board)
    scoreBlack = score(BLACK, board)
    victoryText = '{} has won!'.format(PLAYERS[BLACK] if scoreBlack > scoreWhite else PLAYERS[WHITE]) if scoreBlack is not scoreWhite else 'Game ended in a tie!'
    print('Game over!\n Final score: Black {}, White {}\n'.format(scoreBlack, scoreWhite), victoryText)

def next_player(board, prev_player):
    # which player should move next?  Returns None if no legal moves exist
    nextPlayer = opponent(prev_player)
    return nextPlayer if any_legal_move(nextPlayer, board) else None

def get_move(strategy, player, board):
    # call strategy(player, board) to get a move
    return strategy(player, board)

def score(player, board):
    return len([sq for sq in board if sq == player])
    # compute player's score (number of player's pieces minus opponent's)
    # pass

# Play strategies
def random_choice_strategy(player, board):
    return random.choice(legal_moves(player, board))

def minimax_strategy(player, board):
    MIN, MAX = 0, 1

    def minimax(move, depth, minmax, player, new_board):
        if depth == 0 or not any_legal_move(player, new_board):
            print('\t' * (2 - depth), '({}) either depth == o ({}) or no legal moves ({})'.format(depth, depth == 0, not any_legal_move(player, new_board)))
            print('\t' * (2 - depth), '({}) flip count: {}'.format(depth, get_flip_count(move, player, new_board)))
            return get_flip_count(move, player, new_board), move

        new_board = make_move(mov, player, new_board)

        if minmax == MAX:
            bestMove = (0, 0)  # (# of squares flipped by move, move)
            print('\t' * (2 - depth), '({}) (MAX) legal moves from {}:'.format(depth, move), legal_moves(player, new_board))
            for nextMove in legal_moves(player, new_board):
                updated_board = make_move(nextMove, player, new_board.copy())
                mm = minimax(nextMove, depth - 1, MIN, opponent(player), updated_board)
                print('\t' * (2 - depth), '({}) (MAX) compare {} to {}: {}'.format(depth, bestMove, mm, max(bestMove, mm)))
                bestMove = max(bestMove, mm)
            return bestMove
        else:
            bestMove = (0, 0)  # (# of squares flipped by move, move)
            print('\t' * (2 - depth), '({}) (MIN) legal moves from {}:'.format(depth, move), legal_moves(player, new_board))
            for nextMove in legal_moves(player, new_board):
                updated_board = make_move(nextMove, player, new_board.copy())
                mm = minimax(nextMove, depth - 1, MAX, opponent(player), updated_board)
                print('\t' * (2 - depth), '({}) (MIN) compare {} to {}: {}'.format(depth, bestMove, mm, min(bestMove, mm)))
                bestMove = min(bestMove, mm)
            return bestMove

    def minimax_simple(move, depth, minmax, player, new_board):
        if depth == 0 or not any_legal_move(player, new_board):
            return get_flip_count(move, player, new_board), move

        if minmax == MAX:
            bestMove = (0, 0)
            for nextMove in legal_moves(player, new_board):
                updated_board = make_move(nextMove, player, new_board.copy())
                bestMove = max(bestMove, minimax(nextMove, depth - 1, MIN, opponent(player), updated_board))
            return bestMove
        else:
            bestMove = (0, 0)
            for nextMove in legal_moves(player, new_board):
                updated_board = make_move(nextMove, player, new_board.copy())
                bestMove = min(bestMove, minimax(nextMove, depth - 1, MAX, opponent(player), updated_board))
            return bestMove

    # square = die we willen (nog moeten) plaatsen
    # player = huidige speler
    # board  = huidige bord, zonder aanpassingen van square
    def minimax_pseudo(square, depth, minmax, player, board):
        if depth == 0 or not any_legal_move(player, board):  # or not any_legal_move():
            return get_flip_count(square, player, board), square
        if minmax == MAX:
            value = 0
            # do move
            updated_board = make_move(square, player, board.copy())
            # check legal moves, after the move above
            for child in legal_moves(player, updated_board):
                value = max(value, minimax_pseudo(child, depth-1, MIN, opponent(player), updated_board))
            return value
        else:  # player == MIN
            value = 0
            # do move
            updated_board = make_move(square, player, board.copy())
            # check legal moves, after the move above
            for child in legal_moves(player, updated_board):
                value = min(value, minimax_pseudo(child, depth-2, MAX, opponent(player), updated_board))
            return value


    bestMove = (0, 0)  # (# of squares flipped by move, move)
    minmaxDepth = 1
    # This for loop is MAX-ing
    for mov in legal_moves(player, board):
        # updated_board = make_move(mov, player, board.copy())
        mm = minimax_pseudo(mov, minmaxDepth - 1, MAX, player, board.copy())
        # print('get max value from {}[0] and {}[0]'.format(bestMove, mm))
        bestMove = max(bestMove, mm)
    print('best move for {} is {}'.format(PLAYERS[player], '{}[1]'.format(bestMove)))
    return bestMove[1]

    # return minimax(origin, 5, MAX)  # TODO return proper bestMove

    # TODO possible shorter version for the code above! Still need some fixing
    #  def get_val(f, v, node):
    #      for child in get_next_moves(node):
    #          bestMove = f(v, minimax(child, depth - 1, MIN))
    #      return bestMove
    #  get_val(min/max, ???, move)

# Start of the program
play(minimax_strategy, random_choice_strategy)

# board = initial_board()
# print(get_flip_count(34, BLACK, board))
# make_move(34, BLACK, board)
# print(print_board(board))

# Theorie vragen te beantwoorden:
#  - Waarom een 1 of 2 dimentionale array gebruiken?
