class State:
    def __init__(self, left: [], right: []):
        self.left = left.copy()
        self.right = right.copy()

    left = []
    right = []


def turn(left, right):
    # Check for the winning condition
    if len(left) == 0 and len(right) == 4:
        return left, right

    print('Start of turn. State:\t\t', left, right)

    # Put both river side states in a list, relative to the farmer. A will always contain the farm, B not.
    farmerLeft = left.__contains__('f')
    a = left if farmerLeft else right  # A is where the farmer is
    b = right if farmerLeft else left  # B is where the farmer is NOT

    # Start by moving the farmer first
    a.remove('f')
    b.append('f')

    # We then sort characters (necessary for tracking the history)
    a.sort()
    b.sort()

    # Loop through the river side to see what item the farmer can take with him
    validStateFound = False
    for e in a:
        # Move E from A to B
        newA = a.copy()
        newA.remove(e)
        newB = b.copy() + [e]
        newA.sort()
        newB.sort()

        # Check if the move we just made is valid
        if valid(State(newA if farmerLeft else newB, newB if farmerLeft else newA)):
            # Set the new state
            left = newA if farmerLeft else newB
            right = newB if farmerLeft else newA
            validStateFound = True
            break

    # If no valid state was found, backtrack
    if not validStateFound and not valid(State(a if farmerLeft else b, b if farmerLeft else a)):
        del stack[-1]

        print('      Backtracking...')

        left = stack[len(stack) - 1].left
        right = stack[len(stack) - 1].right
    # Else, continue like normal
    else:
        # Save the new state, and add to the stack
        visited.append(State(left, right))
        stack.append(State(left, right))

    print('  End of turn. State:\t\t', left, right, '\n')

    left, right = turn(left, right)
    return left, right


def valid(state: State):
    # Check if the left and right side contain the cabbage and goat or the wolf and goat (they can only go together if the farmer is there)
    if not state.left.__contains__('f'):
        return (state.left.__contains__('c') and state.left.__contains__('g')) or (state.left.__contains__('w') and state.left.__contains__('g'))

    if not state.right.__contains__('f'):
        return (state.right.__contains__('c') and state.right.__contains__('g')) or (state.right.__contains__('w') and state.right.__contains__('g'))

    # The state is invalid if we have already visited this state
    for e in visited:
        if e.left == state.left and e.right == state.right:
            return False

    return True


left, right = ['c', 'f', 'g', 'w'], []
visited = [State(left, right), ]
stack = [State(left, right)]

# Entry point
left, right = turn(left, right)

print('Finished game in {turns} turns!\nGame state: {left} {right}'.format(turns=len(stack) - 1, left=left, right=right))


# # Helper functions
# def print_stack():
#     p = [str(e.left) + str(e.right) for e in stack]
#     print('\tstack', p)
#
#
# def log_history():
#     for e in visited:
#         print(e.left, e.right)
