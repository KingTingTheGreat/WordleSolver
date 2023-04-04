from wordle_functions import *


class wordlesolver:
    """ a class to solve the Wordle game """

    def __init__(self):
        """ constructor for the wordlesolver class """
        self.possible_words = getAllAnswers()
        self.possible_guesses = getAllGuesses()

    def set_words(self, words):
        """ sets the list of possible words to a list of words """
        self.possible_words = words

    def set_guesses(self, guesses):
        """ sets the list of possible guesses to a list of guesses """
        self.possible_guesses = guesses

    def getFeedback(self):
        """ gets feedback from the user """
        feedback = input("input feedback from Wordle: ")
        while True:
            if len(feedback) == 5 and self.checkAllValidNums(feedback):
                break
            feedback = input("input valid feedback: ")
        return feedback

    def checkAllValidNums(self, feedback):
        """ checks that the feedback from the user only consists of 0, 1, 2 """
        valid_nums = ['0', '1', '2']
        for char in feedback:
            if char not in valid_nums:
                return False
        return True

    def processFeedback(self, guess, feedback):
        """ eliminates words from the list of possible answers based on feedback from the previous guess """
        words = []
        for possible_answer in self.possible_words:
            if createFeedback(guess, possible_answer) == feedback:
                words += [possible_answer]
        self.possible_words = words

    def getFrequencies(self):
        """ returns a dictionary; the key of each entry is a letter and the value is a list representing its frequency in each position in a 5-letter word """
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        letter_frequencies = {letter: [0, 0, 0, 0, 0] for letter in alphabet}

        for possible_answer in self.possible_words:
            for i, letter in enumerate(possible_answer):
                letter_frequencies[letter][i] += 1

        return letter_frequencies

    def scoreWords(self, frequencies):
        """ returns a dictionary; the key of each entry is a word and the value is its score """
        word_scores = {}

        for word in self.possible_words:
            score = 0
            for i, letter in enumerate(word):
                score += frequencies[letter][i]
            word_scores[word] = score

        return word_scores

    def scoreWord(self, word, frequencies, ignore):
        """ returns an integer representing the score of an individual word 
        doesn't count letters in List ignore """
        score = 0
        for i, letter in enumerate(word):

            if len(ignore) >= 3:  # if ignore is not empty, it will have a min length of 3
                if letter in ignore or letter in word[i + 1:]:
                    continue
                score += sum(frequencies[letter])
                continue

            # normal way of calculating scores
            score += frequencies[letter][i]
        return score

    def bestGuess(self):
        """ returns the current best guess """
        if len(self.possible_words) == 0:
            return None
        best_word = self.possible_words[0]
        letter_frequencies = self.getFrequencies()

        # find the number of letters that all possible answers left have in the same position
        same_letters = []
        for letter in "abcdefghijklmnopqrstuvwxyz":
            for freq_pos in letter_frequencies[letter]:
                if freq_pos == len(self.possible_words):
                    same_letters += [letter]

        # use a separate heuristic if all possible answers left have 3 or more letters in the same position
        if len(same_letters) >= 3 and len(self.possible_words) > 2:
            max_score = 0
            for word in self.possible_guesses:
                score = self.scoreWord(word, letter_frequencies, same_letters)
                if score > max_score:
                    max_score = score
                    best_word = word
            return best_word

        # the usual way for choosing the next guess
        max_score = 0
        for word in self.possible_words:
            score = self.scoreWord(word, letter_frequencies, [])

            if score > max_score:
                max_score = score
                best_word = word

        return best_word
