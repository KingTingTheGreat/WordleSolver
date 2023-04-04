import pygame
from wordlesolver import wordlesolver

if __name__ == '__main__':
    pygame.init()

    pygame.display.set_caption('Wordle Solver by KingTing')

    WIDTH = 600
    HEIGHT = 800
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    SCREEN.fill('white')

    FONT_GUESS = pygame.font.Font('Helvetica.ttf', 75)
    FONT_TITLE = pygame.font.Font('Helvetica.ttf', 80)

    CLOCK = pygame.time.Clock()

    GRAY = (121, 124, 126)
    YELLOW = (198, 179, 102)
    GREEN = (121, 168, 108)
    WHITE = (255, 255, 255)

    WORD_LEN, NUM_GUESSES = 5, 6
    OUTLINE_WIDTH = 4
    BOX_DIM = 100
    BOXES = [[pygame.Surface((BOX_DIM, BOX_DIM))
              for j in range(WORD_LEN)] for i in range(NUM_GUESSES)]
    BOXES_OUTLINES = [[pygame.Surface((BOX_DIM+OUTLINE_WIDTH, BOX_DIM+OUTLINE_WIDTH))
                       for j in range(WORD_LEN)] for i in range(NUM_GUESSES)]
    x_center = WIDTH//2
    x_coords = [x_center - 2*(BOX_DIM+10), x_center - (BOX_DIM+10),
                x_center, x_center + (BOX_DIM+10), x_center + 2*(BOX_DIM+10)]
    coords = [[(x_coords[j], (i+1)*(BOX_DIM+10) + 60)
               for j in range(WORD_LEN)] for i in range(NUM_GUESSES)]
    BOX_RECTS = [[BOXES[i][j].get_rect(center=coords[i][j]) for j in range(
        WORD_LEN)] for i in range(NUM_GUESSES)]
    COLORS = {(i, j): WHITE for j in range(WORD_LEN)
              for i in range(NUM_GUESSES)}
    del x_center, x_coords, coords  # delete variables that are no longer needed

    SOLVER = wordlesolver()


def blit_title() -> None:
    title = FONT_TITLE.render('Wordle Solver', True, 'black')
    title_rect = title.get_rect(center=(WIDTH//2, 75))
    SCREEN.blit(title, title_rect)


def blit_outlines_boxes() -> None:
    for i in range(len(BOXES)):
        for j in range(len(BOXES[i])):
            BOXES[i][j].fill(COLORS[(i, j)])
            BOXES_OUTLINES[i][j].fill('black')
            topleft = BOX_RECTS[i][j].topleft
            SCREEN.blit(BOXES_OUTLINES[i][j], (topleft[0] -
                        OUTLINE_WIDTH//2, topleft[1] - OUTLINE_WIDTH//2))
            SCREEN.blit(BOXES[i][j], BOX_RECTS[i][j])


def blit_guesses(guesses: list) -> None:
    for i, guess in enumerate(guesses):
        for j, box_rect in enumerate(BOX_RECTS[i]):
            guess = guess.upper()
            text = FONT_GUESS.render(guess[j], True, (0, 0, 0))
            text_rect = text.get_rect(center=box_rect.center)
            SCREEN.blit(text, text_rect)


def set_row_color(row: int, color: tuple[int]) -> None:
    """ sets all of the colors in a row to the given color """
    for j in range(WORD_LEN):
        COLORS[(row, j)] = color


def next_color(i_j: tuple[int]) -> tuple[int]:
    """ changes the color of the clicked box to the next color in the sequence 
    GRAY, YELLOW, GREEN, GRAY, YELLOW, GREEN, ... """
    current_color = COLORS[i_j]
    if current_color == WHITE:
        return GRAY
    elif current_color == GRAY:
        return YELLOW
    elif current_color == YELLOW:
        return GREEN
    elif current_color == GREEN:
        return GRAY
    return WHITE


def get_feedback(guess_num: int) -> str:
    """ converts the colors of the boxes to a string of numbers """
    feedback = []
    for j in range(WORD_LEN):
        if COLORS[(guess_num, j)] == WHITE:
            return ''
        elif COLORS[(guess_num, j)] == GRAY:
            feedback.append('0')
        elif COLORS[(guess_num, j)] == YELLOW:
            feedback.append('2')
        elif COLORS[(guess_num, j)] == GREEN:
            feedback.append('1')
        else:
            return ''
    return ''.join(feedback)


def show_error() -> None:
    """ shows an erorr screen when the user enters invalid feedback 
    can only exit this function by exiting the program """
    error_block = pygame.surface.Surface((400, 200))
    error_block.fill((40, 40, 40))
    error_rect = error_block.get_rect(center=(WIDTH//2, HEIGHT//2))

    font_error = pygame.font.Font('Helvetica.ttf', 30)

    text1 = font_error.render('AN ERROR OCCURRED:', True, (255, 255, 255))
    text2 = font_error.render('NO WORDS LEFT', True, (255, 255, 255))
    text3 = font_error.render('PLEASE TRY AGAIN', True, (255, 255, 255))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        SCREEN.fill('red')

        SCREEN.blit(error_block, error_rect)

        SCREEN.blit(text1, text1.get_rect(center=(WIDTH//2, HEIGHT//2 - 50)))
        SCREEN.blit(text2, text2.get_rect(center=(WIDTH//2, HEIGHT//2)))
        SCREEN.blit(text3, text3.get_rect(center=(WIDTH//2, HEIGHT//2 + 50)))

        pygame.display.update()
        CLOCK.tick(60)


if __name__ == '__main__':
    guess = SOLVER.bestGuess()
    guesses = [guess]
    guess_num = 0
    set_row_color(guess_num, GRAY)

    done = False

    error = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if done == False and event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, rect in enumerate(BOX_RECTS[guess_num]):
                    if rect.collidepoint(pos):
                        new_color = next_color((guess_num, i))
                        COLORS[(guess_num, i)] = new_color
                        break
                # add clicking funcionality
            if done == False and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    feedback = get_feedback(guess_num)
                    if not feedback:
                        break
                    SOLVER.processFeedback(guess, feedback)
                    if feedback == '11111':
                        done = True
                        break
                    guess = SOLVER.bestGuess()
                    if guess is None:
                        done = True
                        error = True
                        break
                    guesses.append(guess)
                    guess_num += 1
                    set_row_color(guess_num, GRAY)

        if error:
            show_error()  # will intentionally not return from this function

        SCREEN.fill('white')
        blit_title()
        blit_outlines_boxes()
        blit_guesses(guesses)

        pygame.display.update()
        CLOCK.tick(60)
