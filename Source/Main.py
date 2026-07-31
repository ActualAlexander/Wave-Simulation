import math
import pygame
import pygame_gui
import sys
import Waves


# 1. Initialize Pygame
pygame.init()

# 2. Set up display window
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
managerUI = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("My Pygame Window")

clock = pygame.time.Clock()

globalTime = 0  # Time in seconds
amplitude = 100
frequency = 1
width = 5
dt = 0
lamda = 200

# ClickMode variables
isMouseClicked = False
isCopiedClicked = False
clickedPos = (0, 0)
clickTimer = 0  # Now also tracked in seconds!

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

    labels = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((10, 30 * (i + 1)), (200, 30)),
        text=Sliders[i][0],
        manager=managerUI
    )

    sliderName = Sliders[i][0]
    SlidersElements[sliderName] = slider

    properties = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((-50, 550 + 30 * (i + 1)), (200, 30)),
        text=Sliders[i][4] + ": " + str(SlidersElements[sliderName].get_current_value()),
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
        SCREEN_HEIGHT / 2, 
        "white", 
        screen, 
        SCREEN_WIDTH, 
        SlidersElements["Width"].get_current_value()
    )


def createWaveOnClick(mousPos):
    global isCopiedClicked, clickedPos
    if not isCopiedClicked:
        clickedPos = mousPos
        isCopiedClicked = True

    Waves.createWave(
        SlidersElements["Amplitude"].get_current_value(), 
        SlidersElements["Lamda"].get_current_value(), 
        SlidersElements["Frequency"].get_current_value(), 
        globalTime, 
        clickedPos[0], 
        clickedPos[1], 
        "white", 
        screen, 
        SCREEN_WIDTH, 
        SlidersElements["Width"].get_current_value()
    )


def modes():
    global isMouseClicked, isCopiedClicked, globalTime, clickTimer

    # Continuous mode when box is unchecked
    if not modeCheckBox.get_state():
        continousWave()
        isMouseClicked = False
        isCopiedClicked = False

    # Click mode active
    if isMouseClicked and modeCheckBox.get_state():
        createWaveOnClick(clickedPos)

        # FIX 1: Check 3.0 seconds (since globalTime & clickTimer are both in seconds)
        if globalTime - clickTimer >= 3.0:
            isMouseClicked = False
            isCopiedClicked = False


def main():
    global dt, isMouseClicked, isCopiedClicked, clickedPos, clickTimer, globalTime
    running = True

    while running:
        globalTime = pygame.time.get_ticks() / 1000.0  # Seconds elapsed

        for event in pygame.event.get():
            managerUI.process_events(event)

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Don't trigger click-wave if clicking UI components
                    if not modeCheckBox.rect.collidepoint(event.pos):
                        isMouseClicked = True
                        isCopiedClicked = False
                        clickedPos = event.pos
                        clickTimer = globalTime  # Store timestamp in seconds!

        screen.fill((100, 100, 100))

        # Update properties text
        for i in range(len(Sliders)):
            ProperitesElements[Sliders[i][0]].set_text(
                Sliders[i][4] + ": " + str(SlidersElements[Sliders[i][0]].get_current_value())
            )

        modes()

        managerUI.update(dt)
        managerUI.draw_ui(screen)

        pygame.display.flip()

        # FIX 2: Only call tick once per frame!
        dt = clock.tick(60) / 1000.0

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()