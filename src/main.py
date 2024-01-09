import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1000, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Note Guessing Game")

# Load images
g_clef_image = pygame.image.load('assets/img/g_clef.png')
f_clef_image = pygame.image.load('assets/img/f_clef.png')
c_clef_image = pygame.image.load('assets/img/c_clef.png')
quarter_note_image = pygame.image.load('assets/img/quarter_note.png')
quarter_note_correct_image = pygame.image.load('assets/img/quarter_note_correct.png')
quarter_note_incorrect_image = pygame.image.load('assets/img/quarter_note_incorrect.png')
flat_image = pygame.image.load('assets/img/flat.png')
sharp_image = pygame.image.load('assets/img/sharp.png')
ledger_line_image = pygame.image.load('assets/img/ledger_line.png')

pixel_image = pygame.image.load('assets/img/pixel.png')

# Define notes and their corresponding keys
note_names = 'ABCDEFGH'
notes = [
    'A0', 'B0',
    'C1', 'D1', 'E1', 'F1', 'G1', 'A1', 'B1',
    'C2', 'D2', 'E2', 'F2', 'G2', 'A2', 'B2',
    'C3', 'D3', 'E3', 'F3', 'G3', 'A3', 'B3',
    'C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4',
    'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B5',
    'C6', 'D6', 'E6', 'F6', 'G6', 'A6', 'B6',
    'C7', 'D7', 'E7', 'F7', 'G7', 'A7', 'B7',
    'C8'
]

# Define accidentals and their corresponding probabilities
accidentals = ['', 'b', '#']  # None, Flat, Sharp
accidental_probabilities = [0.8, 0.1, 0.1]

# Define clefs
clefs = ['G', 'F', 'C']
clef_images = [g_clef_image, f_clef_image, c_clef_image]
clef_centernote = ['B4', 'D3', 'C4']
clef_chosen = 'G'

# Define note width, i.e. number of notes above and below the center note
center_note = clef_centernote[clefs.index(clef_chosen)]
#center_note = 'E6'
note_width = 12

# Initialize streak counter
streak_counter = 0
highest_streak = 0

black_color = (0, 0, 0)
green_color = (77, 230, 22)
red_color = (237, 28, 36)

# Main game loop
running = True
flipped = False
previous_note = ''
full_note = ''

