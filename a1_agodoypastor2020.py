# Florida Atlantic University
# Intro to AI, CAP4630, Summer 2023, Dr. Marques
# Project 1: AI Tic-Tac-Toe game
# Author: Amparo Godoy Pastore
# Date: 6/7/2023

import math

# Players
class Player():
    def __init__(self, symbol):
        self.symbol = symbol

    def choose_move(self, game):
        pass

class HumanPlayer(Player):
    def __init__(self, symbol):
        super().__init__(symbol)

    def choose_move(self, game):
        valid_move = False
        while not valid_move:
            move = input('\n' + self.symbol + '\'s turn. Input a move (0-8): ') # human input's their move
            try:
                val = int(move)
                if val not in game.available_moves():
                    raise ValueError
                valid_move = True
            except ValueError:
                print('\nInvalid square. Try again.')
        return val
    
class AIPlayer(Player):
    def __init__(self, symbol):
        super().__init__(symbol)

    def choose_move(self, game):
        move = self.minimax(game, self.symbol, -math.inf, math.inf)['position']
        return move

    def minimax(self, state, player, alpha, beta):
        max_player = self.symbol
        opponent = 'O' if player == 'X' else 'X'

        # check for a winner
        if state.winner == opponent:
            return {'position': None, 'score': 1 * (state.empty_cells() + 1) if opponent == max_player else -1 * (state.empty_cells() + 1)}
        elif state.empty_cells() == 0:
            return {'position': None, 'score': 0}

        best = {'position': None, 'score': -math.inf if player == max_player else math.inf}

        for possible_move in state.available_moves():
            state.place_move(possible_move, player)
            sim = self.minimax(state, opponent, alpha, beta)  # simulate

            # undo move
            state.undo_move(possible_move)
            state.winner = None
            sim['position'] = possible_move  # optimal next move

            if player == max_player:
                if sim['score'] > best['score']:
                    best = sim
                alpha = max(alpha, best['score'])
                if beta <= alpha:
                    break
            else:
                if sim['score'] < best['score']:
                    best = sim
                beta = min(beta, best['score'])
                if beta <= alpha:
                    break

        return best


# Game
class TicTacToe():
    def __init__(self):
        self.board = [' ' for _ in range(9)] # board as a list of nine items
        self.winner = None

    def print_board(self):
        # print the items in the board list in a board format
        for row in [self.board[i*3:(i+1) * 3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    def print_position_board(self):
        # print the board with the positions
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def place_move(self, cell, symbol):
        # place your move on the board
        if cell is None or not isinstance(cell, int) or cell < 0 or cell >= 9:
            return False
        
        if self.board[cell] == ' ': # check cell is empty just in case
            self.board[cell] = symbol 
            if self.is_winner(cell, symbol):
                self.winner = symbol
            return True
        return False
    
    def undo_move(self, move):
        self.board[move] = ' '

    def is_winner(self, cell, symbol):
    # check for winning combinations, or tie
        winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]  # diagonals
        ]

        for combination in winning_combinations:
            if all(self.board[cell] == symbol for cell in combination):
                return True

        return False
    
    def empty_cells(self):
        return self.board.count(' ')
    
    def available_moves(self):
        return [i for i, x in enumerate(self.board) if x == ' ']
    
    def welcome(self):
        print()

def Play(game, x_player, o_player):
    game.print_position_board() # start each game by printing the position board
    symbol = 'X' # X always starts the game
    while game.empty_cells():
        if symbol == 'X':
            cell = x_player.choose_move(game)
        else:
            cell = o_player.choose_move(game)

        if game.place_move(cell, symbol):
            print('\n' + symbol + ' makes a move to square {}'.format(cell) + '\n')
            game.print_board()
            print('') # just an empty line
        
        # check for winner
        if game.winner:
            print(symbol + ' wins')
            ask_play_again()
        
        symbol = 'O' if symbol == 'X' else 'X'  # switch player
    
    # declare tie
    print('\nIt\'s a tie')
    ask_play_again()

def ask_play_again():
    yes_choices = ['yes', 'y']
    no_choices = ['no', 'n']
    while True:
        answer = input('\nPlay again? (yes/no): ')
        if answer.lower() in yes_choices:
            game = TicTacToe()
            print('')
            Play(game, x_player, o_player)

        elif answer.lower() in no_choices:
            print('\nThanks for playing!\n')
            raise SystemExit
        else:
            print('\nEnter yes or no')
            continue


# Main 
if __name__ == '__main__':
    o_player = AIPlayer('O')
    x_player = HumanPlayer('X')
    game = TicTacToe()
    Play(game, x_player, o_player)