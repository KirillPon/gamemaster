import pygame
import sys
import props

pygame.init()
screen = 0
# Set up colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
font = pygame.font.Font('freesansbold.ttf', 20)


# Set up fonts
font = pygame.font.Font(None, 36)


class GameControl:
    def __init__(self):
        self.volume_control = VolumeControl()
        self.theme_control = ThemeControl()
        self.options_button = Options()
        self.buttons = [
                           ToggleButton(f"Button{i + 1}", (150 + i * 150, 110)) for i in range(4)
                       ] + [
                           ToggleButton(f"Button{i + 5}", (140 + (i - 5) * 150, 160)) for i in range(4)
                       ]

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.volume_control.handle_event(event)
            self.theme_control.handle_event(event)
            self.options_button.handle_event(event)
            for button in self.buttons:
                button.handle_event(event)

        # Cap the frame rate
        pygame.time.Clock().tick(30)

    def draw(self):
        # Clear the screen
        screen.fill(self.theme_control.background_color)

        # Update and draw the game controls
        self.volume_control.draw(screen)
        self.theme_control.draw(screen)
        self.options_button.draw(screen)
        for button in self.buttons:
            button.draw(screen)

        # Update the display
        pygame.display.flip()


class VolumeControl:
    def __init__(self):
        self.volume_level = 0.5  # Starting volume level (0.0 to 1.0)
        self.music_playing = False
        self.load_music()

    def load_music(self):
        pygame.mixer.music.load("CIPI.mp3")  # Replace with your music file path

    def play_music(self):
        if not self.music_playing:
            pygame.mixer.music.play(-1)  # -1 plays the music in an infinite loop
            self.music_playing = True

    def stop_music(self):
        if self.music_playing:
            pygame.mixer.music.stop()
            self.music_playing = False

    def adjust_volume(self, delta):
        self.volume_level += delta / 100.0  # Delta is in the range [-100, 100], convert to [-1.0, 1.0]
        self.volume_level = max(0.0, min(1.0, self.volume_level))  # Ensure volume is within the valid range
        pygame.mixer.music.set_volume(self.volume_level)

    def draw(self, screen):
        # Draw volume label
        volume_text = font.render("Volume: {}".format(int(self.volume_level * 100)), True, white)
        screen.blit(volume_text, (10, 10))

        # Draw volume control buttons
        pygame.draw.rect(screen, white, (200, 10, 40, 40))  # Plus button
        plus_text = font.render("+", True, black)
        screen.blit(plus_text, (215, 20))

        pygame.draw.rect(screen, white, (250, 10, 40, 40))  # Minus button
        minus_text = font.render("-", True, black)
        screen.blit(minus_text, (265, 20))

        pygame.draw.rect(screen, white, (310, 10, 80, 40))  # Play/Stop button
        play_stop_text = font.render("Play/Stop", True, black)
        screen.blit(play_stop_text, (320, 20))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if 200 <= mouse_x <= 240 and 10 <= mouse_y <= 50:
                self.adjust_volume(10)  # Increase volume
            elif 250 <= mouse_x <= 290 and 10 <= mouse_y <= 50:
                self.adjust_volume(-10)  # Decrease volume
            elif 310 <= mouse_x <= 390 and 10 <= mouse_y <= 50:
                if self.music_playing:
                    self.stop_music()
                else:
                    self.play_music()


all_themes = [{'fontColor': props.fontColor, 'backgroundColor': props.backgroundColor},
              {'fontColor': 'black', 'backgroundColor': 'lightgrey'}]


class ThemeControl:
    def __init__(self):
        self.current_theme = 1  # 1: Green and Blue, 2: Black and White
        self.set_theme()

    def set_theme(self):
        self.background_color = all_themes[self.current_theme-1]['backgroundColor']
        self.button_color = green
        self.text_color = black

    def switch_theme(self):
        self.current_theme = 3 - self.current_theme  # Toggle between 1 and 2
        self.set_theme()

    def draw(self, screen):
        # Draw theme label
        theme_text = font.render("Theme: {}".format(self.current_theme), True, self.text_color)
        screen.blit(theme_text, (10, 70))

        # Draw theme switch button
        pygame.draw.rect(screen, self.button_color, (200, 70, 120, 40))
        switch_text = font.render("Switch Theme", True, self.text_color)
        screen.blit(switch_text, (210, 80))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if 200 <= mouse_x <= 320 and 70 <= mouse_y <= 110:
                self.switch_theme()


class Options:
    def __init__(self):
        self.clicked = False
        self.checkbox_checked = False  # Added attribute for checkbox state

    def draw(self, screen):
        pygame.draw.rect(screen, white, (10, 110, 120, 40))
        button_text = font.render("Options", True, black)
        screen.blit(button_text, (20, 120))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if 10 <= mouse_x <= 130 and 110 <= mouse_y <= 150:
                self.clicked = not self.clicked  # Toggle the clicked state

                # Toggle checkbox state when button is clicked
                if self.clicked:
                    self.checkbox_checked = not self.checkbox_checked


class ToggleButton:
    def __init__(self, text, position):
        self.text = text
        self.position = position
        self.clicked = False
        self.checkbox_checked = False

    def draw(self, screen):
        # Draw button
        pygame.draw.rect(screen, white, (*self.position, 120, 40))
        button_text = font.render(self.text, True, black)
        screen.blit(button_text, (self.position[0] + 10, self.position[1] + 10))
        pygame.draw.rect(screen, white, (self.position[0] + 120, self.position[1], 20, 20))
        # Draw checkbox if clicked
        if self.clicked:
            pygame.draw.line(screen, black, (self.position[0] + 125, self.position[1] + 5),
                             (self.position[0] + 135, self.position[1] + 15), 2)
            pygame.draw.line(screen, black, (self.position[0] + 135, self.position[1] + 15),
                             (self.position[0] + 145, self.position[1] - 5), 2)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Check button click
            if self.position[0] <= mouse_x <= self.position[0] + 120 and self.position[1] <= mouse_y <= self.position[
                1] + 40:
                self.clicked = not self.clicked

                # Toggle checkbox state when button is clicked
                if self.clicked:
                    self.checkbox_checked = not self.checkbox_checked


# Create an instance of GameControl
game_control = GameControl()


def settings_button_pressed(screen1):
    global screen
    screen = screen1
    while True:
        game_control.update()
        game_control.draw()
