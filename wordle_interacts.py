import time
from wordle_functions import *
from wordlegame import wordlegame
from wordlesolver import wordlesolver

# original average: 3.633693304535637
# original fails: ['homer', 'joker', 'match', 'pound', 'roger', 'shave', 'stash', 'tatty', 'vaunt', 'waste', 'watch', 'wight', 'willy', 'wound']
# new average 1: 3.6233261339092873
# new fails 1: []
# new average 1: 3.621598272138229
# new fails 1: []

def findAverage():
    """ finds the average number of moves for the wordlesolver to solve Wordle """
    start = time.time()
    total_num_guesses = 0
    num_answers_tried = 0
    fails = []
    for answer in getAllAnswers():
        num_answers_tried += 1

        x = wordlegame(answer)
        if x.game_loop_solver() == None:
            fails += [answer]
        total_num_guesses += x.move_num
        
    average = total_num_guesses / num_answers_tried
    print("average number of moves:", str(average))
    print("failed words: ")
    print(fails)
    end = time.time()
    print(end - start)


def useSolver():
    """ a function that allows a user to easily interact with a wordlesolver """
    solver = wordlesolver()
    while True:
        guess = solver.bestGuess()
        print("current guess:", guess)
        feedback = solver.getFeedback()
        solver.processFeedback(guess, feedback)
        if feedback == '11111':
            break

def playGame():
    """ allows the user to play this version of Wordle """
    game = wordlegame(None)
    game.game_loop_player()

if __name__ == "__main__":
    useSolver()
    # playGame()
    # findAverage()