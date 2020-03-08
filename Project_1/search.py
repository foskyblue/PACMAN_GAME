# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    print('########################', str(problem))
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

########################################################################################################################
#   With suggests in the documents and also what we studied for the algorithms of several search functions, we decided
# to extract a main method for all other search methods. For the better reuse and understandability.
#   Method description: With the format information of problem.getStartState() == (5,5),
# problem.isGoalState(problem.getStartState()) == False, and problem.getSuccessors(problem.getStartState()) ==
# [((5, 4), 'South', 1), ((4, 5), 'West', 1)]
# path_to_goal == ['West', 'West', 'West', 'West', 'South', 'South', 'East', 'South', 'South', 'West']
#   We push the general search as the format below and make a list to make sure each coordinate is visited or not.
#   Make a loop with condition of if the algorithm is not empty, then keep running
#   pop()(remove) coordinate and move to the next, and set the current_state
#   If goal state == True for current state, run a roop in the path finding, if x[1] data not empty,  add x[1] to
# path_to_goal.
# Else will check whether the current_state is visited, if not, add to visited.
# Later on, run the roop for successor states for current_state, and add each successtors for current state.
# Last step, push the succesor paths to the algorithm.
########################################################################################################################
def graphFindPath(problem, algorithm):

    algorithm.push([(problem.getStartState(), "", 0)])
    visited_states = []

    while not algorithm.isEmpty():
        path = algorithm.pop()
        current_state = path[-1][0]

        if problem.isGoalState(current_state):
            path_to_goal = []
            for x in path:
                if len(x[1]) != 0:
                    path_to_goal.append(x[1])
            print('path_to_goal', path_to_goal)
            return path_to_goal

        else:
            if current_state not in visited_states:
                visited_states.append(current_state)

                for successor in problem.getSuccessors(current_state):
                    if successor[0] not in visited_states:
                        successorPath = path[:]
                        successorPath.append(successor)
                        algorithm.push(successorPath)

    return (problem, algorithm)


# As we studied the util.py, we find that several methods are related to the search algorithms.
# We choose the Stack function which using the last-in-first-out logic for DFS.
# Then we provide the stack algorithm and return to the graphFindPath method for finding the possible path.
def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    stack = util.Stack()
    return graphFindPath(problem, stack)

# As we studied the util.py, we find that several methods are related to the search algorithms.
# We choose the Queue function which using the first-in-first-out logic for DFS.
# Then we provide the stack algorithm and return to the graphFindPath method for finding the possible path.
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    queue = util.Queue()

    return graphFindPath(problem, queue)


# AS some parts of the condition of input changed from the graphFindPath, we decided to implement the function first
# and refactor it later.
# the difference from above is that PrioQ has a new value, count. It will count the priority and remove the least
# prority target in the list. So, we name it as cost.
# We add a new value that are same with path and call it as actions.
def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()

    visited_states = []
    algorithm = util.PriorityQueue()
    algorithm.push((problem.getStartState(), []), 0)
    cost = 0
    while not algorithm.isEmpty():
        path,actions = algorithm.pop()

        if problem.isGoalState(path):
            return actions

        else:
            if path not in visited_states:
                visited_states.append(path)

                for successor in problem.getSuccessors(path):
                    if successor[0] not in visited_states:
                        directions = successor[1]
                        cost = actions + [directions]
                        algorithm.push((successor[0],cost),problem.getCostOfActions(cost))
    return actions


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0
# The main algorithm of a search is based on uniformCostSearch + heuristic
# This search is similar to uniformCostSearch, the main structure is the same, adding nullHeuristic in the push
# as the count part. Later on, adding nullCost below the original cost and push it(thisis just let the result push of
# problem.getCostOfActions(cost) + heuristic(successor[0], problem))
def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    "Search the node that has the lowest combined cost and heuristic first."
    visited_states = []
    algorithm = util.PriorityQueue()
    algorithm.push((problem.getStartState(), []), nullHeuristic(problem.getStartState(), problem))
    cost = 0
    while not algorithm.isEmpty():
        path, actions = algorithm.pop()

        if problem.isGoalState(path):
            return actions

        else:
            if path not in visited_states:
                visited_states.append(path)

                for successor in problem.getSuccessors(path):
                    if successor[0] not in visited_states:
                        directions = successor[1]
                        cost = actions + [directions]
                        nullCost = problem.getCostOfActions(cost) + heuristic(successor[0], problem)
                        algorithm.push((successor[0], cost), nullCost)
        visited_states.append(path)
    return actions
    #util.raiseNotDefined()
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