center_pos = (height // 2) - 3

while running:
    screen.fill((255, 255, 255))

    correct_note = ''
    accidental = ''
    
    # Ensure that the same note is not chosen twice in a row, and that a valid note is chosen
    while full_note == previous_note or full_note == '' or correct_note == '':
        # Choose a random note based on the clef center note and note width
        correct_note = random.choices(notes[notes.index(center_note) - note_width : notes.index(center_note) + note_width + 1])[0]
        accidental = random.choices(accidentals, accidental_probabilities)[0]
        full_note = correct_note + accidental
        
    previous_note = full_note
    
    # If the note is C5 or higher, the quarter note should be rotated 180 degrees
    if notes.index(correct_note) >= notes.index( clef_centernote[clefs.index(clef_chosen)] ) and not flipped:
        quarter_note_image = pygame.transform.rotate(quarter_note_image, 180)
        quarter_note_correct_image = pygame.transform.rotate(quarter_note_correct_image, 180)
        quarter_note_incorrect_image = pygame.transform.rotate(quarter_note_incorrect_image, 180)
        flipped = True
    elif notes.index(correct_note) < notes.index(clef_centernote[clefs.index(clef_chosen)]) and flipped:
        quarter_note_image = pygame.transform.rotate(quarter_note_image, 180)
        quarter_note_correct_image = pygame.transform.rotate(quarter_note_correct_image, 180)
        quarter_note_incorrect_image = pygame.transform.rotate(quarter_note_incorrect_image, 180)
        flipped = False
        
    # Display Clef
    clef_image = clef_images[clefs.index(clef_chosen)]
    screen.blit(clef_image, (width // 2 - clef_image.get_width() // 2, height // 2 - clef_image.get_height() // 2))

    # Display quarter note at the correct position on the staff including octaves
    note_position = (width // 2 - quarter_note_image.get_width() // 2 + 100, center_pos + 24 - quarter_note_image.get_height() - (notes.index(correct_note) - notes.index( clef_centernote[clefs.index(clef_chosen)] )) * 24)

    # Display flat or sharp symbols based on the random modifier
    if accidental == 'b':
        screen.blit(flat_image, (note_position[0] - quarter_note_image.get_width() + flat_image.get_width() // 2, note_position[1] + quarter_note_image.get_height() // 2))
    elif accidental == '#':
        screen.blit(sharp_image, (note_position[0] - quarter_note_image.get_width() - 4, note_position[1] + sharp_image.get_height() + 5))

    # Add the correct ledger lines if the note is outside of the staff
    note_index = notes.index(correct_note)
    # Start with a note_offset of 0 if the note is C, A, F etc. Otherwise, start with a note_offset of 0
    note_offset = 1 if note_index % 2 == 0 else 0
    while(note_index <= notes.index( clef_centernote[clefs.index(clef_chosen)] ) - 6):
        screen.blit(ledger_line_image, (note_position[0] - 12, note_position[1] + quarter_note_image.get_height() - 28 - 24 * note_offset ))
        note_offset += 2
        note_index += 2
    if(notes.index(correct_note) >= notes.index( clef_centernote[clefs.index(clef_chosen)] ) + 6):
        note_index = notes.index( clef_centernote[clefs.index(clef_chosen)] ) + 6
        while(note_index <= notes.index(correct_note)):
            screen.blit(ledger_line_image, (note_position[0] - 12, note_position[1] + quarter_note_image.get_height() - 28  + 24 * note_offset ))
            note_offset += 2
            note_index += 2

    if(flipped):
        note_position = (note_position[0], note_position[1] - 2*24 + quarter_note_image.get_height())

    screen.blit(quarter_note_image, note_position)

    print(full_note)

    # Correct for E#, Fb, B#, and Cb
    if accidental == '#' and correct_note[0] == 'E':
        # Replace E with F, and remove the modifier
        correct_note = 'F' + correct_note[1:]
        accidental = ''
    elif accidental == 'b' and correct_note[0] == 'F':
        # Replace F with E, and remove the modifier
        correct_note = 'E' + correct_note[1:]
        accidental = ''
    elif accidental == '#' and correct_note[0] == 'B':
        # Replace B with C, and remove the modifier. Shift the octave up by one
        correct_note = 'C' + str(int(correct_note[1]) + 1)
        accidental = ''
    elif accidental == 'b' and correct_note[0] == 'C':
        # Replace C with B, and remove the modifier. Shift the octave down by one
        correct_note = 'B' + str(int(correct_note[1]) - 1)
        accidental = ''
  
    # Display streak counter
    font = pygame.font.Font(None, 36)
    
    text_color = black_color
    if(streak_counter == 0 and highest_streak > 0):
        text_color = red_color
    elif(streak_counter > 0 and streak_counter == highest_streak):
        text_color = green_color
    
    streak_text = font.render("Streak: {}".format(streak_counter), True, text_color)
    highest_streak_text = font.render("Highest: {}".format(highest_streak), True, black_color)
    screen.blit(streak_text, (23, center_pos - 20))
    screen.blit(highest_streak_text, (10, center_pos + 20))

    # Update the display
    pygame.display.flip()

    # Wait for user input
    waiting_for_input = True
    correct_guess = False
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                waiting_for_input = False
            elif event.type == pygame.KEYDOWN:
                print(pygame.key.name(event.key))
                if pygame.key.name(event.key).upper() == 'H':
                    event.key = pygame.K_b
                if event.key == pygame.K_ESCAPE:
                    running = False
                    waiting_for_input = False
                elif correct_note[0].find(pygame.key.name(event.key).upper()) != -1:
                    if accidental != '':
                        # Check if the user is holding down the correct modifier key
                        if accidental == 'b' and event.mod & pygame.KMOD_CTRL:
                            waiting_for_input = False
                            correct_guess = True
                            print('Correct!')
                            streak_counter += 1
                        elif accidental == '#' and event.mod & pygame.KMOD_SHIFT:
                            waiting_for_input = False
                            correct_guess = True
                            print('Correct!')
                            streak_counter += 1
                        else:
                            print('Incorrect!')
                            streak_counter = 0
                            waiting_for_input = False
                    else:
                        # No modifier, ensure that the user is not holding down any modifier keys
                        if not (event.mod & pygame.KMOD_CTRL or event.mod & pygame.KMOD_SHIFT):
                            waiting_for_input = False
                            correct_guess = True
                            print('Correct!')
                            streak_counter += 1
                        else:
                            print('Incorrect!')
                            streak_counter = 0
                            waiting_for_input = False
                elif(note_names.find(pygame.key.name(event.key).upper()) != -1):
                    print('Incorrect!')
                    streak_counter = 0
                    waiting_for_input = False
    
    if(correct_guess):
        screen.blit(quarter_note_correct_image, note_position)
        highest_streak = max(streak_counter, highest_streak)
    else:
        screen.blit(quarter_note_incorrect_image, note_position)
  
    pygame.display.flip()
    pygame.time.wait(250)
                    
# Quit Pygame
pygame.quit()