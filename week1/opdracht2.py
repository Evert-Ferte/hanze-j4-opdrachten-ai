import random
import string


class Node:
    def __init__(self, x: int = 0, y: int = 0, val: str = ''):
        self.x = x
        self.y = y
        self.val = val
        self.visited = False

    def get_string(self):
        return '{val} at ({x}, {y}) ({vis})'.format(val=self.val, x=self.x, y=self.y, vis=self.visited)


def create_prefixes():
    p, w = set(), set()
    with open('boggle/words_NL.txt', 'r') as f:
        for word in f:
            word = word.replace("\n", "")
            for i in range(1, len(word)):
                p.add(word[:i].lower())
            p.add(word)
            w.add(word)
    return p, w


def fill_board():
    for i in range(size * size):
        board[i % size][int(i / size)] = Node(i % size, int(i / size), random.choice(string.ascii_letters).lower())


def print_board():
    p = ''
    for i in range(size * size):
        p += ' {} '.format(board[i % size][int(i / size)].val) + ('\n' if i % size >= size - 1 else '')
    print(p)


def match_words():
    # loop through the board (from top left, to bottom right)
    for y in range(size):
        for x in range(size):
            found, word = dfs(board[x][y], set(), board[x][y].val)

            if found:
                foundWords.append(word)

            reset_nodes()


def dfs(node, visited, word):
    if word in words:
        return True, word

    visited.add(node)
    for neighbour in neighbours(node):
        if neighbour not in visited:
            if word + neighbour.val in prefixes:
                found, word = dfs(neighbour, visited, word + neighbour.val)
                if found:
                    return True, word

    # We only get here if all else fails
    return False, word[:-1]


def neighbours(node):
    def get_index(i: int):
        return i % size

    l = []
    x, y = node.x, node.y
    l.append(board[get_index(x - 1)][get_index(y)])
    l.append(board[get_index(x)][get_index(y + 1)])
    l.append(board[get_index(x + 1)][get_index(y)])
    l.append(board[get_index(x)][get_index(y - 1)])
    return l


def reset_nodes():
    for y in range(size):
        for x in range(size):
            board[x][y].visited = False


size = 4
board = [[Node()] * size for i in range(size)]
prefixes, words = create_prefixes()
foundWords = []

fill_board()
match_words()
print('Here is a list of the {} word(s) I found:'.format(len(foundWords)), foundWords)
print_board()
