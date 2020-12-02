import os, logging

import pygame

import api

#links
images_path = r"sources\\images"
LOG_FILENAME = r"errors.txt"
icon = pygame.image.load(r"sources\\icon\\icon_papyrus.png")

#logging
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
logging.debug('This message should go to the log file')

try:
    word_myst = api.random_word()
    definition = api.get_definition(word_myst)
    synonyms = api.get_synonyms(word_myst)
    letters_missed = []
    letters_found = []
    trials = 0

    pygame.init()

    # color lib
    white = (255, 255, 255)
    black = (0, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 128)
    grey = (200, 200, 200)
    beige = (255, 200, 200)
    font = pygame.font.SysFont('arial', 32)
    text_title = pygame.font.SysFont('arial', 16)
    text_normal = pygame.font.SysFont('arial', 14)
    text_small = pygame.font.SysFont('arial', 12)

    # screen size
    X = 750
    Y = 500

    display_surface = pygame.display.set_mode((X, Y))
    pygame.display.set_caption('Hangman')
    pygame.display.set_icon(icon)

    # btn start
    text = font.render('Start', True, black, white)
    text_light = font.render('Start', True, grey, white)
    textRect = text.get_rect()
    textRect.center = (X - 100, Y - 450)


    def main_game():
        letters = []

        # infinite loop
        while True:
            display_surface.fill(white)
            display_surface.blit(text, textRect)
            line_letter(word_myst)
            for i in letters:
                guess_letter(i, word_myst)
            image_hangman()
            image_win()
            show_wrong_letters()
            # look for user's events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                mouse = pygame.mouse.get_pos()
                click = pygame.mouse.get_pressed()
                if (X - 150) < mouse[0] < (X - 50) and (Y - 500) < mouse[1] < (Y - 400):
                    display_surface.blit(text_light, textRect)
                    if click[0] == 1:
                        refresh_word()
                        main_game()

                if event.type == pygame.KEYDOWN:
                    letter = pygame.key.name(event.key)
                    letters.append(letter)

                pygame.display.update()


    def guess_letter(letter, word):
        x = 0
        y = Y - 135
        word = word.lower()
        if letter in word:
            for i in word:
                x += 52.5
                if i == letter:
                    letter_guessed = font.render(letter, True, black, white)
                    display_surface.blit(letter_guessed, (x, y))
                    if letter not in letters_found:
                        letters_found.append(letter)

        else:
            global letters_missed
            if letter not in letters_missed:
                letters_missed.append(letter)


    def image_hangman():
        global letters_missed
        len_l = len(letters_missed)
        if 0 < len_l < 10:
            image_num = f"pole_{len_l}"
            im = import_image(name=image_num)
            display_surface.blit(im, (50, 0))
        elif 10 <= len_l:
            im = import_image("lost")
            display_surface.blit(im, (50, 0))
            show_definition()


    def import_image(name):
        path = os.path.join(images_path, f"{name}.jpg")
        return pygame.image.load(path)


    def image_win():
        tot_letters = 0
        for i in word_myst.lower():
            if i in letters_found:
                tot_letters += 1

        if tot_letters == len(word_myst):
            im = import_image("win")
            display_surface.blit(im, (50, 0))
            show_definition()


    def line_letter(word):
        x = 50
        y = Y - 100
        image = import_image("letter_space")
        for i in word:
            if i == "-":
                text_guess = font.render('-', True, black, white)
                display_surface.blit(text_guess, (x + 15, y - 35))
                x += 50
                if "-" not in letters_found:
                    letters_found.append("-")

            else:
                display_surface.blit(image, (x, y))
                x += 50


    def refresh_word():
        global word_myst
        word_myst = api.random_word()
        global definition
        definition = api.get_definition(word_myst)
        global synonyms
        synonyms = api.get_synonyms(word_myst)
        letters_missed.clear()
        letters_found.clear()
        global trials
        trials = 0


    def show_definition():
        definition_to_show = text_normal.render(word_myst, True, black, white)
        display_surface.blit(definition_to_show, (25, Y - 75))
        definition_to_show = text_small.render(definition, True, black, white)
        display_surface.blit(definition_to_show, (25, Y - 50))
        definition_to_show = text_small.render(synonyms, True, black, white)
        display_surface.blit(definition_to_show, (25, Y - 25))


    def show_wrong_letters():
        x = X - 100
        y = Y - 350
        letter_show = text_title.render("Letters used:", True, black, white)
        display_surface.blit(letter_show, (x - 50, y - 25))
        for i in letters_missed:
            letter_show = text_normal.render(i, True, black, white)
            display_surface.blit(letter_show, (x, y))
            y += 25


    if __name__ == '__main__':
        main_game()


except:
    logging.exception('Got exception on main handler')
    raise