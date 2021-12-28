import numpy as np

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def check_valid_col(self, board):
        fcn_valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                fcn_valid_cols.append(i)
        return fcn_valid_cols
    
    def switch_player(self, num):
            ret = 0
            if num == 1:
                ret = 2
            else:
                ret = 1
            return ret

    def update_board(self, move, player_num, board):
            if 0 in board[:,move]:
                update_row = -1
                for row in range(1, board.shape[0]):
                    update_row = -1
                    if board[row, move] > 0 and board[row-1, move] == 0:
                        update_row = row-1
                    elif row==board.shape[0]-1 and board[row, move] == 0:
                        update_row = row

                    if update_row >= 0:
                        board[update_row, move] = player_num
                        return board
            else:
                err = 'Invalid move by player {}. Column {}'.format(player_num, move)
                raise Exception(err)
            return board

    def get_alpha_beta_move(self, board):

        def max_value(self, state, alpha, beta, depth):
            if depth == 7:
                return self.evaluation_function(state, self.player_number)

            v = float('-inf')
            max_valid_cols = self.check_valid_col(state)

            for a in max_valid_cols:
                maxtemp = state.copy()
                maxtempboard = self.update_board(a, self.player_number, maxtemp)
                v2 = min_value(self, maxtempboard, alpha, beta, depth+1)
                if v2 > v:
                    v = v2
                    alpha = max(alpha, v)
                if v >= beta:
                    return v
            return v

        def min_value(self, state, alpha, beta, depth):
            if depth == 7:
                return self.evaluation_function(state, self.player_number)
            v = float('inf')
            min_valid_cols = self.check_valid_col(state)
            for a in min_valid_cols:
                opp = self.switch_player(self.player_number)
                mintemp = state.copy()
                mintempboard = self.update_board(a, opp, mintemp)
                v2 = max_value(self, mintempboard, alpha, beta, depth+1)
                if v2 < v:
                    v = v2
                    beta = min(beta, v)
                if v <= beta:
                    return v
            return v

        valid_cols = self.check_valid_col(board)
        values = []
        depth = 0
        for col in valid_cols:
            temp = board.copy()
            tempboard = self.update_board(col, self.player_number, temp)
            value = max_value(self, tempboard, float('-inf'), float('inf'), depth+1)
            values.append(value)
        return values.index(max(values))

    def get_expectimax_move(self, board):
                
        def max_value(self, state, player_num, depth, maxdepth):
            v = float('-inf')
            valid_cols = self.check_valid_col(state)
            values_array = []
            for col in valid_cols:
                temp = state.copy()
                maxtempboard = self.update_board(col, player_num, temp)
                v = value(self, maxtempboard, self.switch_player(player_num), depth, maxdepth)
                values_array.append(v)
            return max(values_array)
        
        def exp_value(self, state, player_num, depth, maxdepth):
            v = 0
            valid_cols = self.check_valid_col(state)
            for col in valid_cols:
                temp = state.copy()
                exptempboard = self.update_board(col, player_num, temp)
                p = (1/len(valid_cols))
                v = v + (p * value(self, exptempboard, self.switch_player(player_num), depth, maxdepth))
            return v

        def value(self, state, player_number, depth, maxdepth):
            if depth == maxdepth:
                return self.evaluation_function(state, self.player_number)
            if player_number == self.player_number:
                return max_value(self, state, player_number, depth+1, maxdepth)
            else:
                return exp_value(self, state, player_number, depth+1, maxdepth)

        valid_cols = self.check_valid_col(board)
        values = []
        for col in valid_cols:
            temp = board.copy()
            tempboard = self.update_board(col, self.player_number, temp)
            v = value(self, tempboard, self.player_number, depth=0, maxdepth=3)
            values.append(v)
        return values.index(max(values))

    def evaluation_function(self, board, player_number): 
        four = 1000
        three = 200
        two = 10
        one = 1      
        def check_horizontal(board):
            score = 0
            to_str = lambda a: ''.join(a.astype(str))
            for row in board:
                if player_str4 in to_str(row):
                    score = score + four
                elif player_str3 in to_str(row):
                    score = score + three
                elif player_str2 in to_str(row):
                    score = score + two
                elif player_str1 in to_str(row):
                    score = score + one
            return score

        def check_vertical(board):
            return check_horizontal(board.T)

        def check_diagonal(board):
            for op in [None, np.fliplr]:
                op_board = op(board) if op else board
                root_diag = np.diagonal(op_board, offset=0).astype(np.int)

                score = 0
                if player_str4 in to_str(root_diag):
                    score = score + four
                elif player_str3 in to_str(root_diag):
                    score = score + three
                elif player_str2 in to_str(root_diag):
                    score = score + two
                elif player_str1 in to_str(root_diag):
                    score = score + one

                for i in range(1, board.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(np.int))
                        if player_str4 in diag:
                            score = score + four
                        elif player_str3 in diag:
                            score = score + three
                        elif player_str2 in diag:
                            score = score + two
                        elif player_str1 in diag:
                            score = score + one
            return score

        to_str = lambda a: ''.join(a.astype(str))
        
        player_str4 = '{0}{0}{0}{0}'.format(player_number)
        player_str3 = '{0}{0}{0}'.format(player_number)
        player_str2 = '{0}{0}'.format(player_number)
        player_str1 = '{0}'.format(player_number)
        tempy = board.copy()
        playerscore = check_vertical(tempy) + check_horizontal(tempy) + check_diagonal(tempy)

        opp = self.switch_player(player_number)
        player_str4 = '{0}{0}{0}{0}'.format(opp)
        player_str3 = '{0}{0}{0}'.format(opp)
        player_str2 = '{0}{0}'.format(opp)
        player_str1 = '{0}'.format(opp)
        tempy2 = board.copy()
        oppscore = check_vertical(tempy2) + check_horizontal(tempy2) + check_diagonal(tempy2)

        return (playerscore - oppscore)

class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return np.random.choice(valid_cols)


class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    def get_move(self, board):
        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))
        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))
        
        return move