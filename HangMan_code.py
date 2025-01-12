import pygame
import math
import random

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 1000, 700
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HANGMAN GAME")

# Set up FPS
FPS = 60
clock = pygame.time.Clock()

# Buttons setup
radius = 24
space = 20
letters = []  # [x, y, "A", True]
x_start = round((WIDTH - (radius * 2 + space) * 13) / 2)
y_start = 540

A = 65  # ASCII value of 'A'

for i in range(26):
    x = x_start + space * 2 + ((radius * 2 + space) * (i % 13))
    y = y_start + ((i // 13) * (space + radius * 2))
    letters.append([x, y, chr(A + i), True])

# Fonts
font_path = "fonts/Jaro-Regular-VariableFont_opsz.ttf"  
font = pygame.font.Font(font_path, 50)  # Buttons
WORD = pygame.font.Font(font_path, 60)  # Word and hints
TITLE = pygame.font.Font(font_path, 100)  # Title

# Load images for hangman
images = []
for i in range(7):
    image = pygame.image.load(f"hangman{i}.png")
    images.append(image)

# Words and hints
words_with_hints = {
    "AMBITIOUS": "Always aiming for success and achievement.",
    "COMPETITIVE": "Always striving to be the best, especially in challenges.",
    "RESOURCEFUL": "Skilled at finding quick and clever ways to overcome difficulties.",
    "PRACTICAL": "Focused on what works effectively rather than theoretical ideas.",
    "TECHSAVVY": "Very skilled and comfortable with technology.",
}

def reset_game():
    global word, hint, guessed, hangman, letters
    word, hint = random.choice(list(words_with_hints.items()))
    word = word.upper()
    guessed = []  # Reset guessed letters
    hangman = 0  # Reset hangman state
    for letter in letters:
        letter[3] = True  # Reset all buttons

reset_game()

# Draw function
def draw():
    win.fill((200, 200, 200))  # Fill background with white

    # Title
    title = TITLE.render("HangMan", 1, (0, 0, 0))
    win.blit(title, (WIDTH / 2 - title.get_width() / 2, 10))

    # Display the word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        elif letter == "-":
            display_word += "- "
        else:
            display_word += "_ "
    text = WORD.render(display_word, 1, (0, 0, 0))
    win.blit(text, (500, 250))

    # Display the hint
    hint_text = WORD.render("Hint: " + hint, 1, (100, 100, 100))
    win.blit(hint_text, (50, 450))

    # Draw buttons
    for btn_pos in letters:
        x, y, ltr, visible = btn_pos
        if visible:
            pygame.draw.circle(win, (0, 0, 0), (x, y), radius, 4)
            txt = font.render(ltr, 1, (0, 0, 0))
            win.blit(txt, (x - txt.get_width() / 2, y - txt.get_height() / 2))

    # Draw hangman image
    win.blit(images[hangman], (50, 150))

    pygame.display.update()

# End screen with interaction
def end_screen(message):
    while True:
        # Draw the end screen
        win.fill((255, 255, 255))

        # Main message
        end_message_font = pygame.font.SysFont("comicsans", 30)
        text = end_message_font.render(message, 1, (0, 0, 0))
        win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))

        # Word reveal
        word_text = WORD.render(f"The word was: {word}", 1, (50, 50, 50))
        win.blit(word_text, (WIDTH / 2 - word_text.get_width() / 2, HEIGHT / 2 + 50))

        # Draw "Play Again" button
        button_width, button_height = 200, 50
        play_again_x = WIDTH / 2 - button_width / 2
        play_again_y = HEIGHT / 2 + 100
        pygame.draw.rect(win, (0, 0, 0), (play_again_x, play_again_y, button_width, button_height), border_radius=15)
        play_again_text = WORD.render("Retry", 1, (255, 255, 255))
        win.blit(play_again_text, (play_again_x + button_width / 2 - play_again_text.get_width() / 2,
                                   play_again_y + button_height / 2 - play_again_text.get_height() / 2))

        # Draw "Exit" button
        exit_x = WIDTH / 2 - button_width / 2
        exit_y = play_again_y + button_height + 20
        pygame.draw.rect(win, (0, 0, 0), (exit_x, exit_y, button_width, button_height), border_radius=15)
        exit_text = WORD.render("Exit", 1, (255, 255, 255))
        win.blit(exit_text, (exit_x + button_width / 2 - exit_text.get_width() / 2,
                             exit_y + button_height / 2 - exit_text.get_height() / 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x_mouse, y_mouse = pygame.mouse.get_pos()

                # Check "Play Again" button
                if play_again_x <= x_mouse <= play_again_x + button_width and \
                        play_again_y <= y_mouse <= play_again_y + button_height:
                    reset_game()
                    return

                # Check "Exit" button
                if exit_x <= x_mouse <= exit_x + button_width and \
                        exit_y <= y_mouse <= exit_y + button_height:
                    pygame.quit()
                    exit()

# Main loop
run = True
while run:
    clock.tick(FPS)
    draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = pygame.mouse.get_pos()

            for letter in letters:
                x, y, ltr, visible = letter
                if visible:
                    dist = math.sqrt((x - x_mouse) ** 2 + (y - y_mouse) ** 2)
                    if dist <= radius:
                        letter[3] = False
                        guessed.append(ltr)
                        if ltr not in word:
                            hangman += 1

    # Check win condition
    if all(letter in guessed for letter in word):
        end_screen("Congratulations, YOU WON!")

    # Check lose condition
    if hangman == 6:
        end_screen(f"YOU LOST! The word was {word}.")

pygame.quit()
