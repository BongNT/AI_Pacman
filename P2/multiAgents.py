# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        pos = currentGameState.getPacmanPosition()
        newFood = currentGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        capsuales = currentGameState.getCapsules()
        newCapsuales = successorGameState.getCapsules()
        "*** YOUR CODE HERE ***"
        scoreEvaluation = 0
        scoreEatFood = 100
        scoreCollisionGhost = float("-inf")
        scoreEatCapsuale = 150
        scoreEatGhost = 50
        if action == Directions.STOP:
            #print("stop")
            scoreEvaluation += -110
        if pos not in capsuales and newPos in capsuales:
            #print("eat capsuale")
            scoreEvaluation += scoreEatCapsuale

        for newGhostState in newGhostStates:
            ghostPosition = newGhostState.getPosition()
            if (manhattanDistance(newPos, ghostPosition) < 2):
                if newGhostState.scaredTimer > 0:
                    scoreEvaluation += scoreEatGhost
                else:
                    return scoreCollisionGhost

        minFood = float("inf")
        for food in newFood:
            minFood = min(minFood, manhattanDistance(food, newPos))
            #print("food",food,newPos)
        #print("min", minFood)

        if minFood == 0:
            return float("inf")
        else:
            scoreEvaluation += (scoreEatFood / minFood)



        return scoreEvaluation + currentGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        return self.minimax(gameState, self.depth * gameState.getNumAgents())[0]
        util.raiseNotDefined()
    def minimax(self, gameState, depth, agent=0):
        '''
        return bestvalue (action, bestEvaluation) using minimax algorithm
        '''

        numAgents = gameState.getNumAgents()
        if depth ==0 or gameState.isWin() or gameState.isLose():
            return (None, self.evaluationFunction(gameState))
        if agent == 0:
            maxval = (None, float("-inf"))
            for action in gameState.getLegalActions(0):
                val = (action, self.minimax( gameState.generateSuccessor(0, action), depth-1, (agent + 1) % numAgents)[1])
                maxval = max(maxval, val, key=lambda val: val[1])
            return maxval
        else:
            minval = (None,float("inf"))
            for action in gameState.getLegalActions(agent):
                val = (action, self.minimax(gameState.generateSuccessor(agent, action), depth-1, (agent+1) % numAgents)[1])
                minval = min(minval, val, key=lambda val: val[1])
            return minval




class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.AlphaBeta(gameState, self.depth * gameState.getNumAgents())[0]
        util.raiseNotDefined()

    def AlphaBeta(self, gameState, depth, agent=0, alpha = float("-inf"), beta = float("inf")):
        '''
                return bestvalue (action, bestEvaluation) using alpha beta pruning algorithm
        '''
        numAgent = gameState.getNumAgents()
        if depth ==0 or gameState.isWin() or gameState.isLose():
            return (None, self.evaluationFunction(gameState))
        if agent ==0:
            maxVal = (None, float("-inf"))
            for action in gameState.getLegalActions(agent):
                val = (action, self.AlphaBeta(gameState.generateSuccessor(agent, action) , depth - 1, (agent + 1) % numAgent, alpha, beta)[1])
                maxVal = max(maxVal, val, key= lambda val: val[1])
                if maxVal[1] > beta:
                    return maxVal
                alpha = max(alpha, maxVal[1])
            return maxVal
        else:
            minVal = (None, float("inf"))
            for action in gameState.getLegalActions(agent):
                val = (action, self.AlphaBeta(gameState.generateSuccessor(agent, action), depth - 1, (agent + 1) % numAgent, alpha, beta)[1])
                minVal = min(minVal, val, key=lambda val: val[1])
                if minVal[1] < alpha:
                    return minVal
                beta = min(beta, minVal[1])
            return minVal


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.expectimax(gameState, self.depth * gameState.getNumAgents())[0]
        util.raiseNotDefined()

    def expectimax(self, gameState, depth, agent=0,):
        '''
                return bestvalue (action, bestEvaluation) using alpha beta pruning algorithm
        '''
        numAgent = gameState.getNumAgents()
        if depth ==0 or gameState.isWin() or gameState.isLose():
            return (None, self.evaluationFunction(gameState))
        if agent ==0:
            maxVal = (None, float("-inf"))
            for action in gameState.getLegalActions(agent):
                val = (action, self.expectimax(gameState.generateSuccessor(agent, action) , depth - 1, (agent + 1) % numAgent)[1])
                maxVal = max(maxVal, val, key= lambda val: val[1])
            return maxVal
        else:
            # minVal = (None, float("inf"))
            # for action in gameState.getLegalActions(agent):
            #     val = (action, self.expectimax(gameState.generateSuccessor(agent, action), depth - 1, (agent + 1) % numAgent, alpha, beta)[1])
            #     minVal = min(minVal, val, key=lambda val: val[1])
            #     if minVal[1] < alpha:
            #         return minVal
            #     beta = min(beta, minVal[1])
            averageVal = 0
            percentage = 1 / len(gameState.getLegalActions(agent))
            for action in gameState.getLegalActions(agent):
                val = (action, self.expectimax(gameState.generateSuccessor(agent, action), depth -1, (agent + 1) % numAgent)[1])
                averageVal += val[1] * percentage
            return (None,averageVal)



def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    evaluationScore = currentGameState.getScore()
    pos = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()
    capsuales = currentGameState.getCapsules()
    foodLeft = len(foods)
    capsualeLeft = len(capsuales)

    if currentGameState.isWin():
        evaluationScore+=50000
    if currentGameState.isLose():
        evaluationScore-=50000

    minDistanceToFood = float("inf")
    for food in foods:
        minDistanceToFood = min(minDistanceToFood, manhattanDistance(food, pos))
    evaluationScore = 1000 / (minDistanceToFood + 1)

    minDistanceToGhost = float("inf")
    for ghost in ghostStates:
        ghostPosition = ghost.getPosition()
        manhattan = manhattanDistance(pos, ghostPosition)
        minDistanceToGhost = min(minDistanceToGhost, manhattan)
        if manhattan < 2:
            if ghost.scaredTimer > 0:
                evaluationScore += 10
            else:
                evaluationScore += -50000

    evaluationScore += 100000 / (foodLeft+1) + 10000/(capsualeLeft +1) + minDistanceToGhost

    return evaluationScore


# Abbreviation
better = betterEvaluationFunction
