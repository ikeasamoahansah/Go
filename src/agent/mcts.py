from .base import Agent
from goboard import MCTSNode

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

    def simulate_random_game(self, game_state):
        pass
