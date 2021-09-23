class Node:
    def __init__(self, x: int = 0, y: int = 0, val: str = ''):
        self.x = x
        self.y = y
        self.val = val
        self.visited = False

    def get_string(self):
        return '{val} at ({x}, {y}) ({vis})'.format(val=self.val, x=self.x, y=self.y, vis=self.visited)


def create_prefixes(words):
    list = {}

    for word in words:
        pref = []
        for i in range(2, len(word)):
            pref.append(word[:i])
        pref.append(word)

        list[pref[0][:-1]] = pref
    return list


def fill_board(template):
    i = 0
    for y in range(size):
        for x in range(size):
            board[x][y] = Node(x, y, template[i])
            i += 1


def print_board():
    p = ''
    for y in range(size):
        for x in range(size):
            p += ' {e} '.format(e=board[x][y].val) + ('\n' if x >= 3 else '')
    print(p)


def match_words():
    # loop through the board (from top left, to bottom right)
    i = 0
    for y in range(size):
        for x in range(size):
            print('iteration', i, '({e})'.format(e=str(board[x][y].val)))

            # get the current letter and check if it exists in the dictionary
            e = str(board[x][y].val)
            if prefixes.get(e) is not None:
                # check top, right, bottom, left
                stack = get_neighbours(x, y)

                board[x][y].visited = True
                found, word = find_word(e, stack)
                if found:
                    print('\tword found:', word)
                    foundWords.append(word)

                # reset all visited nodes
                reset_nodes()
                stack.clear()

            i += 1

    # Print the final list that contains all the words found
    print('\nFinished. Here is a list of the words I found:', foundWords)
    print_board()


def find_word(word: str, stack):
    # finish condition
    if len(stack) <= 0 or len(word) == len(prefixes[word[:1]]) + 1:
        if len(stack) <= 0:
            return False, ''
        return True, str(word)

    # get the top/last element of the stack
    e = stack[len(stack) - 1]
    e.visited = True
    word += e.val

    isMatch = word == prefixes[word[:1]][len(word) - 2]

    if not isMatch:
        backtrackAmount = 1
        if len(stack) > 1:
            if stack[len(stack) - 2].visited:
                backtrackAmount = 2

        del stack[-backtrackAmount]
        isMatch, word = find_word(word[:-backtrackAmount], stack)
    else:
        # add neighbours to stack (excluding already visited)
        stack.extend(get_neighbours(e.x, e.y))
        isMatch, word = find_word(word, stack)

    return isMatch, word


def get_neighbours(x, y):
    l = []
    if not board[get_index(x - 1)][get_index(y)].visited:
        l.append(board[get_index(x - 1)][get_index(y)])
    if not board[get_index(x)][get_index(y + 1)].visited:
        l.append(board[get_index(x)][get_index(y + 1)])
    if not board[get_index(x + 1)][get_index(y)].visited:
        l.append(board[get_index(x + 1)][get_index(y)])
    if not board[get_index(x)][get_index(y - 1)].visited:
        l.append(board[get_index(x)][get_index(y - 1)])
    return l


def get_index(i: int):
    return i % size


def reset_nodes():
    for y in range(size):
        for x in range(size):
            board[x][y].visited = False


size = 4
board = [[Node()] * size for i in range(size)]
template = ['p', 'i', 'e', 't', 'g', 'a', 'a', 't', 'a', 't', 'm', 's', 'h', 'u', 'i', 's']

words = ['huis', 'mat', 'tas', 'ei']
prefixes = create_prefixes(words)
foundWords = []

fill_board(template)
print_board()
match_words()
