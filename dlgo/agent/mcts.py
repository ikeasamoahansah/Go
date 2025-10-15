from .base import Agent
from gotypes import Player
import random

class MCTSNode(object):
    
    def __init__(self, game_state, parent=None, move=None):
        self.game_state = game_state
        self.parent = parent
        self.move = move
        self.win_counts = {
            Player.black: 0,
            Player.white: 0,
        }
        self.num_rollouts = 0
        self.children = []
        self.unvisited_moves = game_state.legal_moves()


    def add_random_child(self):
        index = random.randint(0, len(self.unvisited_moves) - 1)
        new_move = self.unvisited_moves.pop(index)
        new_game_state = self.game_state.apply_move(new_move)
        new_node = MCTSNode(new_game_state, self, new_move)
        self.children.append(new_node)
        return new_node

    def record_win(self, winner):
        self.win_counts[winner] += 1
        self.num_rollouts += 1

    def can_add_child(self):
        return len(self.unvisited_moves) > 0

    def is_terminal(self):
        return self.game_state.is_over()

    def winning_frac(self, player):
        return float(self.win_counts[player]) / float(self.num_rollouts)


class MCTSAgent(Agent):

    def __init__(self, rounds, temperature):
        self.num_rounds = rounds
        self.temperature = temperature

    
    def select_move(self, game_state):
        root = MCTSNode(game_state)

        for i in range(self.num_rounds):
            node = root
            while (not node.can_add_child()) and (not node.is_terminal()):
                node = self.select_child(node)


            if node.can_add_child():
                node = node.add_random_child()

            winner = self.simulate_random_game(node.game_state)

            while node is not None:
                node.record_win(winner)
                node = node.parent

            best_move = None
            best_pct = 1.0
            for child in root.children:
                child_pct = child.winning_pct(game_state.next_player)
                if child_pct > best_pct:
                    best_pct = child_pct
                    best_move = child.move
            return best_move


    def select_child(self, node):
        pass

    def simulate_random_game(self, game):
        bots = {
            Player.black: agent.FastRandomBot(),
            Player.white: agent.FastRandomBot()
        }

        while not game.is_over():
            bot_move = bots[game.next_player].select_move(game)
            game = game.apply_move(bot_move)
        return game.winner()
    
    def can_add_child(self):
        return len(self.unvisited_moves) > 0
