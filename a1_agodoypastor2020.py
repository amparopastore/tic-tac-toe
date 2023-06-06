import math
import random

class Player:
      def __init__(self, letter):
            # letter is x or o
            self.letter = letter

      # we want all player to get their next move
      def get_move(self, game):
            pass

class AIPlayer(Player):
      def __init__(self, letter):
            super().__init__(letter)
      
      def get_move(self, game):
            if len(game.available_moves()) == 9:
                  square = random.choice(game.available_moves()) # randomly choose first move
            else:
                  # get square based off minimax algorithm
                  square = self.minimax(game, self.letter)['position']
            return square
      
      def minimax(self, state, player):
            max_player = self.letter
            other_player = 'O' if player == 'X' else 'X'

            if state.current_winner == other_player:
                  return {'position': None,
                          'score': 1 * [state.num_empty_square() + 1] if other_player == max_player else -1 * [state.num_empty_square() + 1]
                          }
            elif not state.empty_square(): # no empty square
                  return {'position': None, 'score': 0}
            
            # initialize some dictionaries
            if player == max_player:
                  best = {'position': None, 'score': -math.inf} # maximize
            else:
                  best = {'position': None, 'score': -math.inf} # minimize

            for possible_move in state.available_moves():
                  # step 1: make a move, try that spot
                  state.make_move(possible_move, player)
                  # step 2: recurse using minimax to simulate a game after making that move
                  sim_score = self.minimax(state, other_player) # now we alterante players
                  
                  # step 3: undo the move
                  state.board[possible_move] = ' '
                  state.current_winner = None
                  sim_score['position'] = possible_move 

                  # step 4: update the dictionaries if necessary
                  if player == max_player:
                        if sim_score['score'] > best['score']:
                              best = sim_score
                  else:
                        if sim_score['score'] < best['score']:
                              best = sim_score


class HumanPlayer(Player):
      def __init__(self, letter):
            super().__init__(letter)

      def get_move(self, game):
            valid_square = False
            val = None
            while not valid_square:
                  square = input(self.letter + '\'s turn. Input move (0-9):')
                  # check this is a valid move
                  try:
                        val = int(square)
                        if val not in game.available_moves():
                              raise ValueError
                        valid_square = True 
                  except ValueError:
                        print('Invalid move. Try again!')

            return

class TicTacToe:
      def __init__(self):
            self.board = [' ' for _ in range(9)] # list represent 3x3 board
            self.current_winner = None # keep track of the winner
      
      def print_board(self):
            for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
                  print('| ' + ' | '.join(row) + ' |')

      @staticmethod
      def print_board_nums():
            number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
            for row in number_board:
                  print('| ' + ' | '.join(row) + ' |')

      def available_moves(self):
            return [i for i, spot in enumerate(self.board) if spot == ' ']
      
      def empty_square(self):
            return ' ' in self.board
      
      def num_empty_squares(self):
            return self.board.count(' ')
      
      def make_move(self, square, letter):
            if self.board[square] == ' ':
                  self.board[square] = letter
                  # check for a winner
                  if self.winner(square, letter):
                        self.current_winner = letter
                  return True
            return False
      
      def winner(self, square, letter):
            # winner if 3 in a row
            # first let's check the rows
            row_ind = square // 3
            row = self.board[row_ind*3 : (row_ind + 1) * 3]
            if all([spot == letter for spot in row]):
                  return True
            
            # check columns
            col_ind = square % 3
            column = [self.board[col_ind+1*3] for i in range(3)]
            if all([spot == letter for spot in column]):
                  return True
            
            # check diagonals (even numbers)
            if square % 2 == 0:
                  diagonal1 = [self.board[i] for i in [0, 4, 8]] # left to right
                  if all([spot == letter for spot in diagonal1]):
                        return True
                  diagonal2 = [self.board[i] for i in [2, 4, 6]] # right to left
                  if all([spot == letter for spot in diagonal2]):
                        return True
            
            # if all checks fail it's a tie
            return False  
      
def play(game, x_player, o_player, print_game=True):
      # returns the winner of the game or None if there's a tie
      if print_game:
            game.print_board_nums()

      letter = 'O' # starting letter
      # iterate while game has empty squares
      while game.empty_square():
            if letter == 'O':
                  square = o_player.get_move(game)
            else:
                  square = x_player.get_move(game)

            # make a move
            if game.make_move(square, letter):
                  if print_game:
                        print(letter + f' makes a move to square {square}')
                        game.print_board()
                        print('') # empty line

                  # is there a winner?
                  if game.current_winner:
                        if print_game:
                              print(letter + 'wins!')
                        return letter

                  # alternate letters, switch players
                  letter = 'O' if letter == 'X' else 'X'

            if print_game:
                  print('It\'s a tie')
                  
if __name__ == '__main__':
      x_player = HumanPlayer('X')
      o_player = AIPlayer('O')
      t = TicTacToe()
      play(t, x_player, o_player, print_game=True)