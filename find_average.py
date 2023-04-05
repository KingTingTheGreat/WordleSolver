import time
from wordlesolver import wordlesolver
from optimalsolver import optimalsolver
from wordlegame import wordlegame
from wordle_functions import *
from tqdm import tqdm

if __name__ == '__main__':
    all_answers = getAllAnswers()
    total = 0
    for i in tqdm(range(len(all_answers))):
        answer = all_answers[i]
        game = wordlegame(answer)
        solver = optimalsolver('slate')
        moves = game.game_loop_solver(solver)
        if moves:
            total += moves
    average = total / len(all_answers)
    print(average)
