from copy import deepcopy
from tictactoe import TicTacToeBoard
from tree import TTTState
from math import sqrt, log
import numpy as np


def UCT(node: TTTState, child: TTTState, c: float = 1.141) -> float:
    ''' Returns Upper Confidence Bound of a node wrt the given child.
    '''
    ratio = 0.0 if child.N == 0 else child.Q / child.N
    # Square Root of Log
    SRL = 0.0 if child.N == 0 or node.N == 0 else sqrt(log(node.N) / child.N)
    uct = ratio + c * SRL
    return uct


def traverse(node: TTTState) -> TTTState:
    ''' Picks unvisited child of first node which is not fully-expanded.
        Uses UCT to select the path.
    '''
    current = node
    current.set_children()
    while current.is_expanded():
        ucts = [UCT(current, child) for child in current.children]
        chosen = np.argmax(ucts)
        current = current.children[chosen]
        current.set_children()
    if len(current.children) == 0:
        return None
    unvisited_children = [child for child in current.children if not child.visited]
    child_id = np.random.randint(0, len(unvisited_children))
    leaf = unvisited_children[child_id]
    return leaf


def uniform_rollout(node: TTTState) -> TTTState:
    ''' Returns a child node by the default rollout policy,
        which is to pick uniformly random.
    '''
    if len(node.children) == 0:
        node.set_children()
    child_id = np.random.randint(0, len(node.children))
    child = node.children[child_id]
    return child


def rollout(node: TTTState, policy: object):
    ''' Returns the result of a random rollout with policy "policy"
    '''
    current = node
    while not current.board.finished():
        current = policy(current)
    return current.board.check_winner()


def backpropagate(node: TTTState, result):
    ''' Updates the statistics of nodes along the path
        from root to leaf.
    '''
    assert result in [None, 'x', 'o'], '"result" must be None, "x", or "o"'
    node.increase_N()
    if result is None:
        node.increase_draw()
    elif result != node.board._current_player:
        node.increase_Q()
    if node.parent:
        backpropagate(node.parent, result)


def MCTS(root: TTTState, num_iter: int = 200) -> TTTState:
    ''' Performs "num_iter" simulations of Monte-Carlo Tree Search
        and returns the selected next move.
    '''
    root.set_children()
    for _ in range(num_iter):
        leaf = traverse(root)
        if leaf is None:
            continue
        leaf.visited = True
        result = rollout(leaf, uniform_rollout)
        backpropagate(leaf, result)
    child_id = np.argmax([child.N for child in root.children])
    return root.children[child_id]


if __name__ == '__main__':
    first_player = 'x'
    board0 = TicTacToeBoard(first_player)
    state0 = TTTState(board0)
    state0.visited = True
    state0.set_children()
    history = [state0]

    stateT = history[-1]
    while not stateT.board.finished():
        print(stateT.board)
        stateT = MCTS(stateT, num_iter=1000)
        history.append(stateT)
    print(stateT.board)
