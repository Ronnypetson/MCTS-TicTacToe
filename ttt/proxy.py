from tictactoe import TicTacToeBoard
import torch
import torch.nn as nn
from torch.optim import Adam
import torch.nn.functional as F
from mcts import uniform_rollout
from tree import TTTState


class TTTProxy(nn.Module):
    ''' This class is intended to be a learned proxy dynamics,
        such that the reward signals in rollouts are the only
        information used to learn the model.

        In this case, a "proxy" dynamics is a model that should
        return the same rewards as the original dynamics, regardless
        of what is the internal state at each step.

        If such model is learnable, we expect the original states
        to be easily recoverable from the internal states of the model.
    '''
    def __init__(self) -> None:
        ''' For Tic-Tac-Toe, there is no need to provide observations
            other than rewards as inputs - at least we think so. So, we
            are not going to use convolutional layers, as we won't process
            visual input.
        '''
        super().__init__()
        self._num_actions = 9
        state_dim = 9
        action_dim = self._num_actions
        result_dim = 3
        input_dim = state_dim + action_dim
        output_dim = state_dim + result_dim
        self.dynamics = nn.Sequential(nn.Linear(input_dim, 10 * input_dim),
                                      nn.ReLU(),
                                      nn.Dropout(0.5),
                                      nn.Linear(10 * input_dim, output_dim))
        self._state_dim = state_dim
        self._action_dim = action_dim
        self._result_dim = result_dim
    
    def _encode_actions(self,
                        actions: torch.Tensor) -> torch.Tensor:
        ''' Returns the one-hot encodings for the actions:
            (row, column) -> 3 * row + column
            "actions" is a batch of shape B x L
        '''
        assert len(actions.size()) == 2, '"actions" must have shape (B, L)'
        b, l = actions.size()
        num_actions = self._num_actions
        oh_actions = torch.zeros(b, l, num_actions).to(actions.device)
        for batch in range(b):
            for step in range(l):
                oh_actions[batch, step, actions[batch, step]] = 1.0
        return oh_actions

    def forward(self,
                state0: torch.Tensor,
                actions: torch.Tensor,
                max_len: int = 9) -> torch.Tensor:
        ''' "state0" is a batch of initial board states. Shape: B x D_state
            "actions" is a batch of actions for rollouts. Shape: B x L x D_action
                Enconding: (row, column) -> 3 * row + column
            Must return the final state and the results during the episode.
        '''
        actions = self._encode_actions(actions)
        state = state0
        results = []
        for step in range(max_len):
            x = torch.cat([state, actions[:, step]], dim=1)
            x = self.dynamics(x)
            state, result = x[:, :self._state_dim], x[:, self._state_dim:]
            state = F.relu(state)
            result = F.softmax(result, dim=1)
            results.append(result.unsqueeze(1))
        results = torch.cat(results, dim=1)
        return results


if __name__ == '__main__':
    model = TTTProxy()
    batch_size = 32
    seq_length = 9

    board = TicTacToeBoard()
    state = TTTState(board)
    true_actions = []
    for step in range(seq_length):
        state = uniform_rollout(state)
        true_actions.append(state.board.get_played_postion())
    
    print(true_actions)

    state0 = torch.zeros(batch_size, model._state_dim)
    actions = torch.randint(low=0, high=9, size=(batch_size, seq_length)).long()

    print(actions[0])

    results = model(state0, actions)
