import pygame, sys  # Imports pygame for game development and sys for system operations
from pygame.locals import *  # Imports constants and functions from pygame.locals
import random  # Imports random module for random number generation

def start_pygame_game():
    pygame.init()  # Initializes all imported pygame modules
    pygame.mixer.init()  # Initializes the mixer module for sound

    width = 600  # Sets the width of the game window
    height = 700  # Sets the height of the game window

    screen = pygame.display.set_mode((width, height))  # Creates a game window of specified width and height
    pygame.display.set_caption("Road Rush")  # Sets the caption of the game window

    gray = (100, 100, 100)  # Defines the color gray in RGB
    green = (76, 208, 56)  # Defines the color green in RGB
    red = (200, 0, 0)  # Defines the color red in RGB
    white = (255, 255, 255)  # Defines the color white in RGB
    yellow = (255, 232, 0)  # Defines the color yellow in RGB

    left_lane = 140  # Sets the x-coordinate for the left lane
    right_lane = 470  # Sets the x-coordinate for the right lane
    center_lane = 300  # Sets the x-coordinate for the center lane

    lanes = [left_lane, center_lane, right_lane]  # Creates a list of lane coordinates

    class Vehicle(pygame.sprite.Sprite):  # Defines the Vehicle class inheriting from pygame's Sprite class
        def __init__(self, image, x, y, scale):
            pygame.sprite.Sprite.__init__(self)  # Initializes the parent Sprite class

            # scale down the image to fit in lane
            image_scale = scale / image.get_rect().width  # Calculates the scaling factor based on the image width
            new_width = image.get_rect().width * image_scale  # Calculates the new width of the image
            new_height = image.get_rect().height * image_scale  # Calculates the new height of the image

            self.image = pygame.transform.scale(image, (new_width, new_height))  # Scales the image
            self.rect = self.image.get_rect(center=(x, y))  # Sets the position of the image

    class PlayerVehicle(Vehicle):  # Defines the PlayerVehicle class inheriting from Vehicle class
        def __init__(self, x, y, vehicle, scale):
            image = vehicle  # Assigns the vehicle image to the variable
            super().__init__(image, x, y, scale)  # Calls the parent class constructor

    def main(screen, vehicles_list, path, car, scale, color, sound):
        clock = pygame.time.Clock()  # Creates a clock object to manage frame rate
        fps = 120  # Sets the frames per second
        running = True  # Sets the game running state to True
        
        game_over = False  # Sets the game over state to False
        Pause = False  # Sets the pause state to False
        speed = 5  # Sets the initial speed of the vehicles
        score = 0  # Sets the initial score to 0

        road = path  # Assigns the road image path
        road_y = 0  # Sets the initial y-coordinate of the road

        player_x = 300  # Sets the initial x-coordinate of the player vehicle
        player_y = 600  # Sets the initial y-coordinate of the player vehicle

        player_group = pygame.sprite.Group()  # Creates a group for the player sprite
        player = PlayerVehicle(player_x, player_y, car, scale)  # Creates a PlayerVehicle object
        player_group.add(player)  # Adds the player object to the player group

        Road_filenames = vehicles_list  # Assigns the list of vehicle image filenames

        vehicle_image = []  # Creates an empty list for vehicle images

        for image_filename in Road_filenames:
            image = pygame.image.load(image_filename).convert_alpha()  # Loads and converts the image
            vehicle_image.append(image)  # Appends the image to the vehicle_image list

        vehicle_group = pygame.sprite.Group()  # Creates a group for the vehicle sprites

        crash = pygame.image.load('Assest/explosion1.png').convert_alpha()  # Loads the crash image
        crash_rect = crash.get_rect()  # Gets the rect of the crash image

        crash_sound = pygame.mixer.Sound('Assest/SFX/Crash.mp3')  # Loads the crash sound
        crash_sound.set_volume(0.5)  # Sets the volume of the crash sound

        tpbg = pygame.image.load('Assest/UI/TPBG.png')  # Loads the background image for game over screen

        restart = pygame.image.load('Assest/UI/restart.png').convert_alpha()  # Loads the restart button image
        restart_rect = restart.get_rect(center=(300, 230))  # Sets the position of the restart button
        restart_rect2 = restart.get_rect(center=(300, 306))  # Sets the position of the restart button

        menu_img = pygame.image.load('Assest/UI/menu_btn.png').convert_alpha()  # Loads the menu button image
        menu_rect = menu_img.get_rect(center=(300, 345))  # Sets the position of the menu button
        menu_rect2 = menu_img.get_rect(center=(300, 407))  # Sets the position of the menu button

        exit_img = pygame.image.load('Assest/UI/exit_btn.png').convert_alpha()  # Loads the exit button image
        exit_rect = exit_img.get_rect(center=(300, 460))  # Sets the position of the exit button
        exit_rect2 = exit_img.get_rect(center=(300, 508))  # Sets the position of the exit button
        
        resume = pygame.image.load('Assest/UI/resume.png').convert_alpha()  # Loads the resume button image
        resume_rect = resume.get_rect(center=(300, 205))  # Sets the position of the resume button
        
        sound.play(-1)  # Plays the background sound in a loop

        while running:
            clock.tick(fps)  # Manages the frame rate

            for event in pygame.event.get():  # Loops through the event queue
                if event.type == QUIT:  # Checks if the quit event is triggered
                    pygame.quit()  # Quits pygame
                    sys.exit()  # Exits the system
                if event.type == KEYDOWN:  # Checks if a key is pressed
                    if event.key == K_LEFT and player.rect.center[0] > left_lane:  # Checks if the left arrow key is pressed and the player is not in the leftmost lane
                        player.rect.x -= 160  # Moves the player vehicle to the left
                    elif event.key == K_RIGHT and player.rect.center[0] < 400:  # Checks if the right arrow key is pressed and the player is not in the rightmost lane
                        player.rect.x += 160  # Moves the player vehicle to the right
                    elif event.key == K_ESCAPE:  # Checks if the escape key is pressed
                        Pause = not Pause  # Toggles the pause state
                if event.type == MOUSEBUTTONDOWN and Pause:  # Checks if the mouse button is pressed and the game is paused
                    if resume_rect.collidepoint(event.pos):  # Checks if the resume button is clicked
                        sound.play(-1)
                        Pause = False  # Resumes the game
                    elif restart_rect2.collidepoint(event.pos):  # Checks if the restart button is clicked
                        game_over = False  # Resets the game over state
                        Pause = False  # Resumes the game
                        speed = 5  # Resets the speed
                        score = 0  # Resets the score
                        vehicle_group.empty()  # Empties the vehicle group
                        player.rect.center = [player_x, player_y]  # Resets the player position
                        sound.play(-1)  # Plays the background sound
                    elif menu_rect2.collidepoint(event.pos):  # Checks if the menu button is clicked
                        running = False  # Stops the game loop
                        game_over = False  # Resets the game over state
                        main_menu(screen)  # Calls the main menu function
                    elif exit_rect2.collidepoint(event.pos):  # Checks if the exit button is clicked
                        running = False  # Stops the game loop
                        sys.exit()  # Exits the system
            
            if not Pause:  # Checks if the game is not paused
                road_y += speed  # Moves the road downwards
                if road_y >= height:  # Resets the road position if it moves out of the screen
                    road_y = 0

                screen.fill(color)  # Fills the screen with the background color

                screen.blit(road, (50, road_y))  # Draws the road image
                screen.blit(road, (50, road_y - height))  # Draws the second road image for continuous effect

                player_group.draw(screen)  # Draws the player group on the screen

                if len(vehicle_group) < 2:  # Checks if the number of vehicles is less than 2
                    add_vehicle = True
                    for vehicle in vehicle_group:  # Loops through the vehicle group
                        if vehicle.rect.top < vehicle.rect.height * 1.5:  # Checks if any vehicle is within 1.5 times its height from the top
                            add_vehicle = False  # Sets add_vehicle to False if condition is met

                    if add_vehicle:  # Checks if add_vehicle is True
                        lane = random.choice(lanes)  # Chooses a random lane
                        image = random.choice(vehicle_image)  # Chooses a random vehicle image
                        vehicle = Vehicle(image, lane, height / -2, scale)  # Creates a Vehicle object
                        vehicle_group.add(vehicle)  # Adds the vehicle to the vehicle group

                for vehicle in vehicle_group:  # Loops through the vehicle group
                    vehicle.rect.y += speed  # Moves the vehicle downwards
                    if vehicle.rect.top >= height:  # Checks if the vehicle moves out of the screen
                        vehicle.kill()  # Removes the vehicle from the group
                        score += 1  # Increases the score
                        if score > 0 and score % 5 == 0:  # Checks if the score is a multiple of 5
                            speed += 1  # Increases the speed

                vehicle_group.draw(screen)  # Draws the vehicle group on the screen

                font = pygame.font.Font(pygame.font.get_default_font(), 30)  # Sets the font for the score
                text = font.render(f'Score: {score}', True, white)  # Renders the score text
                text_rect = text.get_rect()  # Gets the rect of the score text
                text_rect.topleft = (70, 650)  # Sets the position of the score text
                screen.blit(text, text_rect)  # Draws the score text on the screen

                if pygame.sprite.spritecollide(player, vehicle_group, True):  # Checks for collision between player and vehicles
                    crash_sound.play()  # Plays the crash sound
                    game_over = True  # Sets the game over state to True
                    crash_rect.center = [player.rect.center[0], player.rect.top]  # Sets the position of the crash image

                if game_over:  # Checks if the game is over
                    speed = 0  # Sets the speed to 0
                    screen.blit(crash, crash_rect)  # Draws the crash image on the screen
                    screen.blit(tpbg, (0, 0))  # Draws the game over background
                    screen.blit(restart, restart_rect)  # Draws the restart button
                    screen.blit(menu_img, menu_rect)  # Draws the menu button
                    screen.blit(exit_img, exit_rect)  # Draws the exit button
                    pygame.draw.rect(screen, red, (0, 50, width, 104))  # Draws a red rectangle for game over text
                    font = pygame.font.Font(pygame.font.get_default_font(), 50)  # Sets the font for the game over text
                    text = font.render('Game Over.', True, white)  # Renders the game over text
                    text_rect = text.get_rect(center=(width / 2, 100))  # Sets the position of the game over text
                    screen.blit(text, text_rect)  # Draws the game over text on the screen
                    sound.stop()  # Stops the background sound

                pygame.display.update()  # Updates the display


                while game_over:  # Loop that runs continuously while the game is in a game-over state
                    clock.tick(fps)  # Manages the frame rate to ensure the game runs at the defined frames per second (fps)
                    
                    for event in pygame.event.get():  # Loops through all events in the event queue
                        if event.type == QUIT:  # Checks if the user has requested to quit the game
                            running = False  # Stops the main game loop
                            game_over = False  # Exits the game-over state
                        
                        if event.type == MOUSEBUTTONDOWN:  # Checks if a mouse button has been pressed
                            if restart_rect.collidepoint(event.pos):  # Checks if the mouse click was within the restart button's area
                                sound.play(-1)  # Plays the background sound on a loop
                                game_over = False  # Resets the game-over state
                                speed = 5  # Resets the speed of the game
                                score = 0  # Resets the player's score
                                vehicle_group.empty()  # Clears all vehicles from the vehicle group
                                player.rect.center = [player_x, player_y]  # Resets the player's position
                            
                            elif menu_rect.collidepoint(event.pos):  # Checks if the mouse click was within the menu button's area
                                running = False  # Stops the main game loop
                                main_menu(screen)  # Calls the main menu function
                            
                            elif exit_rect.collidepoint(event.pos):  # Checks if the mouse click was within the exit button's area
                                game_over = False  # Exits the game-over state
                                running = False  # Stops the main game loop
                                sys.exit()  # Exits the program

            else:  # If the game is paused (not in a game-over state)
                screen.blit(resume, resume_rect)  # Draws the resume button on the screen at the specified position
                screen.blit(restart, restart_rect2)  # Draws the restart button on the screen at the specified position
                screen.blit(menu_img, menu_rect2)  # Draws the menu button on the screen at the specified position
                screen.blit(exit_img, exit_rect2)  # Draws the exit button on the screen at the specified position
                
                pygame.draw.rect(screen, red, (0, 50, width, 104))  # Draws a red rectangle at the top of the screen for the pause text
                font = pygame.font.Font(pygame.font.get_default_font(), 50)  # Sets the font for the pause text
                text = font.render('Pause', True, white)  # Renders the text 'Pause' with the chosen font and color
                text_rect = text.get_rect(center=(width / 2, 100))  # Positions the text in the center of the red rectangle
                screen.blit(text, text_rect)  # Draws the pause text on the screen at the specified position
                
                sound.stop()  # Stops the background sound
                pygame.display.update()  # Updates the display to show the latest drawn frame


    def level_select_menu(screen):  # Defines the function to display the level selection menu
        clock = pygame.time.Clock()  # Creates a clock object to manage the frame rate
        fps = 120  # Sets the frames per second
        running = True  # Sets the running state to true
        menu = True  # Sets the menu state to true (though this variable isn't used later)

        Bg_image = pygame.image.load('Assest/UI/BG.png')  # Loads the background image
        Ocean_level = pygame.image.load('Assest/UI/Ocean.png').convert_alpha()  # Loads the ocean level image with alpha transparency
        Ocean_rect = Ocean_level.get_rect(topleft=(326, 162))  # Sets the position of the ocean level image

        Road_level = pygame.image.load('Assest/UI/Road.png').convert_alpha()  # Loads the road level image with alpha transparency
        Road_rect = Road_level.get_rect(topleft=(91, 162))  # Sets the position of the road level image

        Sky_level = pygame.image.load('Assest/UI/Sky.png').convert_alpha()  # Loads the sky level image with alpha transparency
        Sky_rect = Sky_level.get_rect(topleft=(91, 444))  # Sets the position of the sky level image

        Space_level = pygame.image.load('Assest/UI/Space.png').convert_alpha()  # Loads the space level image with alpha transparency
        Space_rect = Space_level.get_rect(topleft=(326, 444))  # Sets the position of the space level image

        font = pygame.font.Font('Assest/UI/Morspeed-7Be1D.otf', 50)  # Loads a custom font
        text = font.render('_CHOOSE LEVEL_', True, white)  # Renders the "CHOOSE LEVEL" text with the font and white color
        text_rect = text.get_rect()  # Gets the rectangle object for the text
        text_rect.center = (300, 70)  # Centers the text at the specified coordinates

        while running:  # Main loop that runs while the menu is active
            clock.tick(fps)  # Manages the frame rate
            for event in pygame.event.get():  # Loops through all events in the event queue
                if event.type == QUIT:  # Checks if the user has requested to quit
                    pygame.quit()  # Quits Pygame
                    sys.exit()  # Exits the system

                elif event.type == MOUSEBUTTONDOWN:  # Checks if a mouse button has been pressed
                    if Road_rect.collidepoint(event.pos):  # Checks if the mouse click was within the road level button's area
                        # main(screen)
                        vehicle = pygame.image.load('Assest/Road/Car.png').convert_alpha()  # Loads the player's vehicle for the road level

                        vehicle_list = [
                            'Assest/Road/8.png', 'Assest/Road/2.png', 'Assest/Road/3.png', 
                            'Assest/Road/4.png', 'Assest/Road/5.png', 'Assest/Road/6.png', 
                            'Assest/Road/7.png'
                        ]  # List of vehicle images for the road level

                        path = pygame.image.load("Assest/Road/BG.png").convert_alpha()  # Loads the background image for the road level
                        sound = pygame.mixer.Sound('Assest/SFX/Car.wav')  # Loads the background sound for the road level
                        sound.set_volume(0.5)  # Sets the volume of the sound

                        main(screen, vehicle_list, path, vehicle, 50, green, sound)  # Calls the main game function with road level parameters
                        pygame.quit()  # Quits Pygame after the main function finishes
                        sys.exit()  # Exits the system

                    elif Ocean_rect.collidepoint(event.pos):  # Checks if the mouse click was within the ocean level button's area
                        # main(screen)
                        vehicle = pygame.image.load('Assest/Ocean/boat.png').convert_alpha()  # Loads the player's vehicle for the ocean level

                        vehicle_list = [
                            'Assest/Ocean/1.png', 'Assest/Ocean/2.png', 'Assest/Ocean/3.png', 
                            'Assest/Ocean/4.png', 'Assest/Ocean/5.png', 'Assest/Ocean/6.png', 
                            'Assest/Ocean/7.png', 'Assest/Ocean/8.png'
                        ]  # List of vehicle images for the ocean level

                        path = pygame.image.load("Assest/Ocean/BG.png").convert_alpha()  # Loads the background image for the ocean level
                        sound = pygame.mixer.Sound('Assest/SFX/Boat.mp3')  # Loads the background sound for the ocean level
                        sound.set_volume(0.1)  # Sets the volume of the sound

                        main(screen, vehicle_list, path, vehicle, 70, '#f8dfa7', sound)  # Calls the main game function with ocean level parameters
                        pygame.quit()  # Quits Pygame after the main function finishes
                        sys.exit()  # Exits the system

                    elif Sky_rect.collidepoint(event.pos):  # Checks if the mouse click was within the sky level button's area
                        # main(screen)
                        vehicle = pygame.image.load('Assest/Sky/Plane.png').convert_alpha()  # Loads the player's vehicle for the sky level

                        vehicle_list = [
                            'Assest/Sky/1.png', 'Assest/Sky/2.png', 'Assest/Sky/3.png', 
                            'Assest/Sky/4.png', 'Assest/Sky/5.png', 'Assest/Sky/6.png', 
                            'Assest/Sky/7.png'
                        ]  # List of vehicle images for the sky level

                        path = pygame.image.load("Assest/Sky/BG.png").convert_alpha()  # Loads the background image for the sky level
                        sound = pygame.mixer.Sound('Assest/SFX/Plane.mp3')  # Loads the background sound for the sky level
                        sound.set_volume(0.1)  # Sets the volume of the sound

                        main(screen, vehicle_list, path, vehicle, 120, 'blue', sound)  # Calls the main game function with sky level parameters
                        pygame.quit()  # Quits Pygame after the main function finishes
                        sys.exit()  # Exits the system

                    elif Space_rect.collidepoint(event.pos):  # Checks if the mouse click was within the space level button's area
                        # main(screen)
                        vehicle = pygame.image.load('Assest/Space/Spaceship.png').convert_alpha()  # Loads the player's vehicle for the space level

                        vehicle_list = [
                            'Assest/Space/1.png', 'Assest/Space/2.png', 'Assest/Space/3.png', 
                            'Assest/Space/4.png', 'Assest/Space/5.png', 'Assest/Space/6.png', 
                            'Assest/Space/7.png', 'Assest/Space/8.png'
                        ]  # List of vehicle images for the space level

                        path = pygame.image.load("Assest/Space/BG.png").convert_alpha()  # Loads the background image for the space level
                        sound = pygame.mixer.Sound('Assest/SFX/Spaceship.mp3')  # Loads the background sound for the space level
                        # sound.set_volume(50)  # This line is commented out, which means the volume is not set

                        main(screen, vehicle_list, path, vehicle, 70, 'gray', sound)  # Calls the main game function with space level parameters
                        pygame.quit()  # Quits Pygame after the main function finishes
                        sys.exit()  # Exits the system

            screen.blit(Bg_image, (0, 0))  # Draws the background image on the screen
            screen.blit(Ocean_level, Ocean_rect)  # Draws the ocean level button on the screen
            screen.blit(Road_level, Road_rect)  # Draws the road level button on the screen
            screen.blit(Sky_level, Sky_rect)  # Draws the sky level button on the screen
            screen.blit(Space_level, Space_rect)  # Draws the space level button on the screen
            screen.blit(text, text_rect)  # Draws the "CHOOSE LEVEL" text on the screen

            pygame.display.update()  # Updates the display to show the latest drawn frame


    def main_menu(screen):  # Defines the function to display the main menu
        clock = pygame.time.Clock()  # Creates a clock object to manage the frame rate
        fps = 120  # Sets the frames per second
        running = True  # Sets the running state to true
        menu = True  # Sets the menu state to true

        Bg_image = pygame.image.load('Assest/UI/BG.png')  # Loads the background image
        Start_btn = pygame.image.load('Assest/UI/start_btn.png')  # Loads the start button image
        Start_btn_rect = Start_btn.get_rect(center=(width / 2, 400))  # Sets the position of the start button at the center of the screen horizontally and 400 pixels down vertically
        Exit_btn = pygame.image.load('Assest/UI/exit_btn.png')  # Loads the exit button image
        Exit_btn_rect = Exit_btn.get_rect(center=(width / 2, 500))  # Sets the position of the exit button at the center of the screen horizontally and 500 pixels down vertically

        name_img = pygame.image.load('Assest/UI/Name.png')  # Loads the game name image

        while running:  # Main loop that runs while the menu is active
            clock.tick(fps)  # Manages the frame rate
            for event in pygame.event.get():  # Loops through all events in the event queue
                if event.type == QUIT:  # Checks if the user has requested to quit
                    pygame.quit()  # Quits Pygame
                    sys.exit()  # Exits the system
                elif event.type == MOUSEBUTTONDOWN:  # Checks if a mouse button has been pressed
                    if Start_btn_rect.collidepoint(event.pos):  # Checks if the mouse click was within the start button's area
                        # main(screen)
                        level_select_menu(screen)  # Calls the level selection menu function
                        menu = False  # Sets the menu state to false to stop rendering the main menu
                    elif Exit_btn_rect.collidepoint(event.pos):  # Checks if the mouse click was within the exit button's area
                        running = False  # Sets the running state to false to exit the main loop

            if menu:  # Checks if the menu state is true
                screen.blit(Bg_image, (0, 0))  # Draws the background image on the screen
                screen.blit(Start_btn, Start_btn_rect)  # Draws the start button on the screen
                screen.blit(Exit_btn, Exit_btn_rect)  # Draws the exit button on the screen
                screen.blit(name_img, (0, 50))  # Draws the game name image at the top of the screen

            pygame.display.update()  # Updates the display to show the latest drawn frame

    main_menu(screen)  # Calls the main menu function to start the program


# Main block to start the application and a secondary game function
if __name__ == "__main__":
    start_pygame_game()

    