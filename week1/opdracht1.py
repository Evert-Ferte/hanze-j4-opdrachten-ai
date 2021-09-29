class Node:
    def __init__(self, left: [], right: []):
        self.left = left
        self.right = right

    def to_string(self):
        return str(self.left) + str(self.right)


def dfs(node, visited):
    print('new dfs:', node.to_string())
    if goal_reached(node):
        return True

    visited.add(node)
    for neighbour in get_neighbours(node):
        if is_valid(neighbour):
            # if neighbour not in visited:
            if not contains(neighbour, visited):
                # print('new unvisited node found: {} {}'.format(neighbour.left, neighbour.right))
                if dfs(neighbour, visited):
                    return True

    return False


def goal_reached(node: Node):
    return len(node.left) is 0 and len(node.right) is 4


def contains(item, set):
    for e in set:
        if e.left == item.left and e.right == item.right:
            return True


def is_valid(node: Node):
    if not node.left.__contains__('f'):
        return not ((node.left.__contains__('c') or node.left.__contains__('w')) and node.left.__contains__('g'))
    if not node.right.__contains__('f'):
        return not ((node.right.__contains__('c') or node.right.__contains__('w')) and node.right.__contains__('g'))
    return True


def get_neighbours(node: Node):
    n = []
    farmerLeft = 'f' in node.left
    a = node.left if farmerLeft else node.right
    b = node.right if farmerLeft else node.left

    def swap_chars(char: str, list1: [], list2: [], n: []):
        if char in list1:
            r1 = [e for e in list1 if (e is not char) and (e is not 'f')]
            r2 = list2 + [char, 'f']
            r1.sort()
            r2.sort()
            n.append(Node(r1 if farmerLeft else r2, r2 if farmerLeft else r1))

    # can farmer move without trouble?
    swap_chars('c', a, b, n)
    swap_chars('g', a, b, n)
    swap_chars('w', a, b, n)

    r1 = [e for e in a if e is not 'f']
    r2 = b + ['f']
    r1.sort()
    r2.sort()
    n.append(Node(r1 if farmerLeft else r2, r2 if farmerLeft else r1))

    return n


dfs(Node(['c', 'f', 'g', 'w'], []), set())
# print('gaat tot nu toe goed. bij de laatste stap (waar hij in de output blijft hangen) moet hij weer terug met w, dan alleen terug, en dan terug met g. dan is het klaar')
