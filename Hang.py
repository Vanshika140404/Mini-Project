import pygame
import math
import random

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 1920, 1080
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HANGMAN")

# Set up FPS
FPS = 60
clock = pygame.time.Clock()
run = True

# Buttons setup
radius = 35  # Increased for better visibility
space = 25
letters = []  # [x, y, "A", True]
x_start = (WIDTH - (radius * 2 + space) * 13) // 2
y_start = HEIGHT - 200  # Place buttons near the bottom of the screen

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
    "Competitive": "Always striving to be the best, especially in challenges.",
    "Resourceful": "Skilled at finding quick and clever ways to overcome difficulties.",
    "Practical": "Focused on what works effectively rather than theoretical ideas.",
    "Techsavvy": "Very skilled and comfortable with technology.",
    "Experimental": "Willing to try new methods, ideas, or styles.",
    "Collaborative": "Enjoys working with others to achieve shared goals.",
    "Adaptable": "Easily adjusts to new conditions or changes.",
    "Goaloriented": "Always focused on achieving specific objectives.",
    "Curious": "Eager to learn or know more about something.",
    "Sleepless": "Often stays up late, possibly working or studying.",
    "Caffeinated": "Fueled by coffee or energy drinks to stay active.",
    "Stressed": "Often under pressure or dealing with tension.",
    "Lastminute": "Frequently finishes tasks right before deadlines.",
    "Multitasking": "Able to handle multiple tasks at the same time.",
    "Codecentric": "Deeply focused on programming and writing code.",
    "Gamingenthusiast": "Loves playing video games as a hobby.",
    "Budgetconscious": "Careful about spending money, often saving wherever possible.",
    "Messy": "Not particularly organized; enjoys a 'creative' clutter.",
    "Jugaad": "Indian slang for finding clever, unconventional solutions."
}

# Select a random word and hint
word, hint = random.choice(list(words_with_hints.items()))
word = word.upper()
guessed = []  # Track guessed letters
hangman = 0  # Hangman state

# Draw function
def draw():
    win.fill((250, 250, 250))  # Fill background with white

    # Title
    title = TITLE.render("HangMan", 1, (0, 0, 0))
    win.blit(title, (WIDTH / 2 - title.get_width() / 2, 50))

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
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 400))  # Centered in the middle of the screen

    # Display the hint
    hint_text = WORD.render("Hint: " + hint, 1, (50, 50, 50))
    win.blit(hint_text, (WIDTH / 2 - hint_text.get_width() / 2, HEIGHT - 500))  # Positioned just above the buttons

    # Draw buttons
    for btn_pos in letters:
        x, y, ltr, visible = btn_pos
        if visible:
            pygame.draw.circle(win, (0, 0, 0), (x, y), radius, 4)
            txt = font.render(ltr, 1, (0, 0, 0))
            win.blit(txt, (x - txt.get_width() / 2, y - txt.get_height() / 2))

    # Draw hangman image
    win.blit(images[hangman], (WIDTH // 4 - images[hangman].get_width() // 2, 150))
    pygame.display.update()

# Main loop
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
                        letter[3] = False  # Hide the button
                        guessed.append(ltr)
                        if ltr not in word:
                            hangman += 1

    # Check win condition
    won = True
    for letter in word:
        if letter not in guessed:
            won = False
            break

    if won:
        draw()
        pygame.time.delay(1000)
        win.fill((0, 0, 0))
        text = WORD.render("YOU WON!", 1, (0, 255, 0))
        win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
        pygame.display.update()
        pygame.time.delay(4000)
        break

    # Check lose condition
    if hangman == 6:
        draw()
        pygame.time.delay(1000)
        win.fill((0, 0, 0))
        text = WORD.render("YOU LOST!", 1, (255, 0, 0))
        answer = WORD.render(f"The answer was: {word}", 1, (255, 255, 255))
        win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
        win.blit(answer, (WIDTH / 2 - answer.get_width() / 2, HEIGHT / 2 + 50))
        pygame.display.update()
        pygame.time.delay(4000)
        break

pygame.quit()
