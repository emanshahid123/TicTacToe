## import time

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def print_board(self):
        print()
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')
        print()

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([s == letter for s in row]):
            return True

        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([s == letter for s in column]):
            return True

        if square % 2 == 0:
            diag1 = [self.board[i] for i in [0, 4, 8]]
            if all([s == letter for s in diag1]):
                return True
            diag2 = [self.board[i] for i in [2, 4, 6]]
            if all([s == letter for s in diag2]):
                return True

        return False

# Minimax with Alpha-Beta Pruning
def minimax_ab(state, player, maximizing, alpha, beta):
    max_player = 'O'
    other_player = 'X' if player == 'O' else 'O'

    if state.current_winner == other_player:
        return {
            'position': None,
            'score': 1 * (len(state.available_moves()) + 1) if other_player == max_player else -1 * (len(state.available_moves()) + 1)
        }

    if not state.empty_squares():
        return {'position': None, 'score': 0}

    if maximizing:
        best = {'position': None, 'score': -float('inf')}
        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = minimax_ab(state, other_player, False, alpha, beta)
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move

            if sim_score['score'] > best['score']:
                best = sim_score
            alpha = max(alpha, sim_score['score'])
            if beta <= alpha:
                break
    else:
        best = {'position': None, 'score': float('inf')}
        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = minimax_ab(state, other_player, True, alpha, beta)
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move

            if sim_score['score'] < best['score']:
                best = sim_score
            beta = min(beta, sim_score['score'])
            if beta <= alpha:
                break

    return best

# Full Game Loop
def play_game():
    print("Welcome to Tic-Tac-Toe!")
    game = TicTacToe()
    human = 'X'
    ai = 'O'

    game.print_board()

    while game.empty_squares():
        # Human move
        valid_move = False
        while not valid_move:
            try:
                move = int(input("Your move (0-8): "))
                if move not in game.available_moves():
                    raise ValueError
                valid_move = True
                game.make_move(move, human)
            except ValueError:
                print("Invalid move. Try again.")

        game.print_board()

        if game.current_winner:
            print("You win! 🎉")
            return

        if not game.empty_squares():
            break

        # AI move
        print("AI is thinking...")
        move = minimax_ab(game, ai, True, -float('inf'), float('inf'))['position']
        game.make_move(move, ai)
        print(f"AI places at position {move}")
        game.print_board()

        if game.current_winner:
            print("AI wins! 🤖")
            return

    print("It's a draw! 🤝")

# Comparison Function
def compare_algorithms():
    game = TicTacToe()

    print("Comparing Minimax without Alpha-Beta...")
    def basic_minimax(state, player, maximizing):
        max_player = 'O'
        other_player = 'X' if player == 'O' else 'O'

        if state.current_winner == other_player:
            return {
                'position': None,
                'score': 1 * (len(state.available_moves()) + 1) if other_player == max_player else -1 * (len(state.available_moves()) + 1)
            }

        if not state.empty_squares():
            return {'position': None, 'score': 0}

        if maximizing:
            best = {'position': None, 'score': -float('inf')}
        else:
            best = {'position': None, 'score': float('inf')}

        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = basic_minimax(state, other_player, not maximizing)
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move

            if maximizing:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score

        return best

    start = time.time()
    basic_minimax(game, 'O', True)
    print(f"Minimax time: {time.time() - start:.6f} seconds")

    game = TicTacToe()
    start = time.time()
    minimax_ab(game, 'O', True, -float('inf'), float('inf'))
    print(f"Alpha-Beta time: {time.time() - start:.6f} seconds")

# Run everything
if __name__ == '__main__':
    compare_algorithms()
    play_game()