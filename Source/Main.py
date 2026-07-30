import math
import pygame
import pygame_gui
import sys
import Waves


# 1. Initialize all imported pygame modules
pygame.init()

# 2. Set up the display window (Width, Height)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
managerUI = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))


# 3. Set the window title
pygame.display.set_caption("My Pygame Window")

# 4. Set up a clock to control the frame rate
clock = pygame.time.Clock()

globalTime = 0  # Get the time in seconds since the program started

amplitude = 100
frequency = 1
width = 5
dt = 0
lamda = 200


#UI Variables

Sliders = [
    ["Amplitude", amplitude, -100, 100, "Ymax"],
    ["Frequency", frequency, -10, 10, "f"],
    ["Lamda", lamda, -200, 200, "λ"],
    ["Width", width, 1, 20, "ω"]
]


SlidersElements = {}

ProperitesElements = {}

for i in range(len(Sliders)):
    slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((10, 30 * (i + 1)), (200, 30)),
        start_value=Sliders[i][1],
        value_range=(Sliders[i][2], Sliders[i][3]),
        manager=managerUI
    )

    # Create a text label for the slider
    labels = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((10, 30 * (i + 1)), (200, 30)), # Positioned just above the slider
        text=Sliders[i][0],                                # The text to display
        manager=managerUI
    )

    sliderName = Sliders[i][0]

    SlidersElements[sliderName] = slider 


    properties = pygame_gui.elements.UILabel(
        relative_rect = pygame.Rect((-50, 550 + 30 * (i + 1)), (200, 30)), # Positioned just above the slider
        text = Sliders[i][4] + ": " + str(SlidersElements[sliderName].get_current_value()),    # The text to display
        manager=managerUI
    )  

    ProperitesElements[sliderName] = properties


modeCheckBox = pygame_gui.elements.UICheckBox(
    relative_rect=pygame.Rect(225, 30, 30, 30),
    text="Click Mode",
    manager=managerUI,
    initial_state=False
)


def continousWave():
    Waves.createWave( 
        SlidersElements["Amplitude"].get_current_value(), 
        SlidersElements["Lamda"].get_current_value(), 
        SlidersElements["Frequency"].get_current_value(), 
        globalTime, 
        0, 
        SCREEN_HEIGHT/2, 
        "white", 
        screen, 
        SCREEN_WIDTH, 
        SlidersElements["Width"].get_current_value()
    )


def createWaveOnClick(mousPos):
    Waves.createWave( 
        SlidersElements["Amplitude"].get_current_value(), 
        SlidersElements["Lamda"].get_current_value(), 
        SlidersElements["Frequency"].get_current_value(), 
        globalTime, 
        0,
        SCREEN_HEIGHT/2, 
        "white", 
        screen, 
        SCREEN_WIDTH, 
        SlidersElements["Width"].get_current_value()
    )


# 5. Core Game Loop
running = True
while running:
    # Look for user interactions (Events)
    for event in pygame.event.get():
        managerUI.process_events(event)
        # If user clicks the 'X' button, break the loop
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and modeCheckBox.get_state() == True:
                createWaveOnClick(event.pos)



        if event.type == pygame.QUIT:
            running = False

    # Fill the background with an RGB color (e.g., Dark Gray)
    screen.fill((100, 100, 100))

    globalTime = pygame.time.get_ticks() / 1000.0  # Update global time in seconds


    #Update the Properity text.

    for i in range(len(Sliders)):
        ProperitesElements[Sliders[i][0]].set_text(Sliders[i][4] + ": " + str(SlidersElements[Sliders[i][0]].get_current_value()))

    if modeCheckBox.get_state() == False:
        continousWave()
    managerUI.update(dt)
    managerUI.draw_ui(screen)


    # Refresh the display to show changes
    pygame.display.flip()

    # Limit the game to 60 frames per second
    clock.tick(60)
    dt = clock.tick(60)/1000


# 6. Clean up and exit cleanly
pygame.quit()
sys.exit()





