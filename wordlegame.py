import random
import time
from wordle_functions import *
from wordlesolver import wordlesolver


class wordlegame:
    """ a class for playing Wordle """

    def __init__(self, answer):
        """ constructor for the wordlegame class """
        all_answers = getAllAnswers()
        if answer not in all_answers:
            answer = random.choice(all_answers)
        self.answer = answer

        self.move_num = 0

    def printWelcome(self):
        """ prints a welcome message for the player """
        print()
        print("Welcome to Wordle!")
        print("The mystery word is a 5-letter English word.")
        print("You have 6 guesses to guess it.")
        print()

    def printFeedback(self, guess):
        """ prints feedback based on the answer and guess """
        feedback = createFeedback(guess, self.answer)
        to_print = ""
        for i, current in enumerate(feedback):
            if current == '0':
                to_print += '_'
            elif current == '1':
                to_print += guess[i]
            elif current == '2':
                to_print += '['
                to_print += guess[i]
                to_print += ']'
            to_print += ' '
        print(to_print)

    def getGuess(self):
        """ gets a guess from the user and returns it """
        guess = input("Type your next guess: ")
        while len(guess) != 5 or not guess.isalpha():
            print("Invalid input. Please try again.")
            guess = input("Type your next guess: ")
        return guess.lower()

    def game_loop_player(self):
        """ a game loop allowing a human to play """
        self.printWelcome()

        solved = False

        while self.move_num < 6:
            self.move_num += 1
            guess = self.getGuess()
            solved = guess == self.answer
            self.printFeedback(guess)
            if solved:
                print()
                print("Good job! You guessed the word in ", end='')
                print(self.move_num, end='')
                print(" guess(es)!")
                break

        if not solved:
            print()
            print("You did not guess the word.")
            print("The answer was: ", end='')
            print(self.answer)
            print("Better luck next time.")

        print()
        print("Thank you for playing!")

    def game_loop_solver(self, solver=None):
        """ a game loop for using the wordlesolver class """
        print("the answer is:", self.answer)

        if not solver:
            solver = wordlesolver()

        solved = False

        while self.move_num < 6:
            # print(self.answer in solver.possible_words)
            self.move_num += 1
            guess = solver.bestGuess()
            # print(guess)
            # self.printFeedback(guess)
            feedback = createFeedback(guess, self.answer)
            solver.processFeedback(guess, feedback)
            solved = guess == self.answer
            if solved:
                return self.move_num
        if not solved:
            # print("failed to solve: ", end='')
            # print(self.answer)
            return None
