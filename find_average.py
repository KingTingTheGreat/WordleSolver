import time
from wordlesolver import wordlesolver
from optimalsolver import optimalsolver
from wordlegame import wordlegame
from wordle_functions import *

if __name__ == '__main__':
    all_answers = getAllAnswers()
    total = 0
    for i, answer in enumerate(all_answers):
        if i % 100 == 0:
            print(i)
        game = wordlegame(answer)
        solver = optimalsolver('slate')
        moves = game.game_loop_solver(solver)
        if moves:
            total += moves
    average = total / len(all_answers)
    print(average)
