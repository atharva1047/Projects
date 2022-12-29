import game_rules, random
###########################################################################
# Explanation of the types:
# The board is represented by a row-major 2D list of characters, 0 indexed
# A point is a tuple of (int, int) representing (row, column)
# A move is a tuple of (point, point) representing (origin, destination)
# A jump is a move of length 2
###########################################################################

# I will treat these like constants even though they aren't
# Also, these values obviously are not real infinity, but close enough for this purpose
NEG_INF = -1000000000
POS_INF = 1000000000

class Player(object):
    """ This is the player interface that is consumed by the GameManager. """
    def __init__(self, symbol): self.symbol = symbol # 'x' or 'o'

    def __str__(self): return str(type(self))

    def selectInitialX(self, board): return (0, 0)
    def selectInitialO(self, board): pass

    def getMove(self, board): pass

    def h1(self, board):
        return -len(game_rules.getLegalMoves(board, 'o' if self.symbol == 'x' else 'x'))


# This class has been replaced with the code for a deterministic player.
class MinimaxPlayer(Player):
    def __init__(self, symbol, depth): 
        super(MinimaxPlayer, self).__init__(symbol)
        self.depth = depth

    # Leave these two functions alone.
    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    # Edit this one here. :)
    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)

        topLayerScoresDict = {}

        for i in range(len(legalMoves)):
            tmp_board = game_rules.makeMove(board, legalMoves[i])

            topLayerScoresDict[legalMoves[i]] = self.minimaxByAtharva(tmp_board, self.depth - 1, False)
        
        
        finalMove = list(topLayerScoresDict.keys())[list(topLayerScoresDict.values()).index(max(list(topLayerScoresDict.values())))]


        #printFile = open('printLog.txt','a')
        #printFile.write(str(finalMove) + ", " + str(finalScore) + ", " + str(self.symbol) + "\n")
        
        if len(legalMoves) > 0: return finalMove
        else: return None
    
    def minimaxByAtharva(self, board, depth, maximizer):

        if maximizer == False and self.symbol == 'x':
            opponantSymbol = 'o'

        if maximizer == True and self.symbol == 'x':
            opponantSymbol = 'x'
        
        if maximizer == False and self.symbol == 'o':
            opponantSymbol = 'x'
        
        if maximizer == True and self.symbol == 'o':
            opponantSymbol = 'o'

        legalMoves = game_rules.getLegalMoves(board, opponantSymbol)
        
        if depth == 0 or len(legalMoves) == 0:
            return self.h1(board)

        if maximizer:
            maxScore = NEG_INF
            for move in legalMoves:
                updated_board = game_rules.makeMove(board, move)
                score = self.minimaxByAtharva(updated_board, depth - 1, False)
                maxScore = max(maxScore, score)
            return maxScore

        else:
            minScore = POS_INF
            for move in legalMoves:
                updated_board = game_rules.makeMove(board, move)
                score = self.minimaxByAtharva(updated_board, depth - 1, True)
                minScore = min(minScore, score)
            return minScore



# This class has been replaced with the code for a deterministic player.
class AlphaBetaPlayer(Player):
    def __init__(self, symbol, depth): 
        super(AlphaBetaPlayer, self).__init__(symbol)
        self.depth = depth

    # Leave these two functions alone.
    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    # Edit this one here. :)
    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        topLayerScoresDict = {}

        for i in range(len(legalMoves)):
            tmp_board = game_rules.makeMove(board, legalMoves[i])

            topLayerScoresDict[legalMoves[i]] = self.minimaxAplhaBetaByAtharva(tmp_board, self.depth - 1, False, NEG_INF, POS_INF)
        
        
        finalMove = list(topLayerScoresDict.keys())[list(topLayerScoresDict.values()).index(max(list(topLayerScoresDict.values())))]

        if len(legalMoves) > 0: return finalMove
        else: return None

    def minimaxAplhaBetaByAtharva(self, board, depth, maximizer, alpha, beta):

            #printFile = open('printLog.txt','a')
            #printFile.write(str(maximizer) + "    " + str(self.symbol) + "\n")

            if maximizer == False and self.symbol == 'x':
                opponantSymbol = 'o'

            if maximizer == True and self.symbol == 'x':
                opponantSymbol = 'x'
            
            if maximizer == False and self.symbol == 'o':
                opponantSymbol = 'x'
            
            if maximizer == True and self.symbol == 'o':
                opponantSymbol = 'o'

            legalMoves = game_rules.getLegalMoves(board, opponantSymbol)

            
            if depth == 0 or len(legalMoves) == 0:
                return self.h1(board)

            if maximizer:
                maxScore = NEG_INF
                for move in legalMoves:
                    updated_board = game_rules.makeMove(board, move)
                    score = self.minimaxAplhaBetaByAtharva(updated_board, depth - 1, False, alpha, beta)
                    maxScore = max(maxScore, score)
                    alpha = max(alpha, score)

                    if beta <= alpha:
                        break
                return maxScore

            else:
                minScore = POS_INF
                for move in legalMoves:
                    updated_board = game_rules.makeMove(board, move)
                    score = self.minimaxAplhaBetaByAtharva(updated_board, depth - 1, True, alpha, beta)
                    minScore = min(minScore, score)
                    beta = min(beta, score)

                    if beta <= alpha:
                        break
                return minScore


class RandomPlayer(Player):
    def __init__(self, symbol):
        super(RandomPlayer, self).__init__(symbol)

    def selectInitialX(self, board):
        validMoves = game_rules.getFirstMovesForX(board)
        return random.choice(list(validMoves))

    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return random.choice(list(validMoves))

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return random.choice(legalMoves)
        else: return None


class DeterministicPlayer(Player):
    def __init__(self, symbol): super(DeterministicPlayer, self).__init__(symbol)

    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return legalMoves[0]
        else: return None


class HumanPlayer(Player):
    def __init__(self, symbol): super(HumanPlayer, self).__init__(symbol)
    def selectInitialX(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')
    def selectInitialO(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')
    def getMove(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')


def makePlayer(playerType, symbol, depth=1):
    player = playerType[0].lower()
    if player   == 'h': return HumanPlayer(symbol)
    elif player == 'r': return RandomPlayer(symbol)
    elif player == 'm': return MinimaxPlayer(symbol, depth)
    elif player == 'a': return AlphaBetaPlayer(symbol, depth)
    elif player == 'd': return DeterministicPlayer(symbol)
    else: raise NotImplementedException('Unrecognized player type {}'.format(playerType))

def callMoveFunction(player, board):
    if game_rules.isInitialMove(board): return player.selectInitialX(board) if player.symbol == 'x' else player.selectInitialO(board)
    else: return player.getMove(board)
