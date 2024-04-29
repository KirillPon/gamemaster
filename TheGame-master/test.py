import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gradient Frame")

# Define colors
white = (255, 255, 255)
blue = (0, 0, 255)
violet = (148, 0, 211)  # RGB for violet

# Gradient frame settings
frame_thickness = 5
num_steps = 20  # Number of steps in the gradient

# Calculate color steps
r_step = (violet[0] - blue[0]) / num_steps
g_step = (violet[1] - blue[1]) / num_steps
b_step = (violet[2] - blue[2]) / num_steps

class Button:
    def __init__(self, button_color):
        self.button_color = button_color

    def draw(self, screen):
        # Draw gradient frame around the rectangle
        for step in range(num_steps):
            step_color = (int(blue[0] + step * r_step),
                          int(blue[1] + step * g_step),
                          int(blue[2] + step * b_step))

            pygame.draw.rect(screen, step_color, (340 - frame_thickness + step, 340 - frame_thickness + step, 125 + 2 * frame_thickness - 2 * step, 50 + 2 * frame_thickness - 2 * step), frame_thickness)

        # Draw solid rectangle
        pygame.draw.rect(screen, self.button_color, (340, 340, 125, 50))

# Create a button instance with a specified button color (you can adjust this color)
button = Button((0, 128, 255))  # Example color: blue

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill(white)

    # Draw the button
    button.draw(screen)

    # Update the display
    pygame.display.flip()
