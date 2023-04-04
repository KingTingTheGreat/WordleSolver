""" functions used by both the wordlesolver and the wordlegame class
this file allows both classes to use these functions without them needing to be written twice or for one to create an instance of the other class """


def getAllAnswers():
    """ returns a list of all possible answers in the Wordle game """
    with open("wordle-answers-alphabetical.txt", 'r') as file:
        answers = []
        for line in file:
            line = line.strip('\n')
            answers.append(line)
    return answers


def getAllGuesses():
    """ returns a list of all allowed guesses in the Wordle game """
    with open('all-guesses.txt', 'r') as file:
        guesses = []
        for line in file:
            line = line.strip('\n')
            guesses.append(line)
    return guesses


def createFeedback(guess, answer):
    """ returns a string representing the feedback of the Wordle game based on a guess and an answer """
    if len(guess) != len(answer):
        return
    g_arr = [guess[i] for i in range(len(guess))]
    a_arr = [answer[i] for i in range(len(answer))]
    f_arr = ['0' for i in range(len(guess))]

    # checking for correct letters in the correct location
    for i, g_letter in enumerate(g_arr):
        if g_arr[i] == a_arr[i]:
            f_arr[i] = '1'
            g_arr[i] = None
            a_arr[i] = None

    # checking for correct letters in the incorrect location
    for i, g_letter in enumerate(g_arr):
        answer_index = indexOf(g_letter, a_arr)
        if g_arr[i] and answer_index != -1:
            f_arr[i] = '2'
            g_arr[i] = None
            a_arr[answer_index] = None

    return ''.join(f_arr)


def indexOf(checkFor, checkIn):
    """ returns the first index of checkFor in checkIn    
    -1 if checkFor is not in checkIn """
    for i, elem in enumerate(checkIn):
        if elem == checkFor:
            return i
    return -1
